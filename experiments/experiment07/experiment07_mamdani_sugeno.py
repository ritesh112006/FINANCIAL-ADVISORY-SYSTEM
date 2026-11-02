import numpy as np

def trimf(x, params):
    a, b, c = params
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a) if b != a else 1.0
    elif b < x < c:
        return (c - x) / (c - b) if c != b else 1.0
    return 0.0

class ComparativeFISTester:
    def __init__(self):
        self.dsr_range = np.arange(0, 51, 1)
        self.mf_low = [0, 0, 20]
        self.mf_med = [10, 25, 35]
        self.mf_high = [25, 50, 50]

        self.sugeno_z = {
            "low": 80,
            "medium": 50,
            "high": 20
        }

    def compute_sugeno(self, dsr_input):
        w1 = trimf(dsr_input, self.mf_low)
        w2 = trimf(dsr_input, self.mf_med)
        w3 = trimf(dsr_input, self.mf_high)

        z1 = self.sugeno_z["low"]
        z2 = self.sugeno_z["medium"]
        z3 = self.sugeno_z["high"]

        total_weight = w1 + w2 + w3
        if total_weight == 0:
            sugeno_out = 50.0
        else:
            sugeno_out = (w1 * z1 + w2 * z2 + w3 * z3) / total_weight

        return {
            "weights": {"w1_low": round(w1, 3), "w2_med": round(w2, 3), "w3_high": round(w3, 3)},
            "singletons": {"z1": z1, "z2": z2, "z3": z3},
            "output_equity_pct": round(float(sugeno_out), 2)
        }

    def compute_mamdani(self, dsr_input):
        w_low = trimf(dsr_input, self.mf_low)
        w_med = trimf(dsr_input, self.mf_med)
        w_high = trimf(dsr_input, self.mf_high)

        out_universe = np.linspace(0, 100, 201)
        mu_agg = []
        for y in out_universe:
            mu_high_alloc = min(w_low, trimf(y, [60, 80, 100]))
            mu_med_alloc  = min(w_med, trimf(y, [35, 50, 65]))
            mu_low_alloc  = min(w_high, trimf(y, [0, 20, 40]))
            mu_agg.append(max(mu_low_alloc, mu_med_alloc, mu_high_alloc))

        numerator = sum(y * mu for y, mu in zip(out_universe, mu_agg))
        denominator = sum(mu_agg)
        mamdani_out = (numerator / denominator) if denominator > 0 else 50.0

        return {
            "firing_strengths": {"low_dsr": round(w_low, 3), "med_dsr": round(w_med, 3), "high_dsr": round(w_high, 3)},
            "output_equity_pct": round(float(mamdani_out), 2)
        }

    def compare(self, dsr_input):
        mam = self.compute_mamdani(dsr_input)
        sug = self.compute_sugeno(dsr_input)
        diff = abs(mam["output_equity_pct"] - sug["output_equity_pct"])
        return {
            "input_dsr_pct": dsr_input,
            "mamdani": mam,
            "sugeno": sug,
            "absolute_difference": round(diff, 2),
            "interpretation": f"At {dsr_input}% discretionary spending, Mamdani gives {mam['output_equity_pct']}% equity and Sugeno gives {sug['output_equity_pct']}%."
        }


def run_experiment_07():
    tester = ComparativeFISTester()
    return tester.compare(28.0)

if __name__ == "__main__":
    res = run_experiment_07()
    print("Mamdani:", res["mamdani"]["output_equity_pct"], "Sugeno:", res["sugeno"]["output_equity_pct"])
