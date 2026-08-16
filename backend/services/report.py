import os

from reportlab.lib.pagesizes import A4

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)


REPORT_DIR = os.path.join(
    BASE_DIR,
    "reports"
)


def generate_report(
    filename,
    title,
    analysis
):

    os.makedirs(
        REPORT_DIR,
        exist_ok=True
    )

    output_path = os.path.join(
        REPORT_DIR,
        filename
    )

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            title,
            styles["Title"]
        )
    )

    story.append(
        Spacer(
            1,
            20
        )
    )

    formatted_analysis = (
        analysis
        .replace(
            "&",
            "&amp;"
        )
        .replace(
            "<",
            "&lt;"
        )
        .replace(
            ">",
            "&gt;"
        )
        .replace(
            "\n",
            "<br/>"
        )
    )

    story.append(
        Paragraph(
            formatted_analysis,
            styles["BodyText"]
        )
    )

    document.build(
        story
    )

    return output_path