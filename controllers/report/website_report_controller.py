import datetime
from flask import request, jsonify, send_file
from controllers.base_controller import BaseController
from models.website_report import WebsiteReport
from io import BytesIO
import tempfile
import os
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
                
                # Tạo temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                    wb.save(tmp.name)
                    tmp_path = tmp.name

                # Trả về file Excel
                
                download_name = f'website_report_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'
                if publisher_email:
                    download_name = f'website_report_{publisher_email}.xlsx'
                    
                if start_date and end_date:
                    download_name = f'website_report_{publisher_email}_{start_date}_{end_date}.xlsx'
                    
                return send_file(
                    tmp_path,
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name=download_name
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
        finally:
            # Xóa temporary file sau khi đã gửi
            if export and 'tmp_path' in locals():
                try:
                    os.unlink(tmp_path)
                except:
                    pass
