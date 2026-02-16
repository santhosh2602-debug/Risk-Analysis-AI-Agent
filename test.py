from google import genai
from app.config import settings

# 1. Setup the Client (This replaces genai.configure)
client = genai.Client(api_key=settings.google_api_key)

# 2. List models through the client instance
print("Models supporting generateContent:")
for m in client.models.list():
    # In the new SDK, 'supported_actions' replaces 'supported_generation_methods'
    if "generateContent" in m.supported_actions:
        print(f" - {m.name}")