import json

from flask import Flask, render_template, request, jsonify
from flask.views import View
import requests
import test_score
app = Flask(__name__,static_folder='kgdemo/static',static_url_path='/kgdemo/static')
app.config['JSON_AS_ASCII']=False

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/kgdemo/pre_tail',methods = ['POST', 'GET'])
def pre_tail():
    select=1
    if request.method == 'POST':
        result = request.form
        entity=result.get('entity_test')
        relation=result.get('relation_test')
    try:
        pre=test_score.rank(entity,relation)
    except:
        key='0'
        return render_template('index.html',key=key,select=select)
    pre=json.dumps(pre,ensure_ascii=False)
    
    return render_template('index.html',entity=entity,relation=relation,tail=pre,select=select)



@app.route('/kgdemo/pre_smi',methods = ['POST', 'GET'])
def pre_smi():
    select=2
    if request.method == 'POST':
        result = request.form
        entity=result.get('entity_smi')
    try:
        pre_smi=test_score.smi(entity)
    except:
        key='0'
        return render_template('index.html',key=key,select=select)
    pre_smi=json.dumps(pre_smi,ensure_ascii=False)
    return render_template('index.html',entity=entity,pre_smi=pre_smi,select=select)



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5333,debug = True)
    #app.run(host='0.0.0.0',port=5000,debug=app.config["DEBUG"], threaded=True)

