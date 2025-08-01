from flask import Flask, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json, os

app = Flask(__name__)

# Google Sheets API scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from Render environment variable
creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)

# Authorize and open the sheet
client = gspread.authorize(creds)
sheet = client.open("Orders toronto py").worksheet("Orders")

@app.route('/')
def home():
    return jsonify({"status": "API running"})

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
