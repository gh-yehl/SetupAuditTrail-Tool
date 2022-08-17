from flask import Flask, render_template, request, Response, json, jsonify
import pandas as pd
import csv
from datetime import datetime

app = Flask(__name__, template_folder='./static/templates')
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        uploadedFile = request.files.get('myFile')
        data = pd.read_csv(uploadedFile, encoding= 'ISO-8859-1', index_col=None)

        #Save File
        data.to_csv('audit.csv', index=False)

        #Display default 300 rows
        result = data.head(300)
        data.columns = ['date','user','source','action','section','delegateUser']

        return render_template('index.html', test=convertList(result.values.tolist()))

    else:
        return render_template('index.html')


@app.route('/filterData', methods=['POST'])
def filterData():
    input_startDate = request.form.get('startDate')
    input_endDate = request.form.get('endDate')
    input_user = request.form.get('user')
    input_action = request.form.get('action')

    df = pd.read_csv('audit.csv', index_col=None)
    df.columns = ['date', 'user', 'source', 'action', 'section', 'delegateUser']

    # Specify input format
    df["date"] = df["date"].str[0:10]
    df['date'] = pd.to_datetime(df['date']) #, format='%d/%m/%Y'

    #Filter Data
    df = df[ ((df['date'] >= input_startDate) & (df['date'] <= input_endDate) )
             & (df['user'].str.contains(input_user))
             & (df['action'].str.contains(input_action))
             ]

    #Only display first/latest 300 rows on the page
    display_df = df.head(300)

    filteredList = convertList(display_df.values.tolist())
    json_str = json.dumps([x.dump() for x in filteredList])
    return json_str


def convertList(recordList):
    list = []
    for record in recordList:
        auditInfo = AuditInfo()
        auditInfo.date = record[0]
        auditInfo.user = record[1]
        auditInfo.source = record[2]
        auditInfo.action = record[3]
        auditInfo.section = record[4]
        auditInfo.delegateUser = record[5]
        list.append(auditInfo)
    return list


def downloadFile():
    uploadedFile = request.files.get('myFile')
    data = pd.read_csv(uploadedFile)
    return Response(
        data,
        mimetype='text/csv',
        headers={"Content-disposition": "attachment; filename=new-audit.csv"}
    )


class AuditInfo:
    def __init__(self):
        self.date = ''
        self.user = ''
        self.source = ''
        self.action = ''
        self.section = ''
        self.delegateUser = ''

    def dump(self):
        return {
                'date': self.date,
                'user': self.user,
                'source': self.source,
                'action': self.action,
                'section': self.section,
                'delegateUser': self.delegateUser
        }

if __name__ == '__main__':
    app.run()

