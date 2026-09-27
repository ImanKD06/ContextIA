import os
import re

import matplotlib.pyplot as plt


def create_filename(title: str) -> str:
    """
    Convierte el título del gráfico en un nombre de archivo seguro.
    """

    filename = title.lower()

    filename = re.sub(
        r"[^a-z0-9áéíóúüñ]+",
        "_",
        filename
    )

    filename = filename.strip("_")

    return f"{filename}.png"


def generate_chart(
    title: str,
    chart_type: str,
    data: list[dict],
    output_dir: str = "generated_reports"
):
    """
    Genera automáticamente un gráfico a partir de los datos
    proporcionados por Gemini.
    """

    os.makedirs(output_dir, exist_ok=True)

    labels = [
        item["label"]
        for item in data
    ]

    values = [
        item["value"]
        for item in data
    ]

    filename = create_filename(title)

    output_path = os.path.join(
        output_dir,
        filename
    )

    if chart_type == "pie":

        plt.figure(figsize=(8, 6))

        plt.pie(
            values,
            labels=labels,
            autopct="%1.1f%%"
        )

        plt.title(title)

    elif chart_type in ["bar", "comparison"]:

        plt.figure(figsize=(8, 6))

        plt.bar(
            labels,
            values
        )

        plt.title(title)

        plt.ylabel("Valor")

        plt.xticks(
            rotation=20,
            ha="right"
        )

    else:

        raise ValueError(
            f"Tipo de gráfico no soportado: {chart_type}"
        )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    return output_path


def generate_charts(
    charts: list[dict],
    output_dir: str = "generated_reports"
):
    """
    Genera automáticamente todos los gráficos
    definidos en la respuesta de Gemini.
    """

    generated_files = []

    for chart in charts:

        file_path = generate_chart(
            title=chart["title"],
            chart_type=chart["chart_type"],
            data=chart["data"],
            output_dir=output_dir
        )

        filename = os.path.basename(file_path)

        generated_files.append({
            "title": chart["title"],
            "chart_type": chart["chart_type"],
            "url": f"/generated_reports/{filename}"
        })

    return generated_files