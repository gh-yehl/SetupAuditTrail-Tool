from flask import Flask, render_template, request, Response, make_response, json, jsonify
import pandas as pd
import csv

app = Flask(__name__)
'''避免中文 显示成为 ASCII'''
app.config['JSON_AS_ASCII'] = False

@app.route('/index')

def index():
    data = {
        'name': 'herman',
        'gender': '男'
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run()