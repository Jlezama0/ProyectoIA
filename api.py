from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import vertexai
import os
from vertexai.generative_models import GenerativeModel
from vertexai.tuning import sft

# Definir la variable de entorno para que Vertex AI la use automáticamente
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\juanp\inteArtificial\chatbotempresarial-28c80ef20f19.json"

project_id = "348338715521"  # ID del proyecto
region = "us-central1"  # Región donde está el trabajo de ajuste
tuning_job_id = "7050482678046392320"  # El ID del modelo ajustado

# Iniciar vertex AI
vertexai.init(project=project_id, location=region)

# Se crea el objeto de trabajo de ajuste supervisado
sft_tuning_job = sft.SupervisedTuningJob(f"projects/{project_id}/locations/{region}/tuningJobs/{tuning_job_id}")

# Se obtiene el endpoint del modelo ajustado
tuned_model = GenerativeModel(sft_tuning_job.tuned_model_endpoint_name)

app = FastAPI()

class promptRequest(BaseModel):
    prompt : str

@app.post("/Grammi")
def generate_text(request: promptRequest):
    try: 
        response = tuned_model.generate_content(request.prompt)
        return{"Grammi": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))