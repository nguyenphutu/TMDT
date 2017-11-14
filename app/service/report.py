import os
import pdfkit
from app import app
from flask import render_template

# http://wkhtmltopdf.org/index.html
class ReportService():
    def __init__(self):
        self.config = pdfkit.configuration(
            wkhtmltopdf=app.config['WKHTMLTOPDF_BIN_PATH']
        )

    def to_pdf(self, template='test.html', output='report.pdf', context=None):
        options = {
            'page-size': 'A4',
            # 'margin-top': '0mm',
            # 'margin-right': '0mm',
            # 'margin-left': '0mm',
            # 'margin-bottom': '0mm',
            'zoom': '1',
            'encoding': "UTF-8",
            # 'orientation': "Landscape",
            # 'debug-javascript': 1,
            'load-error-handling': 'ignore',
            'window-status': 'done',
            # 'javascript-delay': 3000,
        }

        # html = render_template(template, **context)
        html = render_template(template)
        output_path = os.path.join(app.config['PDF_DIR_PATH'], output)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        import pdb;pdb.set_trace()
        pdf = pdfkit.from_string(
            html,
            options=options,
            configuration=self.config,
            output_path=output_path)

        if pdf:
            return output_path
        raise Exception('failed to generate pdf')

