# FinWise - Personal Financial Advisory System

A simple, practical web application that helps users track personal income and expenses, manage budgets, set savings targets, and receive personalized financial advice. The project adapts 10 standard computer science lab experiments into practical personal finance features.

---

## 1. How the System Works (Workflow)

1. **Recording Transactions:** The user adds income or expense transactions with an amount, date, category, and description.
2. **Database Storage:** All entries are stored in a local SQLite database (`database/finwise.db`) using safe, parameterized queries.
3. **Calculation & Analysis:** The backend financial engine calculates total income, total expenses, net balance, savings rate, and category breakdowns.
4. **Dashboard Display:** The dashboard displays financial summary cards, an expense breakdown doughnut chart, and a budget comparison bar chart.
5. **Budget & Savings Tracking:** The system checks whether category spending has exceeded or approached budget limits, and tracks progress towards active savings goals.
6. **Generating Advice:** The system evaluates stored user data using logic rules, search algorithms, fuzzy logic, neural networks, and language models to produce recommendations.
7. **Monthly Progress Tracking:** The application compares spending across months to track financial improvements over time.

---

## 2. Project Structure & Key Files

- `app.py`: The main Flask server. Handles page routes (`/dashboard`, `/transactions`, `/budgets`, `/savings`, `/advisory`, `/continuous-improvement`, `/reports`, `/experiments`) and REST API endpoints.
- `database/schema.sql`: Defines tables for transactions, budgets, savings goals, and snapshots.
- `database/db.py`: Manages the SQLite database connection and initial setup.
- `services/financial_engine.py`: Performs all financial calculations, category breakdowns, health scores, and connects the experiment algorithms with real database data.
- `services/seed_data.py`: Loads sample transactions across four months so the system is ready to demonstrate immediately.
- `frontend/templates/`: Contains HTML templates for all web pages using a clean dark layout.
- `frontend/static/css/style.css`: Provides styling, layout structure, cards, tables, and responsiveness.
- `frontend/static/js/main.js`: Handles modal popups, currency formatting, and form submissions.
- `experiments/`: Contains 10 separate folders (`experiment01` to `experiment10`), each containing the standalone Python code for that experiment.
- `tests/`: Automated unit and integration tests verifying all 10 experiments and web routes.

---

## 3. Adaptation of the 10 Experiments

### Experiment 01: PEAS Model & Financial State Space
**Original Concept:** Describing an intelligent agent using Performance Measure, Environment, Actuators, and Sensors, along with state space search graph exploration.  
**Why and Where Needed:** In this project, it is used on the Financial Advisor page to model a user's financial journey. The agent reads transaction inputs as sensors, tracks savings rate and budget compliance as performance measures, and suggests category spending caps as actuators. The state space defines milestone transitions from financial deficit to financial independence, helping users see the exact sequence of practical steps required to reach stability.

### Experiment 02: PROLOG Financial Rules & Queries
**Original Concept:** Declarative logic programming using facts, rules, and queries with automated inference and backtracking mechanisms in the PROLOG language.  
**Why and Where Needed:** Needed in the Advisory engine to apply standard financial planning rules without hardcoding complex nested conditions. Facts store user income, expenses, and savings balances. Rules check whether the emergency fund covers three months of living expenses, flag high-risk spending when expenses exceed safe limits, and verify if the user is ready to invest in mutual funds. It powers the safety checks shown on the advisor dashboard.

### Experiment 03: Uninformed Search (BFS & DFS)
**Original Concept:** Breadth-First Search using a queue data structure and Depth-First Search using a stack data structure to navigate connected graph nodes.  
**Why and Where Needed:** Needed in the Savings Goals module to calculate roadmaps across financial milestones. The graph connects unbudgeted spending to emergency reserves, debt clearance, and long-term targets. Breadth-First Search finds the path with the fewest milestone steps to reach a goal. Depth-First Search explores an intensive, single-focus debt elimination route. Users can compare both pathways directly inside the savings section to plan their personal financial goals.

### Experiment 04: Informed Search (A* Algorithm)
**Original Concept:** A* heuristic search evaluating f(n) = g(n) + h(n) with Manhattan distance to find the optimal path in minimal moves.  
**Why and Where Needed:** Needed in the Budget Management section to fix overspent discretionary categories such as dining out, shopping, and entertainment. The algorithm treats current spending levels as the start state and safe budget caps as the goal state. Using Manhattan distance between category limits, A* computes the exact step-by-step reduction plan with the least friction, showing users which categories to cut first to rebalance their monthly budget.

### Experiment 05: Adversarial Search (Minimax Algorithm)
**Original Concept:** Two-player game tree evaluation where MAX maximizes payoff and MIN minimizes payoff to find optimal decisions.  
**Why and Where Needed:** Needed in the Advisory module for financial stress testing against uncertain economic conditions. The user acts as the MAX player choosing between conservative or growth allocation strategies. Market inflation and unexpected emergency expenses act as the MIN player trying to reduce savings. Minimax evaluates all branch outcomes to calculate the guaranteed worst-case financial floor, helping users choose a resilient plan that withstands sudden expense spikes.

### Experiment 06: Fuzzy Logic Controller
**Original Concept:** Fuzzifying crisp numerical inputs into triangular membership sets and applying Mamdani centroid defuzzification to determine a crisp control action.  
**Why and Where Needed:** Needed in the Financial Overview and Advisor modules to calculate spending restriction levels. Real-world financial health cannot be captured by rigid yes-or-no rules. The controller fuzzifies expense-to-income ratios and savings rates into Low, Medium, and High sets. It then applies fuzzy rules and centroid defuzzification to generate a smooth restriction percentage (0% to 100%), telling users how strictly they should curb non-essential spending.

### Experiment 07: Mamdani vs Sugeno Fuzzy Inference
**Original Concept:** Comparing Mamdani FIS (centroid integration of fuzzy output sets) with Sugeno FIS (fast weighted average of constant values).  
**Why and Where Needed:** Needed in the Investment Risk section to calculate recommended equity portfolio allocations based on discretionary spending ratios. Mamdani evaluates continuous overlapping risk sets using centroid defuzzification, while Sugeno calculates the allocation through weighted averages. The project displays both outputs side by side on the advisor page, allowing users to see how different fuzzy inference methods determine investment aggressiveness while testing computational speed differences.

### Experiment 08: Hybrid Neuro-Fuzzy System
**Original Concept:** Combining a neural network (MLPRegressor) with a fuzzy logic controller using a weighted ensemble formula (0.6*ANN + 0.4*Fuzzy).  
**Why and Where Needed:** Needed in the Monthly Progress and Dashboard modules to estimate realistic monthly savings potential. The neural network learns non-linear spending patterns from multi-income historical data, while the fuzzy component enforces standard budgeting rules like the 50/30/20 guideline. Combining both predictions produces a reliable savings target tailored to the user's current income, displayed as a target amount and percentage on the dashboard to guide monthly savings.

### Experiment 09: Supervised Perceptron & Competitive Learning
**Original Concept:** Supervised Perceptron learning with weight updates and unsupervised competitive learning using Euclidean distance and winner-take-all neurons.  
**Why and Where Needed:** Needed in the Health Score and Analytics modules to evaluate spending habits. The supervised Perceptron classifies each month as disciplined or at-risk based on savings and expense adherence. The unsupervised competitive network groups monthly profiles into spending personas (Consistent Savers vs High Spenders) without needing manual labels. This lets the system automatically detect shifts in user spending behavior across different billing cycles over time.

### Experiment 10: Micro & Small Language Models
**Original Concept:** Building bigram (µLM) and trigram (SLM) statistical language models for next-word probability estimation and domain-specific text generation.  
**Why and Where Needed:** Needed in the Advisory interface to provide quick daily financial guidance and autocomplete suggestions. The models are trained on personal finance advice covering budgeting, emergency reserves, and investing. The bigram model predicts likely financial follow-up words, while the trigram model generates complete advisory sentences. It runs locally without external APIs, providing instant educational tips and search autocomplete directly within the local web application interface.

---

## 4. How to Run the Application

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Seed database with demo records
python services/seed_data.py

# 3. Start the application
python app.py
```

Open your browser and visit: `http://127.0.0.1:5000`
