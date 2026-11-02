import sqlite3
import datetime
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from database.db import get_db_connection

from experiments.experiment01.experiment01_agent import FinancialStateSpace, FinWiseAgentPEAS
from experiments.experiment02.experiment02_expert_system import FinancialExpertSystem
from experiments.experiment03.experiment03_uninformed_search import compare_search_algorithms
from experiments.experiment04.experiment04_informed_search import BudgetAStarOptimizer
from experiments.experiment05.experiment05_adversarial_search import FinancialStressTester
from experiments.experiment06.experiment06_fuzzy_controller import FinancialFuzzyController
from experiments.experiment07.experiment07_mamdani_sugeno import ComparativeFISTester
from experiments.experiment08.experiment08_hybrid_neuro_fuzzy import HybridNeuroFuzzyAdvisor
from experiments.experiment09.experiment09_neural_learning_rules import (
    SupervisedFinancialPerceptron,
    UnsupervisedFinancialCompetitiveLearning
)
from experiments.experiment10.experiment10_language_models import FinancialLanguageModels

STATE_SPACE_AGENT = FinancialStateSpace()
EXPERT_SYSTEM = FinancialExpertSystem()
FUZZY_CONTROLLER = FinancialFuzzyController()
MAMDANI_SUGENO_TESTER = ComparativeFISTester()
HYBRID_ADVISOR = HybridNeuroFuzzyAdvisor()
PERCEPTRON_CLASSIFIER = SupervisedFinancialPerceptron()
PERCEPTRON_CLASSIFIER.train_default()
COMPETITIVE_CLUSTERING = UnsupervisedFinancialCompetitiveLearning()
COMPETITIVE_CLUSTERING.train_and_cluster()
LANGUAGE_MODEL = FinancialLanguageModels()

ESSENTIAL_CATEGORIES = {'Rent', 'Groceries', 'Utilities', 'Healthcare', 'EMI / Loans', 'Education'}
DISCRETIONARY_CATEGORIES = {'Dining Out', 'Entertainment', 'Shopping', 'Travel', 'Subscriptions', 'Personal Care'}

class FinancialEngine:
    @staticmethod
    def get_summary_metrics(month=None):
        conn = get_db_connection()
        cursor = conn.cursor()

        date_filter = ""
        params = []
        if month:
            date_filter = "WHERE strftime('%Y-%m', date) = ?"
            params = [month]

        cursor.execute(f"""
            SELECT 
                COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) AS total_income,
                COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) AS total_expense
            FROM transactions
            {date_filter}
        """, params)
        row = cursor.fetchone()
        total_income = float(row["total_income"]) if row else 0.0
        total_expense = float(row["total_expense"]) if row else 0.0
        balance = total_income - total_expense
        savings_rate = (balance / total_income * 100.0) if total_income > 0 else 0.0

        cursor.execute(f"""
            SELECT category, SUM(amount) AS total, type
            FROM transactions
            {date_filter}
            GROUP BY category, type
            ORDER BY total DESC
        """, params)
        category_rows = cursor.fetchall()
        
        expense_by_category = {}
        income_by_category = {}
        essential_expense = 0.0
        discretionary_expense = 0.0

        for r in category_rows:
            cat = r["category"]
            amt = float(r["total"])
            if r["type"] == "expense":
                expense_by_category[cat] = amt
                if cat in ESSENTIAL_CATEGORIES:
                    essential_expense += amt
                else:
                    discretionary_expense += amt
            else:
                income_by_category[cat] = amt

        conn.close()

        expense_ratio = (total_expense / total_income * 100.0) if total_income > 0 else 100.0
        
        health_score = 50.0
        if total_income > 0:
            health_score += min(40.0, max(-30.0, (savings_rate / 30.0) * 40.0))
            disc_ratio = (discretionary_expense / total_income * 100.0)
            if disc_ratio <= 30.0:
                health_score += 20.0
            elif disc_ratio <= 50.0:
                health_score += 10.0
            else:
                health_score -= 15.0
            ess_ratio = (essential_expense / total_income * 100.0)
            if ess_ratio <= 50.0:
                health_score += 10.0
        health_score = max(0.0, min(100.0, round(health_score, 1)))

        return {
            "month": month or "All Time",
            "total_income": round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "balance": round(balance, 2),
            "savings_rate": round(savings_rate, 2),
            "expense_ratio": round(expense_ratio, 2),
            "essential_expense": round(essential_expense, 2),
            "discretionary_expense": round(discretionary_expense, 2),
            "health_score": health_score,
            "expense_by_category": expense_by_category,
            "income_by_category": income_by_category
        }

    @staticmethod
    def get_budget_status(month):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT category, limit_amount FROM budgets WHERE month = ?", (month,))
        budget_map = {row["category"]: float(row["limit_amount"]) for row in cursor.fetchall()}

        cursor.execute("""
            SELECT category, SUM(amount) AS spent
            FROM transactions
            WHERE strftime('%Y-%m', date) = ? AND type = 'expense'
            GROUP BY category
        """, (month,))
        spent_map = {row["category"]: float(row["spent"]) for row in cursor.fetchall()}
        conn.close()

        all_categories = sorted(list(set(list(budget_map.keys()) + list(spent_map.keys()))))
        results = []
        total_budget = 0.0
        total_spent = 0.0

        for cat in all_categories:
            limit = budget_map.get(cat, 0.0)
            spent = spent_map.get(cat, 0.0)
            pct = (spent / limit * 100.0) if limit > 0 else (100.0 if spent > 0 else 0.0)
            status = "Within Budget"
            if limit > 0:
                if spent > limit:
                    status = "Exceeded"
                elif spent >= limit * 0.85:
                    status = "Near Limit"
            elif spent > 0:
                status = "Unbudgeted"

            results.append({
                "category": cat,
                "budget_limit": round(limit, 2),
                "actual_spent": round(spent, 2),
                "remaining": round(limit - spent, 2) if limit > 0 else 0.0,
                "percentage_used": round(pct, 1),
                "status": status,
                "is_discretionary": cat in DISCRETIONARY_CATEGORIES
            })
            total_budget += limit
            total_spent += spent

        return {
            "month": month,
            "total_budget": round(total_budget, 2),
            "total_spent": round(total_spent, 2),
            "categories": results
        }

    @staticmethod
    def get_comprehensive_ai_advisory(month=None):
        metrics = FinancialEngine.get_summary_metrics(month)
        income = metrics["total_income"]
        expense = metrics["total_expense"]
        savings_rate = metrics["savings_rate"]
        essential = metrics["essential_expense"]
        discretionary = metrics["discretionary_expense"]
        expense_ratio = metrics["expense_ratio"]

        eval_income = income if income > 0 else 65000.0
        eval_expense = expense if expense > 0 else 42000.0
        eval_essential = essential if essential > 0 else (eval_expense * 0.6)

        current_state = "Deficit" if expense > income and income > 0 else (
            "Regular_Savings" if savings_rate >= 25 else "Budget_Balanced"
        )
        agent_roadmap = STATE_SPACE_AGENT.simulate_path(current_state)

        user_profile = {
            "income": eval_income,
            "expense": eval_expense,
            "emergency_fund": max(0.0, eval_income - eval_expense) * 3,
            "has_high_interest_debt": (expense_ratio > 80.0),
            "credit_score": 740 if expense_ratio < 75.0 else 630
        }
        expert_eval = EXPERT_SYSTEM.evaluate_user("current_user", custom_data=user_profile)

        fuzzy_eval = FUZZY_CONTROLLER.evaluate(expense_ratio, max(0.0, savings_rate))

        dsr_pct = (discretionary / eval_income * 100.0) if eval_income > 0 else 25.0
        fis_comp = MAMDANI_SUGENO_TESTER.compare(min(50.0, max(0.0, dsr_pct)))

        hybrid_eval = HYBRID_ADVISOR.predict(eval_income, eval_essential)

        ess_adherence = min(100.0, max(0.0, (1.0 - (essential / eval_income if eval_income > 0 else 0.5)) * 100))
        disc_control = min(100.0, max(0.0, (1.0 - (discretionary / eval_income if eval_income > 0 else 0.5)) * 100))
        perceptron_eval = PERCEPTRON_CLASSIFIER.predict(savings_rate, ess_adherence, disc_control)
        persona_eval = COMPETITIVE_CLUSTERING.predict_cluster(savings_rate, ess_adherence, disc_control)

        lm_query = "budgeting" if expense_ratio > 70 else "emergency"
        lm_next_word, _ = LANGUAGE_MODEL.ulm_predict_next_word(lm_query)
        generated_tip = LANGUAGE_MODEL.slm_generate_text("personal", "financial", length=14)

        return {
            "metrics": metrics,
            "state_space_roadmap": agent_roadmap,
            "expert_system": expert_eval,
            "fuzzy_controller": fuzzy_eval,
            "mamdani_sugeno_comparison": fis_comp,
            "hybrid_neuro_fuzzy": hybrid_eval,
            "perceptron_classification": perceptron_eval,
            "financial_persona": persona_eval,
            "language_model_insights": {
                "sample_query": lm_query,
                "predicted_next_word": lm_next_word,
                "generated_advisory_text": generated_tip
            }
        }

    @staticmethod
    def get_continuous_improvement_history():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                strftime('%Y-%m', date) as txn_month,
                COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) AS income,
                COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) AS expense
            FROM transactions
            GROUP BY txn_month
            ORDER BY txn_month ASC
        """)
        months_data = cursor.fetchall()
        conn.close()

        history = []
        prev_savings_rate = None

        for row in months_data:
            m = row["txn_month"]
            inc = float(row["income"])
            exp = float(row["expense"])
            savings = inc - exp
            rate = (savings / inc * 100.0) if inc > 0 else 0.0
            
            mom_change = 0.0
            trend_direction = "Stable"
            if prev_savings_rate is not None:
                mom_change = round(rate - prev_savings_rate, 2)
                if mom_change > 1.0:
                    trend_direction = "Improved"
                elif mom_change < -1.0:
                    trend_direction = "Declined"
                else:
                    trend_direction = "Stable"
            prev_savings_rate = rate

            health = "Good" if rate >= 25.0 else ("Moderate" if rate >= 10.0 else "Needs Attention")

            history.append({
                "month": m,
                "income": round(inc, 2),
                "expense": round(exp, 2),
                "savings": round(savings, 2),
                "savings_rate": round(rate, 2),
                "mom_change": mom_change,
                "trend": trend_direction,
                "health_status": health
            })

        return history
