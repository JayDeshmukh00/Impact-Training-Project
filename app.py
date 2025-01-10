from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Load or initialize transaction data
def load_data():
    try:
        with open("transactions.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(transactions):
    with open("transactions.json", "w") as file:
        json.dump(transactions, file)

@app.route('/')
def index():
    transactions = load_data()
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    balance = total_income - total_expenses
    categories = {}
    for t in transactions:
        if t['type'] == 'expense':
            categories[t['category']] = categories.get(t['category'], 0) + t['amount']

    return render_template('index.html', transactions=transactions, balance=balance,
                           total_income=total_income, total_expenses=total_expenses, categories=categories)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    amount = float(request.form['amount'])
    category = request.form['category']
    transaction_type = request.form['type']
    date = request.form['date']

    transaction = {
        'amount': amount,
        'category': category,
        'type': transaction_type,
        'date': date
    }

    transactions = load_data()
    transactions.append(transaction)
    save_data(transactions)

    return redirect(url_for('index'))

@app.route('/api/transactions')
def api_transactions():
    transactions = load_data()
    return jsonify(transactions)

if __name__ == "__main__":
    app.run(debug=True)
