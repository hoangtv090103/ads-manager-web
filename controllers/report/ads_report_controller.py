from flask import request, jsonify, make_response
from controllers.base_controller import BaseController
from models.ads_report import AdsReport
from io import BytesIO
from datetime import datetime


class AdsReportController(BaseController):
    def post(self):
        try:
            data = request.get_json()
            ad_ids = data.get('ad_ids', [])
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            # Validate required fields
            if not ad_ids:
                return jsonify({
                    "success": False,
                    "error": "Vui lòng chọn ít nhất một tin quảng cáo"
                }), 400

            if not start_date or not end_date:
                return jsonify({
                    "success": False,
                    "error": "Vui lòng chọn khoảng thời gian báo cáo"
                }), 400

            # Validate dates
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                
                if start_date_obj > end_date_obj:
                    return jsonify({
                        "success": False,
                        "error": "Ngày bắt đầu không thể sau ngày kết thúc"
                    }), 400

                # Format dates for display
                start_date_display = start_date_obj.strftime('%d/%m/%Y')
                end_date_display = end_date_obj.strftime('%d/%m/%Y')
            except ValueError:
                return jsonify({
                    "success": False,
                    "error": "Định dạng ngày không hợp lệ. Sử dụng định dạng YYYY-MM-DD"
                }), 400

            # Get report data
            try:
                report_data = AdsReport.get_report_data(
                    ad_ids=ad_ids,
                    start_date=start_date,
                    end_date=end_date
                )

                if not report_data:
                    return jsonify({
                        "success": False,
                        "error": "Không có dữ liệu cho khoảng thời gian này"
                    }), 404

            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": f"Lỗi khi lấy dữ liệu báo cáo: {str(e)}"
                }), 500

            # Generate Excel file
            try:
                wb = AdsReport.generate_excel_report(
                    report_data,
                    start_date_display,
                    end_date_display
                )

                # Save to BytesIO
                excel_file = BytesIO()
                wb.save(excel_file)
                excel_file.seek(0)

                # Generate filename with Vietnamese encoding
                filename = f"Bao_cao_tin_quang_cao_{start_date_display}_den_{end_date_display}.xlsx"
                filename = filename.replace('/', '_')

                # Create response with proper headers
                response = make_response(excel_file.getvalue())
                response.headers.set(
                    'Content-Type', 
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response.headers.set(
                    'Content-Disposition', 
                    f'attachment; filename="{filename}"; filename*=UTF-8\'\'{filename}'
                )
                response.headers.set('Content-Length', len(excel_file.getvalue()))
                response.headers.set('Cache-Control', 'no-cache, no-store, must-revalidate')
                response.headers.set('Pragma', 'no-cache')
                response.headers.set('Expires', '0')
                response.headers.set('X-Content-Type-Options', 'nosniff')

                return response

            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": f"Lỗi khi tạo file Excel: {str(e)}"
                }), 500

        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Lỗi hệ thống: {str(e)}"
            }), 500