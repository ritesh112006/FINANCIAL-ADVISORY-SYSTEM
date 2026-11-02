profile(rahul, 65000, 42000, 150000, no, 760).
profile(amit, 40000, 38000, 20000, yes, 620).
profile(neha, 90000, 45000, 350000, no, 810).
profile(priya, 55000, 52000, 10000, yes, 580).

category(rent, essential, no).
category(groceries, essential, no).
category(utilities, essential, no).
category(dining_out, discretionary, yes).
category(entertainment, discretionary, yes).
category(shopping, discretionary, yes).
category(travel, discretionary, yes).

monthly_savings(User, Savings) :-
    profile(User, Income, Expense, _, _, _),
    Savings is Income - Expense.

savings_rate(User, Rate) :-
    profile(User, Income, Expense, _, _, _),
    Savings is Income - Expense,
    Rate is (Savings / Income) * 100.

emergency_fund_adequate(User) :-
    profile(User, _, Expense, EmergencyFund, _, _),
    ThreeMonthsExpense is Expense * 3,
    EmergencyFund >= ThreeMonthsExpense.

high_risk_spending(User) :-
    profile(User, Income, Expense, _, yes, _),
    Expense > (Income * 0.70).

high_risk_spending(User) :-
    profile(User, Income, Expense, _, _, _),
    Expense > (Income * 0.85).

eligible_for_investment(User) :-
    profile(User, _, _, _, no, CreditScore),
    CreditScore >= 700,
    emergency_fund_adequate(User).

recommend_cut(Category) :-
    category(Category, discretionary, yes).
