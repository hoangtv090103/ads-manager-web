from flask import request, jsonify, send_file
from controllers.base_controller import BaseController
from models.website_report import WebsiteReport
from io import BytesIO


class WebsiteReportController(BaseController):
    def get(self):
        try:
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            publisher_email = request.args.get('publisher_email')
            export = request.args.get('export', type=bool)

            report_data = WebsiteReport.get_report(
                start_date=start_date,
                end_date=end_date,
                publisher_email=publisher_email
            )

            if export:
                # Tạo file Excel
                wb = WebsiteReport.generate_excel_report(report_data, start_date, end_date)
                
                # Lưu vào buffer
                excel_file = BytesIO()
                wb.save(excel_file)
                excel_file.seek(0)

                # Trả về file Excel
                return send_file(
                    excel_file,
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name=f'website_report_{start_date}_{end_date}.xlsx'
                )

            return jsonify({
                "success": True,
                "data": report_data
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            })
