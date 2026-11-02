from collections import deque

FINANCIAL_MILESTONE_GRAPH = {
    'Unbudgeted_Cashflow': ['Expense_Tracking', 'Emergency_Reserve_Start'],
    'Expense_Tracking': ['50_30_20_Budget_Set', 'High_Interest_Debt_Payoff'],
    'Emergency_Reserve_Start': ['1_Month_Buffer_Built', '3_Month_Emergency_Fund'],
    '50_30_20_Budget_Set': ['Surplus_Capital_Unlocked', 'Discretionary_Spending_Capped'],
    'High_Interest_Debt_Payoff': ['Zero_Consumer_Debt', 'Credit_Score_Optimized'],
    '1_Month_Buffer_Built': ['3_Month_Emergency_Fund', 'Surplus_Capital_Unlocked'],
    '3_Month_Emergency_Fund': ['Retirement_SIP_Active', 'Goal_Specific_Investment'],
    'Surplus_Capital_Unlocked': ['Goal_Specific_Investment', 'Home_Downpayment_Fund'],
    'Discretionary_Spending_Capped': ['Goal_Specific_Investment'],
    'Zero_Consumer_Debt': ['Retirement_SIP_Active', 'Home_Downpayment_Fund'],
    'Credit_Score_Optimized': ['Low_Interest_Home_Loan_Ready'],
    'Goal_Specific_Investment': ['Financial_Goal_Achieved'],
    'Retirement_SIP_Active': ['Financial_Goal_Achieved'],
    'Home_Downpayment_Fund': ['Financial_Goal_Achieved'],
    'Low_Interest_Home_Loan_Ready': ['Financial_Goal_Achieved'],
    'Financial_Goal_Achieved': []
}

def bfs_financial_path(graph, start, goal):
    visited = set()
    queue = deque([[start]])
    exploration_order = []

    while queue:
        path = queue.popleft()
        node = path[-1]
        exploration_order.append(node)

        if node == goal:
            return {
                "algorithm": "BFS",
                "found": True,
                "path": path,
                "step_count": len(path) - 1,
                "nodes_explored": exploration_order
            }

        if node not in visited:
            visited.add(node)
            for neighbour in graph.get(node, []):
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

    return {"algorithm": "BFS", "found": False, "path": [], "nodes_explored": exploration_order}


def dfs_financial_path(graph, start, goal):
    stack = [[start]]
    visited = set()
    exploration_order = []

    while stack:
        path = stack.pop()
        node = path[-1]
        exploration_order.append(node)

        if node == goal:
            return {
                "algorithm": "DFS",
                "found": True,
                "path": path,
                "step_count": len(path) - 1,
                "nodes_explored": exploration_order
            }

        if node not in visited:
            visited.add(node)
            for neighbour in reversed(graph.get(node, [])):
                new_path = list(path)
                new_path.append(neighbour)
                stack.append(new_path)

    return {"algorithm": "DFS", "found": False, "path": [], "nodes_explored": exploration_order}


def compare_search_algorithms(start='Unbudgeted_Cashflow', goal='Financial_Goal_Achieved'):
    bfs_res = bfs_financial_path(FINANCIAL_MILESTONE_GRAPH, start, goal)
    dfs_res = dfs_financial_path(FINANCIAL_MILESTONE_GRAPH, start, goal)
    return {
        "start": start,
        "goal": goal,
        "bfs": bfs_res,
        "dfs": dfs_res,
        "summary": f"BFS found path in {bfs_res['step_count']} steps. DFS explored {len(dfs_res['nodes_explored'])} nodes."
    }

def run_experiment_03():
    return compare_search_algorithms()

if __name__ == "__main__":
    res = run_experiment_03()
    print("BFS Path:", " -> ".join(res["bfs"]["path"]))
