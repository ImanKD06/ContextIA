import json
import os
import subprocess

from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not database_url:
    raise ValueError("DATABASE_URL no está en .env")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY no está en .env")

environment = {
    "Variables": {
        "DATABASE_URL": database_url,
        "GEMINI_API_KEY": gemini_api_key,
    }
}

subprocess.run(
    [
        "aws",
        "lambda",
        "update-function-configuration",
        "--function-name",
        "contextia-api",
        "--region",
        "eu-west-1",
        "--environment",
        json.dumps(environment),
    ],
    check=True,
)

print("Variables de entorno configuradas correctamente.")