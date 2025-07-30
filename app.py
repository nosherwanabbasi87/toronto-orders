from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "API running"})

@app.route('/weekly-profit', methods=['GET'])
def weekly_profit():
    # Replace with your Google Sheets logic
    total_profit = 1234.56
    return jsonify({"weekly_profit": total_profit})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
