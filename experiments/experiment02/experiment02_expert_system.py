class FinancialExpertSystem:
    def __init__(self):
        self.profiles = {
            "rahul": {
                "income": 65000,
                "expense": 42000,
                "emergency_fund": 150000,
                "has_high_interest_debt": False,
                "credit_score": 760
            },
            "amit": {
                "income": 40000,
                "expense": 38000,
                "emergency_fund": 20000,
                "has_high_interest_debt": True,
                "credit_score": 620
            },
            "neha": {
                "income": 90000,
                "expense": 45000,
                "emergency_fund": 350000,
                "has_high_interest_debt": False,
                "credit_score": 810
            },
            "priya": {
                "income": 55000,
                "expense": 52000,
                "emergency_fund": 10000,
                "has_high_interest_debt": True,
                "credit_score": 580
            }
        }
        
        self.categories = {
            "rent": {"essential": True, "can_cut": False},
            "groceries": {"essential": True, "can_cut": False},
            "utilities": {"essential": True, "can_cut": False},
            "dining_out": {"essential": False, "can_cut": True},
            "entertainment": {"essential": False, "can_cut": True},
            "shopping": {"essential": False, "can_cut": True},
            "travel": {"essential": False, "can_cut": True}
        }

    def calculate_savings(self, profile):
        savings = profile["income"] - profile["expense"]
        rate = (savings / profile["income"]) * 100 if profile["income"] > 0 else 0
        return savings, rate

    def is_emergency_fund_adequate(self, profile):
        target = profile["expense"] * 3
        return profile["emergency_fund"] >= target, target

    def is_high_risk_spending(self, profile):
        ratio = profile["expense"] / profile["income"] if profile["income"] > 0 else 1.0
        if profile["has_high_interest_debt"] and ratio > 0.70:
            return True, f"High debt burden with expense ratio of {ratio*100:.1f}%"
        if ratio > 0.85:
            return True, f"High spending ratio of {ratio*100:.1f}%"
        return False, f"Stable spending ratio of {ratio*100:.1f}%"

    def is_eligible_for_investment(self, profile):
        adequate, _ = self.is_emergency_fund_adequate(profile)
        no_debt = not profile["has_high_interest_debt"]
        good_credit = profile["credit_score"] >= 700
        eligible = adequate and no_debt and good_credit
        reasons = []
        if not adequate:
            reasons.append("Emergency fund is lower than 3 months of expenses")
        if not no_debt:
            reasons.append("Clear high interest debt before investing")
        if not good_credit:
            reasons.append("Credit score is below 700")
        return eligible, reasons

    def evaluate_user(self, user_name, custom_data=None):
        profile = custom_data or self.profiles.get(user_name.lower())
        if not profile:
            return {"error": f"Profile for '{user_name}' not found."}

        savings, rate = self.calculate_savings(profile)
        ef_status, ef_target = self.is_emergency_fund_adequate(profile)
        risk_status, risk_reason = self.is_high_risk_spending(profile)
        inv_status, inv_reasons = self.is_eligible_for_investment(profile)

        recommendations = []
        if risk_status:
            recommendations.append("Reduce spending on dining out, shopping, and entertainment.")
        if not ef_status:
            recommendations.append(f"Build emergency fund to at least Rs. {ef_target:,.2f} before investing.")
        if inv_status:
            recommendations.append("You are in a good position to start mutual fund SIPs.")
        else:
            recommendations.append("Focus on clearing debt and saving an emergency fund first.")

        return {
            "user": user_name,
            "monthly_income": profile["income"],
            "monthly_expense": profile["expense"],
            "monthly_savings": savings,
            "savings_rate_pct": round(rate, 2),
            "emergency_fund_adequate": ef_status,
            "emergency_fund_target": ef_target,
            "high_risk_spending": risk_status,
            "risk_analysis": risk_reason,
            "eligible_for_investment": inv_status,
            "ineligibility_reasons": inv_reasons,
            "recommendations": recommendations
        }


def run_experiment_02():
    engine = FinancialExpertSystem()
    return engine.evaluate_user("rahul")

if __name__ == "__main__":
    res = run_experiment_02()
    print("User:", res["user"], "Savings:", res["monthly_savings"])
