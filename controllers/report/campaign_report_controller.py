from flask import request, jsonify, make_response
from controllers.base_controller import BaseController
from models.campaign_report import CampaignReport
from io import BytesIO
from datetime import datetime


class CampaignReportController(BaseController):
    def post(self):
        try:
            data = request.get_json()
            campaign_ids = data.get('campaign_ids', [])
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            # Validate required fields
            if not campaign_ids:
                return jsonify({
                    "success": False,
                    "error": "Campaign IDs are required"
                }), 400

            if not start_date or not end_date:
                return jsonify({
                    "success": False,
                    "error": "Start date and end date are required"
                }), 400

            # Validate dates
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                
                # Format dates for display
                start_date_display = start_date_obj.strftime('%d/%m/%Y')
                end_date_display = end_date_obj.strftime('%d/%m/%Y')
            except ValueError:
                return jsonify({
                    "success": False,
                    "error": "Invalid date format. Use YYYY-MM-DD"
                }), 400

            # Get report data
            report_data = CampaignReport.get_report_data(
                campaign_ids=campaign_ids,
                start_date=start_date,
                end_date=end_date
            )

            # Generate Excel file
            wb = CampaignReport.generate_excel_report(
                report_data,
                start_date_display,
                end_date_display
            )

            # Save to BytesIO
            excel_file = BytesIO()
            wb.save(excel_file)
            excel_file.seek(0)

            # Generate filename
            filename = f"Báo cáo chiến dịch ({start_date_display} đến {end_date_display}).xlsx"

            # Create response
            response = make_response(excel_file.getvalue())
            response.headers.set('Content-Type', 
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response.headers.set('Content-Disposition', 
                f'attachment; filename="{filename}"')
            response.headers.set('Content-Length', len(excel_file.getvalue()))
            response.headers.set('Cache-Control', 'no-cache')
            response.headers.set('X-Content-Type-Options', 'nosniff')

            return response

        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500 