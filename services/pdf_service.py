from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


class PDFReportGenerator:

    def __init__(
        self,
        filename,
        report_data
    ):

        self.filename = filename
        self.report_data = report_data

    def generate(self):

        pdf = SimpleDocTemplate(
            self.filename
        )

        styles = getSampleStyleSheet()

        content = []

        content.append(
            Paragraph(
                "CareerForge AI Report",
                styles["Title"]
            )
        )

        content.append(
            Spacer(1, 20)
        )

        for key, value in self.report_data.items():

            content.append(
                Paragraph(
                    f"<b>{key}</b>: {value}",
                    styles["Normal"]
                )
            )

            content.append(
                Spacer(1, 10)
            )

        pdf.build(content)

        return self.filename