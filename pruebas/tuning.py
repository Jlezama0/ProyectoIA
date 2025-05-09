from google import genai
from google.genai import types
import time

client = genai.Client(api_key="AIzaSyDn9rLwtZX8rwTA004lC0oWPsSJvJeIEe4")

for model_info in client.models.list():
    print(model_info.name)


'''
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Escribe un poema corto sobre el amor"
)
print(response.text)

'''
# create tuning model
training_dataset =  [
    ["1", "2"],
    ["3", "4"],
    ["-3", "-2"],
    ["twenty two", "twenty three"],
    ["two hundred", "two hundred one"],
    ["ninety nine", "one hundred"],
    ["8", "9"],
    ["-98", "-97"],
    ["1,000", "1,001"],
    ["10,100,000", "10,100,001"],
    ["thirteen", "fourteen"],
    ["eighty", "eighty one"],
    ["one", "two"],
    ["three", "four"],
    ["seven", "eight"],
]
training_dataset=types.TuningDataset(
        examples=[
            types.TuningExample(
                text_input=i,
                output=o,
            )
            for i,o in training_dataset
        ],
    )
tuning_job = client.tunings.tune(
    base_model='models/gemini-1.5-flash-001-tuning',
    training_dataset=training_dataset,
    config=types.CreateTuningJobConfig(
        epoch_count= 5,
        batch_size=4,
        learning_rate=0.001,
        tuned_model_display_name="test tuned model"
    )
)

# 7. Inicio del Trabajo de Ajuste Fino (Fine-Tuning)
print("Iniciando el trabajo de ajuste fino...")
tuning_job = client.tunings.tune(
    base_model='models/gemini-1.5-flash-001-tuning',
    training_dataset=training_dataset,
    config=types.CreateTuningJobConfig(
        epoch_count= 5,
        batch_size=4,
        learning_rate=0.001,
        tuned_model_display_name="test tuned model"
    )
)

job_name = tuning_job.name # Obtenemos el nombre único del trabajo iniciado
print(f"Trabajo de ajuste iniciado con nombre: {job_name}")
print("Esperando a que el trabajo se complete (esto puede tardar)...")

# 7.1. <<< NUEVO: Bucle de Espera y Verificación de Estado >>>
# Este bucle verifica periódicamente el estado del trabajo en Google Cloud.
while True:
    # Obtenemos la información más reciente del trabajo usando su nombre
    # Es importante llamar a client.tunings.get() para refrescar el estado
    try:
        job_status = client.tunings.get(name=job_name)

        # Los estados exactos pueden variar ligeramente, consultamos la documentación
        # o inspeccionamos el objeto job_status.state. Usaremos comparaciones robustas.
        # Ejemplo de cómo podrías ver los estados posibles (requiere inspección):
        # from google.ai.generativelanguage_v1beta.types import TuningJob
        # print(TuningJob.State)

        current_state_str = str(job_status.state).upper() # Convertir a mayúsculas para comparación

        if "SUCCEEDED" in current_state_str:
            print(f"¡Éxito! El trabajo de ajuste '{job_name}' se completó correctamente.")
            # Actualizamos nuestra variable local con el estado final del trabajo
            tuning_job = job_status
            break # Salimos del bucle de espera

        elif "FAILED" in current_state_str:
            print(f"Error: El trabajo de ajuste '{job_name}' falló.")
            # Puedes intentar imprimir más detalles si están disponibles
            if hasattr(job_status, 'error') and job_status.error:
                 print(f"  Detalles del error: {job_status.error}")
            tuning_job = None # Marcamos que no hay modelo resultante
            break # Salimos del bucle de espera

        elif "CANCELLED" in current_state_str or "EXPIRED" in current_state_str :
             print(f"Advertencia: El trabajo de ajuste '{job_name}' fue {current_state_str.lower()}.")
             tuning_job = None
             break

        else:
            # Si no está terminado (SUCCEEDED, FAILED, CANCELLED, EXPIRED), asumimos que sigue en progreso (RUNNING, etc.)
            print(f"Estado actual del trabajo '{job_name}': {job_status.state}. Esperando 60 segundos...")
            time.sleep(60) # Esperamos 60 segundos antes de volver a consultar

    except Exception as e:
        print(f"Error al intentar obtener el estado del trabajo: {e}")
        print("Esperando 60 segundos antes de reintentar...")
        time.sleep(60)


# 8. Generación de Contenido con el Modelo Ajustado (SI EL TRABAJO TUVO ÉXITO)
# Verificamos si tuning_job no es None y si tiene la información del modelo ajustado
if tuning_job and hasattr(tuning_job, 'tuned_model') and tuning_job.tuned_model:
    print("\nGenerando contenido con el modelo ajustado...")
    try:
        # Extraemos el nombre/identificador del modelo ajustado del objeto del trabajo
        tuned_model_name = tuning_job.tuned_model.model

        print(f"Usando el modelo ajustado: {tuned_model_name}")

        response = client.models.generate_content(
            model=tuned_model_name,
            contents='III', # La entrada que quieres probar
        )

        print("\nRespuesta del modelo ajustado:")
        print(response.text)

    except Exception as e:
        print(f"\nError al generar contenido con el modelo ajustado: {e}")

else:
    print("\nNo se puede generar contenido porque el trabajo de ajuste fino no finalizó exitosamente o fue cancelado.")

print("\nScript finalizado.")