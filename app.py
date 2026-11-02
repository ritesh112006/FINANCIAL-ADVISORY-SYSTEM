import os
import sys
import csv
import io
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, Response

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from database.db import get_db_connection, init_db
from services.financial_engine import FinancialEngine
from services.seed_data import seed_database

import experiments.experiment01.experiment01_agent as exp01
import experiments.experiment02.experiment02_expert_system as exp02
import experiments.experiment03.experiment03_uninformed_search as exp03
import experiments.experiment04.experiment04_informed_search as exp04
import experiments.experiment05.experiment05_adversarial_search as exp05
import experiments.experiment06.experiment06_fuzzy_controller as exp06
import experiments.experiment07.experiment07_mamdani_sugeno as exp07
import experiments.experiment08.experiment08_hybrid_neuro_fuzzy as exp08
import experiments.experiment09.experiment09_neural_learning_rules as exp09
import experiments.experiment10.experiment10_language_models as exp10

app = Flask(
    __name__,
    template_folder=os.path.join(ROOT_DIR, 'frontend', 'templates'),
    static_folder=os.path.join(ROOT_DIR, 'frontend', 'static')
)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'finwise-secret-key-2026')

init_db()

def get_current_month():
    return datetime.datetime.now().strftime('%Y-%m')

@app.context_processor
def inject_global_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM system_settings WHERE key = 'currency'")
    row = cursor.fetchone()
    currency = row["value"] if row else "₹"
    conn.close()
    return {
        "currency": currency,
        "current_month": get_current_month(),
        "now_year": datetime.datetime.now().year
    }

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    month = request.args.get('month', get_current_month())
    summary = FinancialEngine.get_summary_metrics(month)
    budget_status = FinancialEngine.get_budget_status(month)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, amount, type, category, description
        FROM transactions
        ORDER BY date DESC, id DESC
        LIMIT 6
    """)
    recent_txns = cursor.fetchall()

    cursor.execute("""
        SELECT id, title, target_amount, current_amount, target_date, status
        FROM savings_goals
        ORDER BY status ASC, id DESC
    """)
    goals = cursor.fetchall()
    conn.close()

    advisory_quick = FinancialEngine.get_comprehensive_ai_advisory(month)

    return render_template(
        'dashboard.html',
        summary=summary,
        budget_status=budget_status,
        recent_txns=recent_txns,
        goals=goals,
        advisory=advisory_quick,
        selected_month=month
    )

@app.route('/transactions')
def transactions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, amount, type, category, description
        FROM transactions
        ORDER BY date DESC, id DESC
    """)
    txns = cursor.fetchall()
    conn.close()
    return render_template('transactions.html', transactions=txns)

@app.route('/budgets')
def budgets():
    month = request.args.get('month', get_current_month())
    budget_status = FinancialEngine.get_budget_status(month)
    return render_template('budgets.html', budget_status=budget_status, selected_month=month)

@app.route('/savings')
def savings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, target_amount, current_amount, target_date, status
        FROM savings_goals
        ORDER BY id DESC
    """)
    goals = cursor.fetchall()
    conn.close()
    return render_template('savings.html', goals=goals)

@app.route('/advisory')
def advisory():
    month = request.args.get('month', get_current_month())
    advisory_data = FinancialEngine.get_comprehensive_ai_advisory(month)
    return render_template('advisory.html', advisory=advisory_data, selected_month=month)

@app.route('/continuous-improvement')
def continuous_improvement():
    history = FinancialEngine.get_continuous_improvement_history()
    advisory_data = FinancialEngine.get_comprehensive_ai_advisory()
    return render_template('continuous_improvement.html', history=history, advisory=advisory_data)

@app.route('/reports')
def reports():
    history = FinancialEngine.get_continuous_improvement_history()
    current_metrics = FinancialEngine.get_summary_metrics(get_current_month())
    return render_template('reports.html', history=history, metrics=current_metrics)

@app.route('/experiments')
def experiments():
    return render_template('experiments.html')

@app.route('/experiments/<int:exp_id>')
def experiment_detail(exp_id):
    if exp_id < 1 or exp_id > 10:
        return redirect(url_for('experiments'))
    return render_template('experiment_detail.html', exp_id=exp_id)

@app.route('/api/transactions', methods=['GET', 'POST'])
def api_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or request.form
        date = data.get('date') or datetime.date.today().isoformat()
        try:
            amount = float(data.get('amount', 0))
        except ValueError:
            return jsonify({'success': False, 'error': 'Enter a valid amount.'}), 400

        if amount <= 0:
            return jsonify({'success': False, 'error': 'Amount must be greater than zero.'}), 400

        txn_type = data.get('type', 'expense').lower()
        if txn_type not in ('income', 'expense'):
            return jsonify({'success': False, 'error': 'Invalid transaction type.'}), 400

        category = data.get('category', 'General').strip()
        description = data.get('description', '').strip()

        cursor.execute("""
            INSERT INTO transactions (date, amount, type, category, description)
            VALUES (?, ?, ?, ?, ?)
        """, (date, amount, txn_type, category, description))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': new_id, 'message': 'Transaction saved.'})

    cursor.execute("SELECT * FROM transactions ORDER BY date DESC, id DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({'success': True, 'transactions': rows})

@app.route('/api/transactions/<int:txn_id>', methods=['DELETE', 'PUT', 'POST'])
def api_transaction_modify(txn_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'DELETE' or (request.method == 'POST' and request.form.get('_method') == 'DELETE'):
        cursor.execute("DELETE FROM transactions WHERE id = ?", (txn_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Transaction deleted.'})

    data = request.get_json() or request.form
    date = data.get('date')
    amount = float(data.get('amount', 0))
    txn_type = data.get('type')
    category = data.get('category')
    description = data.get('description', '')

    cursor.execute("""
        UPDATE transactions
        SET date = ?, amount = ?, type = ?, category = ?, description = ?
        WHERE id = ?
    """, (date, amount, txn_type, category, description, txn_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Transaction updated.'})

@app.route('/api/budgets', methods=['POST'])
def api_save_budget():
    data = request.get_json() or request.form
    month = data.get('month', get_current_month())
    category = data.get('category')
    try:
        limit_amount = float(data.get('limit_amount', 0))
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid budget amount.'}), 400

    if not category or limit_amount < 0:
        return jsonify({'success': False, 'error': 'Category and limit amount are required.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO budgets (month, category, limit_amount)
        VALUES (?, ?, ?)
        ON CONFLICT(month, category) DO UPDATE SET limit_amount = excluded.limit_amount
    """, (month, category, limit_amount))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': f'Budget for {category} saved.'})

@app.route('/api/savings', methods=['POST'])
def api_create_goal():
    data = request.get_json() or request.form
    title = data.get('title', '').strip()
    try:
        target = float(data.get('target_amount', 0))
        current = float(data.get('current_amount', 0))
    except ValueError:
        return jsonify({'success': False, 'error': 'Enter valid numbers.'}), 400

    target_date = data.get('target_date', '')

    if not title or target <= 0:
        return jsonify({'success': False, 'error': 'Title and positive target amount required.'}), 400

    status = 'achieved' if current >= target else 'in_progress'

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO savings_goals (title, target_amount, current_amount, target_date, status)
        VALUES (?, ?, ?, ?, ?)
    """, (title, target, current, target_date, status))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Savings goal added.'})

@app.route('/api/savings/<int:goal_id>/deposit', methods=['POST'])
def api_deposit_savings(goal_id):
    data = request.get_json() or request.form
    try:
        deposit = float(data.get('amount', 0))
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid deposit amount.'}), 400

    if deposit <= 0:
        return jsonify({'success': False, 'error': 'Amount must be greater than zero.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT target_amount, current_amount FROM savings_goals WHERE id = ?", (goal_id,))
    goal = cursor.fetchone()
    if not goal:
        conn.close()
        return jsonify({'success': False, 'error': 'Goal not found.'}), 404

    new_amount = float(goal['current_amount']) + deposit
    new_status = 'achieved' if new_amount >= float(goal['target_amount']) else 'in_progress'

    cursor.execute("""
        UPDATE savings_goals
        SET current_amount = ?, status = ?
        WHERE id = ?
    """, (new_amount, new_status, goal_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'new_amount': new_amount, 'status': new_status})

@app.route('/reports/export-csv')
def export_csv():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, date, type, category, amount, description FROM transactions ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Transaction ID', 'Date', 'Type', 'Category', 'Amount (INR)', 'Description'])
    for r in rows:
        writer.writerow([r['id'], r['date'], r['type'], r['category'], r['amount'], r['description']])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=finwise_transactions.csv"}
    )

@app.route('/api/seed-database', methods=['POST'])
def api_seed_database():
    seed_database()
    return jsonify({'success': True, 'message': 'Database loaded with demo records.'})

@app.route('/api/experiments/run/<int:exp_id>', methods=['POST'])
def run_experiment_api(exp_id):
    payload = request.get_json() or {}

    try:
        if exp_id == 1:
            start_state = payload.get('start_state', 'Deficit')
            fss = exp01.FinancialStateSpace()
            res = fss.simulate_path(start_state)
            peas = exp01.FinWiseAgentPEAS.get_peas_description()
            return jsonify({'success': True, 'peas': peas, 'simulation': res})

        elif exp_id == 2:
            user_name = payload.get('user_name', 'custom')
            custom_data = payload.get('profile')
            engine = exp02.FinancialExpertSystem()
            res = engine.evaluate_user(user_name, custom_data=custom_data)
            return jsonify({'success': True, 'evaluation': res})

        elif exp_id == 3:
            start = payload.get('start_node', 'Unbudgeted_Cashflow')
            goal = payload.get('goal_node', 'Financial_Goal_Achieved')
            res = exp03.compare_search_algorithms(start, goal)
            return jsonify({'success': True, 'search_comparison': res})

        elif exp_id == 4:
            curr_dining = int(payload.get('dining', 18))
            curr_ent = int(payload.get('entertainment', 11))
            curr_shop = int(payload.get('shopping', 14))
            optimizer = exp04.BudgetAStarOptimizer()
            res = optimizer.a_star_solve((curr_dining, curr_ent, curr_shop))
            return jsonify({'success': True, 'a_star_result': res})

        elif exp_id == 5:
            tester = exp05.FinancialStressTester()
            res = tester.evaluate_stress_test()
            return jsonify({'success': True, 'stress_test': res})

        elif exp_id == 6:
            exp_ratio = float(payload.get('expense_ratio', 75.0))
            sav_rate = float(payload.get('savings_rate', 15.0))
            ctrl = exp06.FinancialFuzzyController()
            res = ctrl.evaluate(exp_ratio, sav_rate)
            return jsonify({'success': True, 'fuzzy_control': res})

        elif exp_id == 7:
            dsr = float(payload.get('discretionary_spending', 28.0))
            tester = exp07.ComparativeFISTester()
            res = tester.compare(dsr)
            return jsonify({'success': True, 'fis_comparison': res})

        elif exp_id == 8:
            income = float(payload.get('income', 75000.0))
            essential = float(payload.get('essential_expenses', 38000.0))
            advisor = exp08.HybridNeuroFuzzyAdvisor()
            res = advisor.predict(income, essential)
            return jsonify({'success': True, 'hybrid_prediction': res})

        elif exp_id == 9:
            sav = float(payload.get('savings_rate', 35.0))
            ess = float(payload.get('essential_discipline', 80.0))
            disc = float(payload.get('discretionary_control', 75.0))
            p = exp09.SupervisedFinancialPerceptron()
            p.train_default()
            p_res = p.predict(sav, ess, disc)
            c = exp09.UnsupervisedFinancialCompetitiveLearning()
            c.train_and_cluster()
            c_res = c.predict_cluster(sav, ess, disc)
            return jsonify({'success': True, 'perceptron': p_res, 'persona_clustering': c_res})

        elif exp_id == 10:
            word1 = payload.get('word1', 'emergency')
            word2 = payload.get('word2', 'fund')
            lm = exp10.FinancialLanguageModels()
            ulm_pred, ulm_prob = lm.ulm_predict_next_word(word1)
            slm_pred, slm_prob = lm.slm_predict_next_word(word1, word2)
            gen_text = lm.slm_generate_text(word1, word2, length=12)
            return jsonify({
                'success': True,
                'micro_lm': {'input': word1, 'predicted': ulm_pred, 'probability': ulm_prob},
                'small_lm': {'context': [word1, word2], 'predicted': slm_pred, 'probability': slm_prob},
                'generated_sentence': gen_text
            })

        else:
            return jsonify({'success': False, 'error': 'Invalid experiment index.'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"Server started on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=True)
