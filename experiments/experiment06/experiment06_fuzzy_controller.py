import numpy as np

try:
    import skfuzzy as fuzz
    from skfuzzy import control as ctrl
    HAS_SKFUZZY = True
except ImportError:
    HAS_SKFUZZY = False

class FinancialFuzzyController:
    def __init__(self):
        self.has_skfuzzy = HAS_SKFUZZY
        if self.has_skfuzzy:
            self._setup_skfuzzy_system()

    def _setup_skfuzzy_system(self):
        self.expense_ratio = ctrl.Antecedent(np.arange(0, 101, 1), 'expense_ratio')
        self.savings_rate = ctrl.Antecedent(np.arange(0, 101, 1), 'savings_rate')
        self.restriction = ctrl.Consequent(np.arange(0, 101, 1), 'restriction')

        self.expense_ratio['low'] = fuzz.trimf(self.expense_ratio.universe, [0, 20, 50])
        self.expense_ratio['medium'] = fuzz.trimf(self.expense_ratio.universe, [40, 60, 75])
        self.expense_ratio['high'] = fuzz.trimf(self.expense_ratio.universe, [70, 90, 100])

        self.savings_rate['low'] = fuzz.trimf(self.savings_rate.universe, [0, 10, 20])
        self.savings_rate['medium'] = fuzz.trimf(self.savings_rate.universe, [15, 30, 45])
        self.savings_rate['high'] = fuzz.trimf(self.savings_rate.universe, [40, 70, 100])

        self.restriction['low'] = fuzz.trimf(self.restriction.universe, [0, 20, 40])
        self.restriction['medium'] = fuzz.trimf(self.restriction.universe, [30, 50, 70])
        self.restriction['high'] = fuzz.trimf(self.restriction.universe, [60, 85, 100])

        r1 = ctrl.Rule(self.expense_ratio['low'] & self.savings_rate['high'], self.restriction['low'])
        r2 = ctrl.Rule(self.expense_ratio['low'] & self.savings_rate['medium'], self.restriction['low'])
        r3 = ctrl.Rule(self.expense_ratio['low'] & self.savings_rate['low'], self.restriction['medium'])
        r4 = ctrl.Rule(self.expense_ratio['medium'] & self.savings_rate['high'], self.restriction['low'])
        r5 = ctrl.Rule(self.expense_ratio['medium'] & self.savings_rate['medium'], self.restriction['medium'])
        r6 = ctrl.Rule(self.expense_ratio['medium'] & self.savings_rate['low'], self.restriction['high'])
        r7 = ctrl.Rule(self.expense_ratio['high'] & self.savings_rate['low'], self.restriction['high'])
        r8 = ctrl.Rule(self.expense_ratio['high'] & self.savings_rate['medium'], self.restriction['high'])
        r9 = ctrl.Rule(self.expense_ratio['high'] & self.savings_rate['high'], self.restriction['medium'])

        self.control_sys = ctrl.ControlSystem([r1, r2, r3, r4, r5, r6, r7, r8, r9])

    @staticmethod
    def _triangular_mf(x, a, b, c):
        if x <= a or x >= c:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a) if b != a else 1.0
        elif b < x < c:
            return (c - x) / (c - b) if c != b else 1.0
        return 0.0

    def compute_pure_python(self, exp_val, sav_val):
        exp_low = self._triangular_mf(exp_val, 0, 20, 50)
        exp_med = self._triangular_mf(exp_val, 40, 60, 75)
        exp_high = self._triangular_mf(exp_val, 70, 90, 100)

        sav_low = self._triangular_mf(sav_val, 0, 10, 20)
        sav_med = self._triangular_mf(sav_val, 15, 30, 45)
        sav_high = self._triangular_mf(sav_val, 40, 70, 100)

        w_low = max(min(exp_low, sav_high), min(exp_low, sav_med), min(exp_med, sav_high))
        w_med = max(min(exp_low, sav_low), min(exp_med, sav_med), min(exp_high, sav_high))
        w_high = max(min(exp_med, sav_low), min(exp_high, sav_low), min(exp_high, sav_med))

        x_vals = np.linspace(0, 100, 101)
        mu_agg = []
        for x in x_vals:
            mu_l = min(w_low, self._triangular_mf(x, 0, 20, 40))
            mu_m = min(w_med, self._triangular_mf(x, 30, 50, 70))
            mu_h = min(w_high, self._triangular_mf(x, 60, 85, 100))
            mu_agg.append(max(mu_l, mu_m, mu_h))

        numerator = sum(x * mu for x, mu in zip(x_vals, mu_agg))
        denominator = sum(mu_agg)
        crisp_output = (numerator / denominator) if denominator > 0 else 50.0
        return float(crisp_output)

    def evaluate(self, expense_ratio_pct, savings_rate_pct):
        exp_val = max(0.0, min(100.0, float(expense_ratio_pct)))
        sav_val = max(0.0, min(100.0, float(savings_rate_pct)))

        if self.has_skfuzzy:
            try:
                sim = ctrl.ControlSystemSimulation(self.control_sys)
                sim.input['expense_ratio'] = exp_val
                sim.input['savings_rate'] = sav_val
                sim.compute()
                restriction_val = float(sim.output['restriction'])
            except Exception:
                restriction_val = self.compute_pure_python(exp_val, sav_val)
        else:
            restriction_val = self.compute_pure_python(exp_val, sav_val)

        restriction_val = round(restriction_val, 2)
        if restriction_val <= 35:
            status = "Low Restriction"
            advice = "Your spending is healthy. Continue your regular savings."
        elif restriction_val <= 65:
            status = "Moderate Restriction"
            advice = "Keep a check on non-essential spending this month."
        else:
            status = "High Restriction"
            advice = "High expenses detected. Avoid luxury purchases until cash reserve improves."

        return {
            "expense_ratio": exp_val,
            "savings_rate": sav_val,
            "restriction_percentage": restriction_val,
            "status": status,
            "financial_advice": advice
        }


def run_experiment_06():
    controller = FinancialFuzzyController()
    return controller.evaluate(65.0, 25.0)

if __name__ == "__main__":
    res = run_experiment_06()
    print("Restriction:", res["restriction_percentage"])
