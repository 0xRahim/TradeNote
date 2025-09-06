from flask import Blueprint, jsonify

events_bp = Blueprint('events', __name__)

@events_bp.route('/', methods=['GET'])
def get_events():
    mock_response = [
        {
            "date": "2024-07-22",
            "events": [
                {"type": "earnings", "time": "BMO", "symbol": "UEC", "details": "UEC Uranium Energy Corp Earnings"},
                {"type": "data", "time": "08:30", "details": "Chicago Fed National Activity Index"}
            ]
        },
        {
            "date": "2024-07-23",
            "events": [
                {"type": "earnings", "time": "BMO", "symbol": "GE", "details": "General Electric Co Earnings"},
                {"type": "data", "time": "09:00", "details": "S&P Case-Shiller Home Price Index"}
            ]
        }
    ]
    return jsonify(mock_response)
