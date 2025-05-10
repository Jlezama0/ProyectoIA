from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import vertexai
import os
from vertexai.generative_models import GenerativeModel
from vertexai.tuning import sft

creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if not creds_json:
    raise RuntimeError("No se encontró GOOGLE_APPLICATION_CREDENTIALS_JSON en el entorno.")

creds_path = '/tmp/chatbotempresarial-28c80ef20f19.json'
with open(creds_path, "w") as f:
    f.write(creds_json)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path

# Inicializamos Vertex AI
project_id = "348338715521"  # ID del proyecto
region = "us-central1"  # Región donde está el trabajo de ajuste
tuning_job_id = "7050482678046392320"  # El ID del modelo ajustado

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