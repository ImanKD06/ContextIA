ContextIA

ContextIA es una plataforma backend para análisis documental mediante RAG (Retrieval-Augmented Generation). Permite procesar documentos, realizar búsquedas semánticas sobre su contenido y utilizar un modelo de IA para generar respuestas y propuestas contextualizadas.

Además, el sistema puede generar gráficos e informes PDF a partir de los resultados obtenidos.

Arquitectura

Documentos
    ↓
Procesamiento y fragmentación (chunks)
    ↓
Generación de embeddings
    ↓
PostgreSQL + pgvector
    ↓
Búsqueda semántica
    ↓
Contexto relevante
    ↓
Google Gemini
    ↓
Respuesta estructurada
    ↓
┌───────────────┬────────────────┐
│               │                │
Gráficos       Informe PDF       API
│               │
└───────┬───────┘
        ↓
   Amazon S3

La arquitectura está organizada por responsabilidades para separar la lógica de API, acceso a datos, búsqueda vectorial, integración con IA, generación de informes y almacenamiento.

Tecnologías

Backend

Python 3.13

FastAPI

SQLAlchemy

Pydantic

Inteligencia artificial

Google Gemini

Embeddings

RAG (Retrieval-Augmented Generation)

Base de datos

PostgreSQL

Supabase

pgvector

Archivos y generación de informes

ReportLab para generación de PDF

python-multipart para recepción de archivos mediante FastAPI

Amazon S3 para almacenamiento

Infraestructura

AWS Lambda

AWS SAM

Docker

Desarrollo

Git

GitHub

Pytest

Funcionamiento del RAG

Cuando el usuario realiza una consulta, ContextIA no envía directamente la pregunta al modelo generativo.

Primero se genera un embedding de la consulta:

Pregunta del usuario
        ↓
Embedding
        ↓
Búsqueda vectorial
        ↓
Chunks relevantes

Los fragmentos recuperados se utilizan posteriormente para construir el contexto que recibe Gemini:

Pregunta
   +
Contexto recuperado
   ↓
Google Gemini
   ↓
Respuesta

Esto permite generar respuestas basadas en la documentación proporcionada por el usuario.

Estructura del proyecto

Una estructura simplificada del backend es:

app/
├── core/
│   └── database.py
│
├── models/
│   ├── document.py
│   └── chunk.py
│
├── schemas/
│   └── proposal.py
│
├── routers/
│   ├── chat.py
│   └── proposals.py
│
├── services/
│   ├── embedding_service.py
│   ├── vector_service.py
│   ├── llm_service.py
│   ├── proposal_service.py
│   ├── report_service.py
│   ├── report_generator_service.py
│   └── s3_service.py
│
└── main.py

tests/

La estructura puede variar según la versión actual del proyecto.

Componentes principales

FastAPI

FastAPI expone la API REST y gestiona las peticiones del frontend.

Entre los endpoints principales se encuentran:

POST /chat
POST /proposals

SQLAlchemy

SQLAlchemy se utiliza como ORM para trabajar con PostgreSQL y representar las entidades de la aplicación mediante modelos Python.

Supabase + PostgreSQL

Supabase proporciona la infraestructura de PostgreSQL utilizada por ContextIA.

La base de datos almacena los documentos y sus fragmentos de texto.

pgvector

pgvector permite almacenar embeddings dentro de PostgreSQL y realizar búsquedas por similitud vectorial.

Los chunks contienen un embedding que permite relacionarlos semánticamente con las consultas del usuario.

Google Gemini

Gemini se utiliza como modelo generativo.

El backend le proporciona:

La petición del usuario.

Los fragmentos recuperados.

Las instrucciones necesarias para generar una respuesta estructurada.

En determinadas funcionalidades, Gemini también devuelve información estructurada para la generación posterior de gráficos e informes.

Generación de gráficos

Los resultados estructurados obtenidos del modelo pueden utilizarse para generar gráficos mediante Python.

El modelo determina la información que debe representarse y el backend procesa esos datos para crear los recursos correspondientes.

Generación de PDF

Los informes se generan mediante ReportLab.

El flujo es:

Resultado de Gemini
        ↓
Datos estructurados
        ↓
Generador de informes
        ↓
PDF

Amazon S3

Los archivos generados, como los informes PDF, se almacenan en Amazon S3.

El servicio s3_service.py se encarga de la comunicación con S3.

AWS Lambda

El backend puede desplegarse como una función serverless mediante AWS Lambda.

Docker

Docker se utiliza para empaquetar la aplicación junto con sus dependencias y facilitar un entorno reproducible para el despliegue.

Variables de entorno

Las credenciales y configuraciones sensibles no deben almacenarse directamente en el código.

Ejemplo:

DATABASE_URL=
GEMINI_API_KEY=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
S3_BUCKET_NAME=

Utiliza un archivo .env en desarrollo y asegúrate de que no se suba al repositorio.

Instalación

Clona el repositorio:

git clone <URL_DEL_REPOSITORIO>
cd ContextIA

Crea un entorno virtual:

python -m venv .venv

En Windows:

.venv\Scripts\activate

Instala las dependencias:

pip install -r requirements.txt

Configura las variables de entorno necesarias y prepara la base de datos PostgreSQL/Supabase con pgvector.

Ejecución local

uvicorn app.main:app --reload


Testing

El proyecto utiliza Pytest.

python -m pytest

Para ejecutar un archivo concreto:

python -m pytest tests/test_proposal_service.py -v

Despliegue

El proyecto está preparado para despliegue mediante AWS SAM y AWS Lambda.

Código
   ↓
Docker / SAM Build
   ↓
AWS SAM
   ↓
AWS Lambda
   ↓
API

Los informes generados pueden almacenarse en Amazon S3.

Seguridad

Antes de realizar un despliegue se debe comprobar:

Que las API keys no estén en Git.

Que .env esté incluido en .gitignore.

Que las credenciales de AWS no estén hardcodeadas.

Que los endpoints validen correctamente los datos recibidos.

Objetivos técnicos

Este proyecto permite trabajar conceptos de:

Arquitectura backend modular.

APIs REST.

RAG.

Búsqueda semántica.

Embeddings.

Bases de datos vectoriales.

Integración de LLMs.

Generación de contenido estructurado.

Generación automática de gráficos.

Generación de informes PDF.

Almacenamiento cloud.

Serverless.

Docker.

Testing.

Integración de servicios externos.
