from google import genai
from google.genai import types
import time

client = genai.Client(api_key="AIzaSyDn9rLwtZX8rwTA004lC0oWPsSJvJeIEe4")

for model_info in client.tunings.list():
    print(model_info.name)