import numpy as np
import pandas as pd

class SupervisedFinancialPerceptron:
    def __init__(self, learning_rate=0.1, epochs=25):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = 0.0
        self.features = ["Savings_Rate_Pct", "Essential_Adherence_Pct", "Discretionary_Control_Pct"]

    def train_default(self):
        data = {
            "Savings_Rate_Pct":        [45, 35, 40, 30, 10, 8, 12, 5],
            "Essential_Adherence_Pct":  [90, 85, 95, 80, 50, 45, 60, 40],
            "Discretionary_Control_Pct":[85, 80, 90, 75, 40, 35, 50, 30],
            "Target":                   [ 1,  1,  1,  1,  0,  0,  0,  0]
        }
        df = pd.DataFrame(data)
        X = df[self.features].values / 100.0
        y = df["Target"].values

        self.weights = np.zeros(X.shape[1])
        self.bias = 0.0

        for epoch in range(self.epochs):
            total_error = 0
            for i in range(len(X)):
                net = np.dot(X[i], self.weights) + self.bias
                pred = 1 if net >= 0 else 0
                error = y[i] - pred
                self.weights += self.learning_rate * error * X[i]
                self.bias += self.learning_rate * error
                total_error += abs(error)
            if total_error == 0:
                break
        return {"epochs_trained": epoch + 1, "weights": self.weights.tolist(), "bias": self.bias}

    def predict(self, savings_rate, essential_adherence, discretionary_control):
        x = np.array([savings_rate, essential_adherence, discretionary_control]) / 100.0
        net = np.dot(x, self.weights) + self.bias
        pred = 1 if net >= 0 else 0
        return {
            "prediction_code": pred,
            "classification": "Disciplined Spending" if pred == 1 else "High Risk Spending",
            "net_activation": round(float(net), 4)
        }


class UnsupervisedFinancialCompetitiveLearning:
    def __init__(self, learning_rate=0.3, epochs=15):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = np.array([
            [0.8, 0.8, 0.8],
            [0.3, 0.4, 0.3]
        ])

    def train_and_cluster(self):
        data = {
            "Savings_Rate":        [45, 40, 35, 30, 10, 8, 12, 5],
            "Fixed_Discipline":    [90, 85, 80, 75, 50, 45, 55, 40],
            "Discretionary_Budget":[85, 80, 85, 70, 40, 35, 45, 30]
        }
        df = pd.DataFrame(data)
        X = df.values / 100.0

        for epoch in range(self.epochs):
            for x in X:
                distances = np.linalg.norm(self.weights - x, axis=1)
                winner = np.argmin(distances)
                self.weights[winner] += self.learning_rate * (x - self.weights[winner])

        clusters = []
        for x in X:
            d = np.linalg.norm(self.weights - x, axis=1)
            clusters.append(int(np.argmin(d) + 1))

        df["Cluster"] = clusters
        return {
            "clustered_data": df.to_dict(orient="records"),
            "final_neuron_weights": self.weights.tolist(),
            "cluster_labels": {
                1: "Cluster 1: Consistent Savers",
                2: "Cluster 2: High Spenders"
            }
        }

    def predict_cluster(self, savings_rate, fixed_discipline, discretionary_budget):
        x = np.array([savings_rate, fixed_discipline, discretionary_budget]) / 100.0
        d = np.linalg.norm(self.weights - x, axis=1)
        winner = int(np.argmin(d) + 1)
        persona = "Consistent Saver" if winner == 1 else "High Spender"
        return {"assigned_cluster": winner, "financial_persona": persona, "distances": [round(float(val), 4) for val in d]}


def run_experiment_09():
    perceptron = SupervisedFinancialPerceptron()
    perceptron.train_default()
    p_res = perceptron.predict(38, 85, 80)
    
    comp = UnsupervisedFinancialCompetitiveLearning()
    comp.train_and_cluster()
    c_res = comp.predict_cluster(38, 85, 80)
    return {"perceptron": p_res, "clustering": c_res}

if __name__ == "__main__":
    res = run_experiment_09()
    print("Classification:", res["perceptron"]["classification"])
