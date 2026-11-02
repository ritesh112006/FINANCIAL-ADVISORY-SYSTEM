import unittest
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

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


class TestExperiments(unittest.TestCase):

    def test_experiment_01_peas_state_space(self):
        peas = FinWiseAgentPEAS.get_peas_description()
        self.assertIn("Performance Measure", peas)
        fss = FinancialStateSpace()
        sim = fss.simulate_path("Deficit")
        self.assertTrue(sim["goal_reached"])
        self.assertEqual(sim["goal_state"], "Financial_Independence")
        self.assertGreater(len(sim["trajectory"]), 2)

    def test_experiment_02_expert_system(self):
        engine = FinancialExpertSystem()
        rahul_eval = engine.evaluate_user("rahul")
        self.assertTrue(rahul_eval["emergency_fund_adequate"])
        amit_eval = engine.evaluate_user("amit")
        self.assertTrue(amit_eval["high_risk_spending"])

    def test_experiment_03_bfs_dfs(self):
        comp = compare_search_algorithms('Unbudgeted_Cashflow', 'Financial_Goal_Achieved')
        self.assertTrue(comp['bfs']['found'])
        self.assertTrue(comp['dfs']['found'])
        self.assertLessEqual(comp['bfs']['step_count'], comp['dfs']['step_count'])

    def test_experiment_04_a_star(self):
        optimizer = BudgetAStarOptimizer(target_budget=(10, 5, 8))
        res = optimizer.a_star_solve((14, 8, 10))
        self.assertTrue(res["success"])
        self.assertEqual(res["target_state"], (10, 5, 8))
        self.assertGreater(len(res["action_sequence"]), 0)

    def test_experiment_05_minimax(self):
        tester = FinancialStressTester()
        res = tester.evaluate_stress_test()
        self.assertIn(res["recommended_strategy"], [
            "Conservative Allocation",
            "Growth Allocation"
        ])
        self.assertGreater(res["minimax_optimal_value"], 0)

    def test_experiment_06_fuzzy_controller(self):
        ctrl = FinancialFuzzyController()
        healthy = ctrl.evaluate(30.0, 45.0)
        self.assertLessEqual(healthy["restriction_percentage"], 40.0)
        critical = ctrl.evaluate(85.0, 5.0)
        self.assertGreaterEqual(critical["restriction_percentage"], 60.0)

    def test_experiment_07_mamdani_sugeno(self):
        tester = ComparativeFISTester()
        res = tester.compare(25.0)
        self.assertGreater(res["mamdani"]["output_equity_pct"], 0)
        self.assertGreater(res["sugeno"]["output_equity_pct"], 0)

    def test_experiment_08_hybrid_neuro_fuzzy(self):
        advisor = HybridNeuroFuzzyAdvisor()
        res = advisor.predict(75000, 38000)
        self.assertGreater(res["hybrid_savings_rate_pct"], 0)
        self.assertGreater(res["potential_monthly_savings_inr"], 0)

    def test_experiment_09_neural_learning(self):
        p = SupervisedFinancialPerceptron()
        p.train_default()
        res_high = p.predict(45, 90, 85)
        self.assertEqual(res_high["prediction_code"], 1)
        res_low = p.predict(5, 40, 30)
        self.assertEqual(res_low["prediction_code"], 0)

        c = UnsupervisedFinancialCompetitiveLearning()
        c.train_and_cluster()
        c_pred = c.predict_cluster(40, 85, 80)
        self.assertIn(c_pred["assigned_cluster"], [1, 2])

    def test_experiment_10_language_models(self):
        lm = FinancialLanguageModels()
        pred, prob = lm.ulm_predict_next_word("emergency")
        self.assertEqual(pred, "fund")
        gen = lm.slm_generate_text("emergency", "fund", length=6)
        self.assertIn("emergency fund", gen)


if __name__ == '__main__':
    unittest.main()
