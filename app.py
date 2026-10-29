from flask import Flask, jsonify, request

app = Flask(__name__)
app.balance = 0.0

@app.route("/")
def home():
    return jsonify(message="Simple Banking Application", balance=app.balance)

@app.route("/health")
def health():
    return jsonify(status="healthy"), 200

@app.route("/balance", methods=["GET"])
def check_balance():
    return jsonify(balance=app.balance), 200

@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.get_json(silent=True) or {}
    amount = data.get("amount")

    if amount is None:
        return jsonify(error="Amount is required."), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify(error="Amount must be a number."), 400

    if amount <= 0:
        return jsonify(error="Deposit amount must be greater than zero."), 400

    app.balance += amount
    return jsonify(message="Deposit successful", balance=app.balance), 200

@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json(silent=True) or {}
    amount = data.get("amount")

    if amount is None:
        return jsonify(error="Amount is required."), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify(error="Amount must be a number."), 400

    if amount <= 0:
        return jsonify(error="Withdrawal amount must be greater than zero."), 400

    if amount > app.balance:
        return jsonify(error="Insufficient funds."), 400

    app.balance -= amount
    return jsonify(message="Withdrawal successful", balance=app.balance), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)