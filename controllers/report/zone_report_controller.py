from flask import request, jsonify, make_response
from controllers.base_controller import BaseController
from models.zone_report import ZoneReport
from io import BytesIO
from datetime import datetime


class ZoneReportController(BaseController):
    def get(self):
        try:
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            website_id = request.args.get('website_id')
            zone_id = request.args.get('zone_id')
            export = request.args.get('export', type=bool)

            # Validate dates
            if start_date and end_date:
                try:
                    datetime.strptime(start_date, '%Y-%m-%d')
                    datetime.strptime(end_date, '%Y-%m-%d')
                except ValueError:
                    return jsonify({
                        "success": False,
                        "error": "Invalid date format. Use YYYY-MM-DD"
                    })

            report_data = ZoneReport.get_report(
                start_date=start_date,
                end_date=end_date,
                website_id=website_id,
                zone_id=zone_id
            )

            if export:
                # Generate Excel file
                wb = ZoneReport.generate_excel_report(
                    report_data, 
                    start_date or 'all', 
                    end_date or 'all'
                )
                
                # Save to BytesIO
                excel_file = BytesIO()
                wb.save(excel_file)size
                excel_file.seek(0)

                # Generate filename
                filename = f"zone_report_{start_date or 'all'}_{end_date or 'all'}.xlsx"

                response = make_response(excel_file.getvalue())
                response.headers.set('Content-Type', 
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response.headers.set('Content-Disposition', 
                    f'attachment; filename="{filename}"')
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