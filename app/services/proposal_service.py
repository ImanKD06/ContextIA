import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY no está configurada")

client = genai.Client(api_key=api_key)


def generate_proposal(
    request: str,
    context: str
):
    prompt = f"""
Analiza la siguiente información documental y responde a la petición
del usuario.

PREGUNTA DEL USUARIO:
{request}

CONTEXTO DOCUMENTAL:
{context}

REGLAS IMPORTANTES:

1. Utiliza exclusivamente la información del CONTEXTO DOCUMENTAL.

2. No inventes datos, porcentajes, cantidades, fechas, requisitos,
   objetivos, resultados ni cifras.

3. Puedes realizar operaciones matemáticas sencillas únicamente cuando
   los datos necesarios estén explícitamente presentes en el contexto.

4. Adapta la estructura del análisis al tipo de documento y a la petición
   del usuario.

5. NO utilices una estructura empresarial por defecto.

6. Si el documento y la petición están relacionados con una empresa,
   negocio, organización o análisis empresarial, utiliza una estructura
   apropiada para ese caso. Por ejemplo:

   - Situación actual
   - Datos relevantes
   - Problemas detectados
   - Objetivos
   - Propuesta de solución
   - Recursos necesarios
   - Impacto esperado

7. Si el documento trata sobre una beca, ayuda o subvención, utiliza
   secciones apropiadas como:

   - Resumen
   - Requisitos
   - Personas beneficiarias
   - Documentación necesaria
   - Cuantía
   - Plazos
   - Procedimiento de solicitud
   - Condiciones
   - Aspectos importantes

8. Si el documento trata sobre un procedimiento administrativo, utiliza
   secciones apropiadas como:

   - Resumen
   - Quién puede realizarlo
   - Requisitos
   - Documentación necesaria
   - Pasos del procedimiento
   - Plazos
   - Costes o tasas
   - Organismo responsable
   - Aspectos importantes

9. Si el documento trata sobre una ley, normativa o reglamento, utiliza
   secciones apropiadas como:

   - Resumen
   - Ámbito de aplicación
   - Derechos
   - Obligaciones
   - Excepciones
   - Plazos
   - Aspectos relevantes

10. Para contratos, informes, documentos académicos u otros documentos,
    crea las secciones que sean más útiles para comprender la información
    y responder a la petición del usuario.

11. No es necesario utilizar todas las secciones de los ejemplos
    anteriores. Selecciona únicamente las que sean relevantes.

12. Las secciones deben aparecer en un orden lógico.

13. Cada sección debe tener un título claro y un contenido formado por
    una lista de elementos.

14. No inventes información para completar una sección. Si una información
    no aparece en el contexto, simplemente no la incluyas.


==================================================
GRÁFICOS
==================================================

15. Genera gráficos únicamente cuando los datos del contexto permitan
    representar una comparación o distribución útil.

16. Busca especialmente estos tipos de gráficos cuando existan datos
    suficientes:

    - Distribuciones porcentuales.
    - Situación actual frente a objetivo.
    - Distribución de costes.
    - Distribución de causas.
    - Comparaciones entre cantidades relevantes.

17. Los gráficos deben utilizar únicamente datos presentes o calculables
    directamente a partir del contexto.

18. Cuando un gráfico de distribución porcentual no incluya todas las
    categorías, puedes calcular una categoría residual mediante:

    100 - suma de los porcentajes conocidos.

    Etiqueta esa categoría como "Otras" u "Otros".

19. Los gráficos de tipo "pie" deben representar una distribución
    completa que sume aproximadamente 100%.

20. No es obligatorio generar gráficos. Si no existen datos suficientes
    o los gráficos no aportan valor, devuelve:

    "charts": []

21. En "charts", "data" SIEMPRE debe ser una lista de objetos.

22. Cada objeto de "data" debe tener exactamente:

    "label"
    "value"

23. "value" debe ser siempre un número.

24. "chart_type" debe ser uno de:

    "bar"
    "pie"
    "comparison"

25. "source_chunk_ids" debe contener únicamente los IDs de los chunks
    utilizados para construir ese gráfico.

26. No inventes IDs de chunks.


==================================================
FORMATO DE RESPUESTA
==================================================

27. Devuelve únicamente un JSON válido.

28. La respuesta debe tener exactamente esta estructura:

{{
    "sections": [
        {{
            "title": "Título de la sección",
            "content": [
                "Contenido de la sección"
            ]
        }}
    ],

    "charts": [
        {{
            "title": "Título del gráfico",
            "chart_type": "bar",
            "description": "Descripción breve del gráfico",
            "data": [
                {{
                    "label": "Categoría",
                    "value": 0
                }}
            ],
            "source_chunk_ids": [
                0
            ]
        }}
    ]
}}

29. No añadas ningún campo adicional.

30. Si no existen datos suficientes para generar gráficos, devuelve:

"charts": []

31. Los IDs utilizados en "source_chunk_ids" deben corresponder
    exclusivamente a los chunks proporcionados en el CONTEXTO DOCUMENTAL.
"""

    print("\n===== PROMPT ENVIADO A GEMINI =====")
    print(prompt)
    print("===== FIN PROMPT =====\n")

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    response_text = response.text.strip()

    print("\n===== RESPUESTA RAW DE GEMINI =====")
    print(response_text)
    print("===== FIN RESPUESTA RAW =====\n")

    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

    return json.loads(response_text)