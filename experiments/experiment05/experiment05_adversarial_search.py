import math

def minimax_financial(depth, node_index, is_maximizing, terminal_utilities, tree_height):
    if depth == tree_height:
        return terminal_utilities[node_index]

    if is_maximizing:
        left_eval = minimax_financial(depth + 1, node_index * 2, False, terminal_utilities, tree_height)
        right_eval = minimax_financial(depth + 1, node_index * 2 + 1, False, terminal_utilities, tree_height)
        return max(left_eval, right_eval)
    else:
        left_eval = minimax_financial(depth + 1, node_index * 2, True, terminal_utilities, tree_height)
        right_eval = minimax_financial(depth + 1, node_index * 2 + 1, True, terminal_utilities, tree_height)
        return min(left_eval, right_eval)


class FinancialStressTester:
    def __init__(self):
        self.scenarios = [
            {"strategy": "Conservative", "macro": "High Inflation", "micro": "High Emergency", "net_wealth": 42},
            {"strategy": "Conservative", "macro": "High Inflation", "micro": "Normal Bills",   "net_wealth": 55},
            {"strategy": "Conservative", "macro": "Low Inflation",  "micro": "High Emergency", "net_wealth": 48},
            {"strategy": "Conservative", "macro": "Low Inflation",  "micro": "Normal Bills",   "net_wealth": 60},
            {"strategy": "Growth-Equity", "macro": "High Inflation", "micro": "High Emergency", "net_wealth": 30},
            {"strategy": "Growth-Equity", "macro": "High Inflation", "micro": "Normal Bills",   "net_wealth": 50},
            {"strategy": "Growth-Equity", "macro": "Low Inflation",  "micro": "High Emergency", "net_wealth": 65},
            {"strategy": "Growth-Equity", "macro": "Low Inflation",  "micro": "Normal Bills",   "net_wealth": 85},
        ]
        self.terminal_utilities = [s["net_wealth"] for s in self.scenarios]
        self.tree_height = int(math.log2(len(self.terminal_utilities)))

    def evaluate_stress_test(self, custom_utilities=None):
        utilities = custom_utilities if custom_utilities is not None else self.terminal_utilities
        
        branch_conservative = [utilities[0], utilities[1], utilities[2], utilities[3]]
        val_conservative = minimax_financial(0, 0, True, branch_conservative, int(math.log2(len(branch_conservative))))
        
        branch_growth = [utilities[4], utilities[5], utilities[6], utilities[7]]
        val_growth = minimax_financial(0, 0, True, branch_growth, int(math.log2(len(branch_growth))))

        best_value = max(val_conservative, val_growth)
        recommended_strategy = "Conservative Allocation" if best_value == val_conservative else "Growth Allocation"

        return {
            "terminal_utilities": utilities,
            "conservative_worst_case_guaranteed": val_conservative,
            "growth_worst_case_guaranteed": val_growth,
            "minimax_optimal_value": best_value,
            "recommended_strategy": recommended_strategy,
            "scenarios": self.scenarios
        }


def run_experiment_05():
    tester = FinancialStressTester()
    return tester.evaluate_stress_test()

if __name__ == "__main__":
    res = run_experiment_05()
    print("Optimal Strategy:", res["recommended_strategy"])
