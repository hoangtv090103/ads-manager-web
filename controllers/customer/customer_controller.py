from flask import request, jsonify
from controllers.base_controller import BaseController
from models.customer import Customer

class CustomerController(BaseController):
    def get(self, customer_id=None):
        try:
            if customer_id:
                customer = Customer.get_by_id(customer_id)
                if not customer:
                    return jsonify({"error": "Customer not found"}), 404
                return jsonify({"customer": customer})
            
            customers = Customer.get_all()
            return jsonify({"customers": customers})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def post(self):
        try:
            data = request.json
            required_fields = ['ho_va_ten', 'user_id', 'email_doanh_nghiep']
            
            # Validate required fields
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400

            customer = Customer(**data)
            customer.save()
            return jsonify({
                "message": "Customer created successfully",
                "customer_id": customer.customer_id
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def put(self, customer_id):
        try:
            data = request.json
            customer = Customer.get_by_id(customer_id)
            if not customer:
                return jsonify({"error": "Customer not found"}), 404
            
            for key, value in data.items():
                setattr(customer, key, value)
            customer.update()
            
            return jsonify({"message": "Customer updated successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete(self, customer_id):
        try:
            Customer.delete_by_id(customer_id)
            return jsonify({"message": "Customer deleted successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500 