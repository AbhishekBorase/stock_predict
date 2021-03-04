#!/usr/bin/python
# coding: utf-8
from flask import Flask, jsonify, request
from templates import logic
from datetime import date

app = Flask(__name__)


@app.route('/predict/<string:stock>/<int:y>/<int:m>/<int:d>')
def signup(stock, y, m, d):
    start_date = date(y, m, d)
    e = start_date.strftime("%Y-%m-%d")
    print(e)
    dataframe = logic.model(stock, e)
    print(dataframe)
    buy, sell, flag = logic.buy_sell_short(dataframe)
    if len(buy) != 0:
        buyFlag = True
    else:
        buyFlag = False
    if len(sell) != 0:
        sellFlag = True
    else:
        sellFlag = False

    result = {
        "Buy": buyFlag,
        "Sell": sellFlag,
        "Flag": flag
    }
    print(result)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
