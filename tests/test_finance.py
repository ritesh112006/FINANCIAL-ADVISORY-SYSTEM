import unittest
import os
import sys
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app
from database.db import get_db_connection, init_db
from services.seed_data import seed_database
from services.financial_engine import FinancialEngine

class TestFinWiseApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        seed_database()

    def setUp(self):
        self.client = app.test_client()

    def test_dashboard_route(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FinWise', response.data)

    def test_transactions_route(self):
        response = self.client.get('/transactions')
        self.assertEqual(response.status_code, 200)

    def test_add_and_delete_transaction(self):
        payload = {
            "date": "2026-10-15",
            "amount": 1500.0,
            "type": "expense",
            "category": "Dining Out",
            "description": "Test Dinner"
        }
        res_post = self.client.post(
            '/api/transactions',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(res_post.status_code, 200)
        post_data = json.loads(res_post.data)
        self.assertTrue(post_data['success'])
        txn_id = post_data['id']

        res_del = self.client.delete(f'/api/transactions/{txn_id}')
        self.assertEqual(res_del.status_code, 200)
        del_data = json.loads(res_del.data)
        self.assertTrue(del_data['success'])

    def test_invalid_transaction_amount(self):
        payload = {
            "date": "2026-10-15",
            "amount": -500.0,
            "type": "expense",
            "category": "Dining Out",
            "description": "Invalid"
        }
        res = self.client.post(
            '/api/transactions',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_budget_management_api(self):
        payload = {
            "month": "2026-10",
            "category": "Dining Out",
            "limit_amount": 4500.0
        }
        res = self.client.post(
            '/api/budgets',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])

    def test_savings_goal_and_deposit(self):
        payload = {
            "title": "Emergency Car Repair",
            "target_amount": 25000.0,
            "current_amount": 5000.0,
            "target_date": "2026-12-31"
        }
        res_create = self.client.post(
            '/api/savings',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(res_create.status_code, 200)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM savings_goals LIMIT 1")
        row = cursor.fetchone()
        target_goal_id = row['id']
        conn.close()

        deposit_payload = {"amount": 2000.0}
        res_dep = self.client.post(
            f'/api/savings/{target_goal_id}/deposit',
            data=json.dumps(deposit_payload),
            content_type='application/json'
        )
        self.assertEqual(res_dep.status_code, 200)
        data = json.loads(res_dep.data)
        self.assertTrue(data['success'])

    def test_csv_export(self):
        response = self.client.get('/reports/export-csv')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/csv')

    def test_experiments_hub_and_detail(self):
        res_hub = self.client.get('/experiments')
        self.assertEqual(res_hub.status_code, 200)
        for exp_id in range(1, 11):
            res_detail = self.client.get(f'/experiments/{exp_id}')
            self.assertEqual(res_detail.status_code, 200)

    def test_experiment_run_apis(self):
        for exp_id in range(1, 11):
            res = self.client.post(
                f'/api/experiments/run/{exp_id}',
                data=json.dumps({}),
                content_type='application/json'
            )
            self.assertEqual(res.status_code, 200)
            data = json.loads(res.data)
            self.assertTrue(data['success'])

if __name__ == '__main__':
    unittest.main()
