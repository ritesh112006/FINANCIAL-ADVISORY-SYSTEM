class FinWiseAgentPEAS:
    @staticmethod
    def get_peas_description():
        return {
            "Performance Measure": "Savings rate >= 20%, maintain 3 months emergency fund, stay within budget limits.",
            "Environment": "Monthly income, expenses (Rent, Food, Bills, Shopping), savings, and transactions.",
            "Actuators": "Budget limits, savings reminders, spending alerts, expense cut suggestions.",
            "Sensors": "User transactions, account balance, category totals, budget alerts."
        }


class FinancialStateSpace:
    def __init__(self):
        self.initial_state = "Deficit"
        self.goal_state = "Financial_Independence"
        
        self.state_graph = {
            "Deficit": [
                {"next": "Budget_Balanced", "action": "Cut discretionary spending and stop taking loans", "cost": 1},
                {"next": "High_Debt", "action": "Take consolidation loan", "cost": 2}
            ],
            "High_Debt": [
                {"next": "Budget_Balanced", "action": "Pay off high interest debt first", "cost": 3}
            ],
            "Budget_Balanced": [
                {"next": "Emergency_Fund_Ready", "action": "Save 3 months of emergency expenses", "cost": 2},
                {"next": "Regular_Savings", "action": "Save 20% of monthly income", "cost": 2}
            ],
            "Emergency_Fund_Ready": [
                {"next": "Regular_Savings", "action": "Build recurring savings habit", "cost": 1},
                {"next": "Investing", "action": "Start low risk mutual fund SIPs", "cost": 3}
            ],
            "Regular_Savings": [
                {"next": "Investing", "action": "Invest surplus savings in index funds", "cost": 2}
            ],
            "Investing": [
                {"next": "Financial_Independence", "action": "Grow investments until returns cover living expenses", "cost": 5}
            ],
            "Financial_Independence": []
        }

    def display_formulation(self):
        return {
            "initial_state": self.initial_state,
            "goal_state": self.goal_state,
            "states": list(self.state_graph.keys()),
            "graph": self.state_graph
        }

    def goal_test(self, current_state):
        return current_state == self.goal_state

    def simulate_path(self, start_state=None):
        start = start_state or self.initial_state
        current = start
        path = [current]
        total_path_cost = 0
        actions_taken = []

        while current != self.goal_state:
            transitions = self.state_graph.get(current, [])
            if not transitions:
                break
            best_transition = transitions[0]
            current = best_transition["next"]
            total_path_cost += best_transition["cost"]
            actions_taken.append({
                "action": best_transition["action"],
                "reached_state": current,
                "step_cost_months": best_transition["cost"]
            })
            path.append(current)

        return {
            "start_state": start,
            "goal_state": self.goal_state,
            "goal_reached": self.goal_test(current),
            "trajectory": path,
            "total_path_cost_months": total_path_cost,
            "actions": actions_taken
        }


def run_experiment_01():
    peas = FinWiseAgentPEAS.get_peas_description()
    fss = FinancialStateSpace()
    simulation = fss.simulate_path()
    return simulation

if __name__ == "__main__":
    res = run_experiment_01()
    print("Roadmap:", " -> ".join(res["trajectory"]))
