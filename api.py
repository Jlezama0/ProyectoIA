from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
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
project_id = "348338715521"
region = "us-central1"
tuning_job_id = "7050482678046392320"

vertexai.init(project=project_id, location=region)


try:
    sft_tuning_job = sft.SupervisedTuningJob(f"projects/{project_id}/locations/{region}/tuningJobs/{tuning_job_id}")
    tuned_model = GenerativeModel(sft_tuning_job.tuned_model_endpoint_name)
except Exception as e:
    print(f"Error cargando el modelo: {e}")
    raise RuntimeError("Error cargando el modelo ajustado.")


app = FastAPI()

# 🔥 AÑADIR CORS MIDDLEWARE AQUÍ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class promptRequest(BaseModel):
    prompt: str

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/Grammi")
def generate_text(request: promptRequest):
    try:
        response = tuned_model.generate_content(request.prompt)
        return {"Grammi": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/Grammi2")
async def grammi_route(request: Request):
    data = await request.json()
    print("✅ Recibido:", data)
    return {"echo": data}