from flask import jsonify, request
from controllers.base_controller import BaseController
from models.ads import Ads
from datetime import datetime, timedelta
import random

class AdsController(BaseController):
    def get(self):
        try:
            # Mock data for ads list
            mock_ads = []
            campaign_types = ['Ecommerce', 'Display Ads', 'Native Ads']
            statuses = ['Đang chạy', 'Tạm dừng', 'Hoàn thành', 'Chưa chạy', 'Lỗi']
            ad_zones = ['Header Banner', 'Sidebar Right', 'In-feed Ads', 'Footer Banner', 'Pop-up Ads']

            for i in range(1, 21):  # Generate 20 mock ads
                views = random.randint(1000, 100000)
                clicks = random.randint(100, views//10)
                ctr = (clicks / views * 100) if views > 0 else 0
                cost = random.randint(500000, 10000000)
                purchases = random.randint(0, clicks//10)
                conversion_rate = (purchases / clicks * 100) if clicks > 0 else 0
                
                mock_ad = {
                    "ads_id": i,
                    "ten_tin_quang_cao": f"Quảng cáo mẫu {i}",
                    "ten_chien_dich": f"Chiến dịch {(i-1)//5 + 1}",
                    "ten_nhom": f"Nhóm quảng cáo {(i-1)//3 + 1}",
                    "dinh_dang": random.choice(campaign_types),
                    "url_dich": f"https://example.com/landing-page-{i}",
                    "trang_thai": random.choice(statuses),
                    "dang_hien_thi": random.choice([True, False]),
                    "tong_chi_phi": cost,
                    "luot_xem": views,
                    "luot_nhan": clicks,
                    "ctr": round(ctr, 2),
                    "cpc": round(cost/clicks if clicks > 0 else 0),
                    "cpm": round(cost*1000/views if views > 0 else 0),
                    "so_luong_mua_hang": purchases,
                    "ti_le_chuyen_doi": round(conversion_rate, 2),
                    "cps": round(cost/purchases if purchases > 0 else 0),
                    "video_view_3s": random.randint(100, views//2) if random.random() > 0.5 else 0,
                    "ten_vung_quang_cao": random.choice(ad_zones),
                    "loai_quang_cao": random.choice(campaign_types)
                }
                mock_ads.append(mock_ad)

            return jsonify({
                "success": True,
                "ads": mock_ads
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

    def put(self, ads_id):
        try:
            data = request.get_json()
            active = data.get('active')
            
            if active is None:
                return jsonify({
                    "success": False,
                    "error": "Active status is required"
                }), 400

            # Mock successful update
            return jsonify({
                "success": True,
                "message": "Ad status updated successfully"
            })

        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500 