import heapq

class BudgetAStarOptimizer:
    def __init__(self, target_budget=(10, 5, 8)):
        self.target_budget = tuple(target_budget)
        self.categories = ["Dining_Out", "Entertainment", "Shopping"]

    def manhattan_heuristic(self, state):
        return sum(abs(s - t) for s, t in zip(state, self.target_budget))

    def generate_next_states(self, state):
        neighbors = []
        state_list = list(state)
        for i in range(len(state_list)):
            if state_list[i] > self.target_budget[i]:
                new_state = list(state_list)
                new_state[i] -= 1
                neighbors.append((tuple(new_state), f"Reduce Rs. 1000 from {self.categories[i]}"))
            elif state_list[i] < self.target_budget[i]:
                new_state = list(state_list)
                new_state[i] += 1
                neighbors.append((tuple(new_state), f"Reallocate Rs. 1000 to {self.categories[i]}"))
        return neighbors

    def a_star_solve(self, initial_budget):
        start = tuple(initial_budget)
        priority_queue = []
        
        step_counter = 0
        h_start = self.manhattan_heuristic(start)
        heapq.heappush(priority_queue, (h_start, step_counter, start, 0, [start], []))
        
        visited = set()
        iterations = 0

        while priority_queue:
            iterations += 1
            f, _, current, g, path, actions = heapq.heappop(priority_queue)

            if current == self.target_budget:
                return {
                    "success": True,
                    "initial_state": start,
                    "target_state": self.target_budget,
                    "optimal_path": path,
                    "action_sequence": actions,
                    "total_cost_g": g,
                    "iterations": iterations
                }

            if current in visited:
                continue
            visited.add(current)

            for next_state, action_desc in self.generate_next_states(current):
                if next_state not in visited:
                    next_g = g + 1
                    next_h = self.manhattan_heuristic(next_state)
                    next_f = next_g + next_h
                    step_counter += 1
                    heapq.heappush(
                        priority_queue,
                        (next_f, step_counter, next_state, next_g, path + [next_state], actions + [action_desc])
                    )

        return {"success": False, "iterations": iterations}


def run_experiment_04():
    optimizer = BudgetAStarOptimizer(target_budget=(10, 5, 8))
    return optimizer.a_star_solve((18, 11, 14))

if __name__ == "__main__":
    res = run_experiment_04()
    print("Steps:", res["total_cost_g"])
