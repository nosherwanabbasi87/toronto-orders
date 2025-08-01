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
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, jsonify

app = Flask(__name__)

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Orders toronto py").worksheet("Orders")

@app.route('/stats', methods=['GET'])
def stats():
    data = sheet.get_all_records()

    total_orders = len(data)
    total_revenue = sum(float(row.get("Sale price", 0) or 0) for row in data)
    total_profit = sum(float(row.get("Profit", 0) or 0) for row in data)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    return jsonify({
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "average_order_value": avg_order_value
    })

@app.route('/')
def home():
    return jsonify({"status": "API running"})
