from flask import Flask, request, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
import re
import pandas as pd
import sqlite3
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

import os
from os.path import join, dirname, realpath

ps = PorterStemmer()
stop_words = set(stopwords.words('indonesian'))


app = Flask(__name__)
app.config["DEBUG"] = True

UPLOAD_FOLDER = 'static/uploadFile'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'Data Cleansing'),
    'version' : LazyString(lambda: '1.0.0'),
    'description' : LazyString(lambda: 'Dokumentasi untuk Data Cleansing')
    },
    host = LazyString(lambda: request.host)    
)


swagger_config = {
    "headers":[],
    "specs": [
        {
            "endpoint" : 'docs',
            "route" : '/docs.json',
        }
    ],
    "static_url_path" : "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/" 
}
swagger = Swagger(app=app, config = swagger_config, template = swagger_template)


@swag_from("docs/1.yml", methods = ['POST'])
@app.route('/uploadFile', methods = ['POST'])
def uploadFile():
    upload_file = request.files['file']

    if upload_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_file.filename)
        upload_file.save(file_path)
        df = pd.read_csv(file_path, encoding = 'latin-1')
    return str(df)
    

@swag_from("docs/2.yml", methods = ['POST'])
@app.route('/textProcessing', methods = ['POST'])

def textProcessing():

    connection = sqlite3.connect('data/kamusalay.db')
    kamus_alay_df = pd.read_sql('''SELECT * FROM kamusalay;''', connection)
    connection.close()

    abusive = pd.read_csv('data/abusive.csv')

    text = request.form.get('text')

    clean_text = re.sub(r'[\W_0-9]', ' ', text.lower())
    stemmed_text = ' '.join([ps.stem(word) for word in clean_text.split() if not word in stop_words])

    json_response = {
        'status_code' : 200,
        'description' : 'Original Text',
        'data': stemmed_text
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == "__main__":
    app.run(debug=True, port=2003)