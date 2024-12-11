from flask import request, jsonify, send_file, make_response
from controllers.base_controller import BaseController
from models.website_report import WebsiteReport
from io import BytesIO
from datetime import datetime


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
                
                # Tạo BytesIO object và lưu workbook
                excel_file = BytesIO()
                wb.save(excel_file)
                excel_file.seek(0)

                # Tạo response với headers cụ thể
                response = make_response(excel_file.getvalue())
                response.headers.set('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response.headers.set('Content-Disposition', 'attachment; filename=website_report.xlsx')
                
                # Thêm headers để tránh cache và xác định content length
                response.headers.set('Content-Length', len(excel_file.getvalue()))
                response.headers.set('Cache-Control', 'no-cache')
                response.headers.set('X-Content-Type-Options', 'nosniff')
                
                return response

            return jsonify({
                "success": True,
                "data": report_data
            })
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            })
