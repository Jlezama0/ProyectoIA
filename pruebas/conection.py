from vertexai.generative_models import GenerativeModel
from vertexai.tuning import sft

# Reemplaza con tu ID de proyecto, región y ID de trabajo de ajuste
project_id = "348338715521"  # Tu ID de proyecto
region = "us-central1"  # Región donde está el trabajo de ajuste
tuning_job_id = "7050482678046392320"  # El ID del trabajo de ajuste que encontraste

# Crea el objeto de trabajo de ajuste supervisado
sft_tuning_job = sft.SupervisedTuningJob(f"projects/{project_id}/locations/{region}/tuningJobs/{tuning_job_id}")

# Obtén el endpoint del modelo ajustado
tuned_model = GenerativeModel(sft_tuning_job.tuned_model_endpoint_name)

# La variable `content` debe ser la entrada que deseas pasar al modelo para generar la respuesta
content = "Hola Grammi"  # Puedes poner cualquier contenido aquí

# Genera la respuesta
response = tuned_model.generate_content(content)

print(response)
