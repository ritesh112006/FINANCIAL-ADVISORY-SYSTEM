import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler

class HybridNeuroFuzzyAdvisor:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.ann_model = MLPRegressor(
            hidden_layer_sizes=(16, 16),
            activation="relu",
            solver="lbfgs",
            max_iter=3000,
            random_state=42
        )
        self._train_ann_component()

    def _train_ann_component(self):
        data = {
            "Income":    [25000, 35000, 45000, 50000, 60000, 75000, 85000, 100000, 120000, 150000, 180000, 200000],
            "Essential": [20000, 24000, 28000, 30000, 32000, 38000, 40000,  45000,  50000,  55000,  60000,  65000],
            "SavingsRate": [12.0,  18.0,  24.0,  28.0,  35.0,  40.0,  45.0,   50.0,   55.0,   60.0,   63.0,   65.0]
        }
        df = pd.DataFrame(data)
        X = df[["Income", "Essential"]].values
        y = df["SavingsRate"].values

        X_scaled = self.scaler.fit_transform(X)
        self.ann_model.fit(X_scaled, y)

    @staticmethod
    def _trimf(x, a, b, c):
        if x <= a or x >= c:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a) if b != a else 1.0
        elif b < x < c:
            return (c - x) / (c - b) if c != b else 1.0
        return 0.0

    def fuzzy_reasoning(self, income, essential):
        ratio = (essential / income * 100) if income > 0 else 100.0

        mu_low = self._trimf(ratio, 20, 30, 45)
        mu_med = self._trimf(ratio, 40, 55, 70)
        mu_high = self._trimf(ratio, 65, 85, 100)

        w_sum = mu_low + mu_med + mu_high
        if w_sum == 0:
            return 25.0
        fuzzy_pot = (mu_low * 60.0 + mu_med * 35.0 + mu_high * 15.0) / w_sum
        return float(fuzzy_pot)

    def predict(self, monthly_income, essential_expenses):
        inc = float(monthly_income)
        ess = min(float(essential_expenses), inc)

        scaled_input = self.scaler.transform([[inc, ess]])
        ann_pred = float(self.ann_model.predict(scaled_input)[0])
        ann_pred = max(0.0, min(80.0, ann_pred))

        fuzzy_pred = self.fuzzy_reasoning(inc, ess)

        hybrid_savings_rate = (0.6 * ann_pred) + (0.4 * fuzzy_pred)
        hybrid_savings_rate = round(max(0.0, min(85.0, hybrid_savings_rate)), 2)

        potential_savings_amount = round(inc * (hybrid_savings_rate / 100.0), 2)

        if hybrid_savings_rate >= 40:
            status = "High Savings Potential"
            guidance = "Good surplus available. You can allocate more towards long-term savings."
        elif hybrid_savings_rate >= 20:
            status = "Moderate Savings Potential"
            guidance = "Balanced finances. Try to save regularly every month."
        else:
            status = "Limited Savings Potential"
            guidance = "Fixed expenses are taking most of the income. Try to review regular bills."

        return {
            "monthly_income": inc,
            "essential_expenses": ess,
            "ann_predicted_rate": round(ann_pred, 2),
            "fuzzy_predicted_rate": round(fuzzy_pred, 2),
            "hybrid_savings_rate_pct": hybrid_savings_rate,
            "potential_monthly_savings_inr": potential_savings_amount,
            "status": status,
            "guidance": guidance
        }


def run_experiment_08():
    advisor = HybridNeuroFuzzyAdvisor()
    return advisor.predict(75000, 38000)

if __name__ == "__main__":
    res = run_experiment_08()
    print("Savings Rate:", res["hybrid_savings_rate_pct"])
