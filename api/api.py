from flask import Flask, jsonify

from report.service import get_daily_report

app = Flask(__name__)

import logging
from datetime import datetime


@app.route('/report/<date>', methods=['GET'])
def get_report(date):
    try:
        if date.isdigit():
            # If the date parameter is a digit, it's a timestamp
            date_str = datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d')
        else:
            # Otherwise, assume it's a datetime string
            date_str = datetime.strptime(date, '%Y-%m-%d').date().isoformat()
    except ValueError:
        logging.error("Invalid date format received in the URL: {}".format(date))
        return jsonify({'error': 'Invalid date format received in the URL: {}'.format(date)}), 400

    get_report = get_daily_report(date_str)
    if get_report:
        return jsonify(get_report), 200
    return {"message": 'DAILY_REPORT_FAILED'}, 500
