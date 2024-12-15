from flask import Blueprint, request, jsonify
from flask_restful import Resource
from models.ads import Ads
from models.ads_ecom import AdsEcom
from models.ads_format import AdsFormat
from configs.db import get_db_connection
from controllers.base_controller import BaseController


class AdsEcomController(BaseController):
    def post(self):
        conn = None
        try:
            data = request.form.to_dict()
            files = request.files

            # Validate required fields
            required_fields = ['ten_tin_quang_cao', 'format_id', 'ads_group_id']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        'status': 'error',
                        'message': f'Missing required field: {field}'
                    }), 400

            # Start transaction
            conn = get_db_connection()
            conn.autocommit = False
            cursor = conn.cursor()

            try:
                # Create base Ads record
                cursor.execute("""
                    INSERT INTO ads (ads_group_id, ads_status_id, ten_tin_quang_cao, URL_dich)
                    VALUES (%s, %s, %s, %s)
                    RETURNING ads_id
                """, (
                    data.get('ads_group_id'),
                    1,  # Default status
                    data.get('ten_tin_quang_cao'),
                    data.get('URL_dich', '')
                ))
                ads_id = cursor.fetchone()[0]

                # Handle file uploads
                anh_banner_chan_trang = None
                video_banner = None
                anh_thumbnail = None

                if 'anh_banner_chan_trang' in files:
                    anh_banner_chan_trang = files['anh_banner_chan_trang'].read()

                if 'video_banner' in files:
                    video_banner = files['video_banner'].read()

                if 'anh_thumbnail' in files:
                    anh_thumbnail = files['anh_thumbnail'].read()

                # Create AdsEcom record
                cursor.execute("""
                    INSERT INTO ads_ecom (
                        ads_id, format_id, anh_banner_chan_trang, video_banner,
                        anh_thumbnail, su_dung_mau_banner_co_san, ten_san_pham,
                        hien_thi_gia_khuyen_mai, hien_thi_freeship_sp
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING ads_id
                """, (
                    ads_id,
                    data.get('format_id'),
                    anh_banner_chan_trang,
                    video_banner,
                    anh_thumbnail,
                    data.get('su_dung_mau_banner_co_san', 'false').lower() == 'true',
                    data.get('ten_san_pham', ''),
                    data.get('hien_thi_gia_khuyen_mai', 'false').lower() == 'true',
                    data.get('hien_thi_freeship_sp', 'false').lower() == 'true'
                ))

                # Commit transaction
                conn.commit()

                return jsonify({
                    'status': 'success',
                    'message': 'Tạo tin quảng cáo thành công',
                    'data': {
                        'ads_id': ads_id
                    }
                }), 201

            except Exception as e:
                conn.rollback()
                raise e

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
        finally:
            if conn:
                conn.close()

    def get(self, ads_id=None):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()

                if ads_id:
                    # Get specific ad
                    cursor.execute("""
                        SELECT 
                            a.ads_id,
                            a.ten_tin_quang_cao,
                            a.URL_dich,
                            ae.format_id,
                            ae.su_dung_mau_banner_co_san,
                            ae.ten_san_pham,
                            ae.hien_thi_gia_khuyen_mai,
                            ae.hien_thi_freeship_sp,
                            af.format_name,
                            a.created_at,
                            a.active
                        FROM ads a
                        JOIN ads_ecom ae ON a.ads_id = ae.ads_id
                        JOIN ads_format af ON ae.format_id = af.format_id
                        WHERE a.ads_id = %s AND a.active = TRUE
                    """, (ads_id,))
                    row = cursor.fetchone()
                    
                    if not row:
                        return jsonify({
                            'status': 'error',
                            'message': 'Không tìm thấy tin quảng cáo'
                        }), 404

                    ad_data = {
                        'ads_id': row[0],
                        'ten_tin_quang_cao': row[1],
                        'URL_dich': row[2],
                        'format_id': row[3],
                        'su_dung_mau_banner_co_san': row[4],
                        'ten_san_pham': row[5],
                        'hien_thi_gia_khuyen_mai': row[6],
                        'hien_thi_freeship_sp': row[7],
                        'format_name': row[8],
                        'created_at': row[9].strftime('%d/%m/%Y') if row[9] else None,
                        'active': row[10]
                    }

                    return jsonify({
                        'status': 'success',
                        'data': ad_data
                    })
                else:
                    # Get all ads
                    cursor.execute("""
                        SELECT 
                            a.ads_id,
                            a.ten_tin_quang_cao,
                            a.URL_dich,
                            ae.format_id,
                            ae.su_dung_mau_banner_co_san,
                            ae.ten_san_pham,
                            ae.hien_thi_gia_khuyen_mai,
                            ae.hien_thi_freeship_sp,
                            af.format_name,
                            a.created_at,
                            a.active
                        FROM ads a
                        JOIN ads_ecom ae ON a.ads_id = ae.ads_id
                        JOIN ads_format af ON ae.format_id = af.format_id
                        WHERE a.active = TRUE
                        ORDER BY a.created_at DESC
                    """)
                    
                    ads_list = []
                    for row in cursor.fetchall():
                        ads_list.append({
                            'ads_id': row[0],
                            'ten_tin_quang_cao': row[1],
                            'URL_dich': row[2],
                            'format_id': row[3],
                            'su_dung_mau_banner_co_san': row[4],
                            'ten_san_pham': row[5],
                            'hien_thi_gia_khuyen_mai': row[6],
                            'hien_thi_freeship_sp': row[7],
                            'format_name': row[8],
                            'created_at': row[9].strftime('%d/%m/%Y') if row[9] else None,
                            'active': row[10]
                        })

                    return jsonify({
                        'status': 'success',
                        'data': ads_list
                    })

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    def put(self, ads_id):
        conn = None
        try:
            data = request.form.to_dict()
            files = request.files

            # Start transaction
            conn = get_db_connection()
            conn.autocommit = False
            cursor = conn.cursor()

            try:
                # Update base Ads record
                if 'ten_tin_quang_cao' in data or 'URL_dich' in data:
                    update_fields = []
                    update_values = []
                    
                    if 'ten_tin_quang_cao' in data:
                        update_fields.append("ten_tin_quang_cao = %s")
                        update_values.append(data['ten_tin_quang_cao'])
                    
                    if 'URL_dich' in data:
                        update_fields.append("URL_dich = %s")
                        update_values.append(data['URL_dich'])
                    
                    update_values.append(ads_id)
                    
                    cursor.execute(f"""
                        UPDATE ads 
                        SET {', '.join(update_fields)},
                            updated_at = CURRENT_TIMESTAMP
                        WHERE ads_id = %s
                    """, update_values)

                # Update AdsEcom record
                update_fields = []
                update_values = []

                # Handle file updates
                if 'anh_banner_chan_trang' in files:
                    update_fields.append("anh_banner_chan_trang = %s")
                    update_values.append(files['anh_banner_chan_trang'].read())

                if 'video_banner' in files:
                    update_fields.append("video_banner = %s")
                    update_values.append(files['video_banner'].read())

                if 'anh_thumbnail' in files:
                    update_fields.append("anh_thumbnail = %s")
                    update_values.append(files['anh_thumbnail'].read())

                # Handle other fields
                field_mappings = {
                    'su_dung_mau_banner_co_san': 'boolean',
                    'ten_san_pham': 'string',
                    'hien_thi_gia_khuyen_mai': 'boolean',
                    'hien_thi_freeship_sp': 'boolean'
                }

                for field, field_type in field_mappings.items():
                    if field in data:
                        update_fields.append(f"{field} = %s")
                        if field_type == 'boolean':
                            update_values.append(data[field].lower() == 'true')
                        else:
                            update_values.append(data[field])

                if update_fields:
                    update_values.append(ads_id)
                    cursor.execute(f"""
                        UPDATE ads_ecom 
                        SET {', '.join(update_fields)},
                            updated_at = CURRENT_TIMESTAMP
                        WHERE ads_id = %s
                    """, update_values)

                # Commit transaction
                conn.commit()

                return jsonify({
                    'status': 'success',
                    'message': 'Cập nhật tin quảng cáo thành công'
                })

            except Exception as e:
                conn.rollback()
                raise e

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
        finally:
            if conn:
                conn.close()

    def delete(self, ads_id):
        conn = None
        try:
            conn = get_db_connection()
            conn.autocommit = False
            cursor = conn.cursor()

            try:
                # Soft delete the ads record
                cursor.execute("""
                    UPDATE ads 
                    SET active = FALSE,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE ads_id = %s
                """, (ads_id,))

                # Soft delete the ads_ecom record
                cursor.execute("""
                    UPDATE ads_ecom 
                    SET active = FALSE,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE ads_id = %s
                """, (ads_id,))

                conn.commit()

                return jsonify({
                    'status': 'success',
                    'message': 'Xóa tin quảng cáo thành công'
                })

            except Exception as e:
                conn.rollback()
                raise e

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
        finally:
            if conn:
                conn.close()