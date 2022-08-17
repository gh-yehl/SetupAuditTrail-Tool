from flask import Flask, render_template, request, Response
import pandas as pd
import csv

app = Flask(__name__)

@app.route('/audit', methods=['GET', 'POST'])

def audit():
    print('start')
    data = [1, 2]
    records = pd.DataFrame.from_records(data, columns=['A', 'B'])
    records.to_csv('test.csv')

    return Response(
            records,
            mimetype='text/csv',
            headers={"Content-disposition": "attachment; filename=new-audit.csv"}
        )

    return render_template('index.html')


def downloadFile():
    uploadedFile = request.files.get('myFile')
    data = pd.read_csv(uploadedFile)
    return Response(
        data,
        mimetype='text/csv',
        headers={"Content-disposition": "attachment; filename=new-audit.csv"}
    )



if __name__ == '__main__':
    app.run()