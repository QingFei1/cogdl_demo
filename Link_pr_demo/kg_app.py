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

@app.route('/kgdemo/graph',methods = ['POST', 'GET'])
def KG_View():
    select=1
    if request.method == 'POST':
        result = request.form
        entity=result.get('entity')
    url = 'https://api.ownthink.com/kg/knowledge?entity=%s' % entity  
    sess = requests.get(url)  
    text = sess.text 
    response = eval(text)  
    knowledge = response['data']
    try:
        en=knowledge['entity']
    except:
        key='0'
        return render_template('index.html',key=key,select=select)
    nodes = []
    for avp in knowledge['avp']:
        if avp[1] == knowledge['entity']:
            continue
        node = {'source': knowledge['entity'], 'target': avp[1], 'type': "resolved", 'rela': avp[0]}
        nodes.append(node)
    nodes_new=''
    li=[]
    for node in nodes:
        node = str(node)
        node = node.replace("'type'", 'type').replace("'source'", 'source').replace("'target'", 'target')
        nodes_new+=node+','
        li.append(node)
    entity=json.dumps(nodes,ensure_ascii=False)
    return render_template('index.html',entity=entity,select=select)

@app.route('/kgdemo/pre_tail',methods = ['POST', 'GET'])
def pre_tail():
    select=2
    if request.method == 'POST':
        result = request.form
        entity=result.get('entity_test')
        relation=result.get('relation_test')
    url = 'https://api.ownthink.com/kg/knowledge?entity=%s' % entity  

    sess = requests.get(url)  
    text = sess.text  
    response = eval(text) 
    knowledge = response['data']
    try:
        entity_new=knowledge['entity']
        pre=test_score.rank(entity_new,relation)
    except:
        try:
            pre=test_score.rank(entity,relation)
        except:
            key='0'
            return render_template('index.html',key=key,select=select)
    pre=json.dumps(pre,ensure_ascii=False)
    
    return render_template('index.html',entity=entity_new,relation=relation,tail=pre,select=select)



@app.route('/kgdemo/pre_smi',methods = ['POST', 'GET'])
def pre_smi():
    select=3
    if request.method == 'POST':
        result = request.form
        entity=result.get('entity_smi')
    url = 'https://api.ownthink.com/kg/knowledge?entity=%s' % entity 

    sess = requests.get(url)  
    text = sess.text 
    response = eval(text)
    knowledge = response['data']
    try:
        entity_new=knowledge['entity']
        pre_smi=test_score.smi(entity_new)
    except:
        try:
            pre_smi=test_score.smi(entity)
        except:
            key='0'
            return render_template('index.html',key=key,select=select)
    pre_smi=json.dumps(pre_smi,ensure_ascii=False)
    return render_template('index.html',entity=entity_new,pre_smi=pre_smi,select=select)



if __name__ == '__main__':
    #app.run(host='127.0.0.1',port=5000,debug = True)
    app.run(host='0.0.0.0',port=5000,debug=app.config["DEBUG"], threaded=True)
    #app.run(host='127.0.0.1',port=8999,debug=True)

