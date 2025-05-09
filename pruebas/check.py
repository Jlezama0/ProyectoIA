from google import genai
from google.genai import types
import time

client = genai.Client(api_key="api")

for model_info in client.tunings.list():
    print(model_info.name)  