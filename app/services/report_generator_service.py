import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)


def generate_pdf_report(
    proposal: dict,
    output_dir: str = "generated_reports"
):
    """
    Genera un informe PDF a partir de una propuesta
    generada por ContextIA.
    """

    os.makedirs(output_dir, exist_ok=True)

    pdf_path = os.path.join(
        output_dir,
        "informe_contextia.pdf"
    )

    document = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    content = []


    content.append(
        Paragraph(
            "CONTEXTIA",
            title_style
        )
    )

    content.append(
        Paragraph(
            "INFORME DE ANÁLISIS DOCUMENTAL",
            heading_style
        )
    )

    content.append(
        Spacer(1, 20)
    )

    for section in proposal.get("sections", []):

        title = section.get(
            "title",
            "Sección"
        )

        section_content = section.get(
            "content",
            []
        )

        content.append(
            Paragraph(
                title,
                heading_style
            )
        )

        for item in section_content:

            content.append(
                Paragraph(
                    f"• {item}",
                    normal_style
                )
            )

        content.append(
            Spacer(1, 15)
        )

   

    generated_charts = proposal.get(
        "generated_charts",
        []
    )

    if generated_charts:

        content.append(
            Paragraph(
                "Gráficos",
                heading_style
            )
        )

        content.append(
            Spacer(1, 10)
        )

    for chart in generated_charts:

        chart_path = chart["url"].lstrip("/")

        if os.path.exists(chart_path):

            content.append(
                Paragraph(
                    chart["title"],
                    heading_style
                )
            )

            image = Image(
                chart_path,
                width=16 * cm,
                height=10 * cm
            )

            content.append(
                image
            )

            content.append(
                Spacer(1, 15)
            )


    content.append(
        Paragraph(
            "Fuentes utilizadas",
            heading_style
        )
    )

    for source in proposal.get(
    "sources",
    []
    ):

        content.append(
            Paragraph(
                f"Documento: {source['document_title']}",
                normal_style
            )
        )

    document.build(content)

    return pdf_path