class Transaction:
    @staticmethod
    def get_dashboard_stats():
        """Get transaction statistics for dashboard"""
        return {
            'total_budget': 100000000,
            'transactions_today': 10,
            'total_amount_today': 20000000
        } 