from flask import request, jsonify
from models.transaction import TransactionSystem
from flask_restful import Resource


class TransactionController(Resource):
    def post(self):
        try:
            data = request.json
            transaction = TransactionSystem(**data)
            transaction.create()
            return jsonify({"message": "Transaction created successfully"})
        except Exception as e:
            return jsonify({"error": str(e)})

    def get(self, transaction_id=None):
        try:
            if transaction_id:
                transaction = TransactionSystem.get_by_id(transaction_id)
                return jsonify(transaction)
            transactions = TransactionSystem.get_all()
            return jsonify({"transactions": transactions})
        except Exception as e:
            return jsonify({"error": str(e)})

    def put(self, transaction_id):
        data = request.json
        transaction = TransactionSystem(**data)
        transaction.update(transaction_id)
        return jsonify({"message": "Transaction updated successfully"})

    def delete(self, transaction_id):
        transaction = TransactionSystem(tran_id=transaction_id)
        transaction.delete()
        return jsonify({"message": "Transaction deleted successfully"})
