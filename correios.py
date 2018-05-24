# -*- coding: utf-8 -*-
"""
correios.py
----------
    Api para usar dados dos Correios
"""
from flask import Flask, request, Response
# from flask.ext.cors import CORS, cross_origin
from flask_cors import CORS, cross_origin
import requests
import json
import os
from bson.json_util import dumps
from pymongo import MongoClient
# client = MongoClient(os.environ.get('DOCKER_HOST'), 27017)
# db = client.test_database
# enderecos = db.enderecos
# pessoas = db.pessoas

__version__ = '0.1.0'
__author__ = {
    'Luiz Junqueira': 'lcjneto@gmail.com',
}
app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/broker/auth', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def auth():
	data = {"token": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJsY2puZXRvQGdtYWlsLmNvbSIsImV4cCI6MTUyMDczMTA5NX0.4ggbTz0fJxB6NcxLDIY9wOige-19aTsSQDdn31SmncK6ggY1wRsFPdax4DmKKjXHVz6iylLfeYYloaP4EUsm1w",
			"user": {"email": "lcjneto@gmail.com",
			"last_login": "2018-03-04 01:04:04.589",
			"name": "roo",
			"username": "lcjneto@gmail.com"}
	}
	resp = Response(json.dumps(data))
	# resp.headers['Access-Control-Allow-Credentials'] = 'true'
	return resp


@app.route('/broker/profile', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def profile():
	data = {"hasSecurityPhrase": "false",
			"hasTwoFactor": "false",
			"localCurrencyLimit": '0',
			"securityPhrase": ''}
	resp = Response(json.dumps(data))
	return resp


@app.route('/correios/<cep>', methods=['GET'])
def findCep(cep):
    # cep = request.args.get('cep')
	url = 'http://cep.republicavirtual.com.br/web_cep.php?formato=' \
			'json&cep=%s' % str(cep)
	r = requests.get(url)
	if r.status_code == 200:
		resp = json.loads(r.content)  #decode('utf-8')
		correio = {"sucesso" : "true",
                   "endereco" :  { "cep" : str(cep),
                                "logr" : resp.get("logradouro"),
                                "compl" : resp.get("tipo_logradouro"),
                                "bairro" : resp.get("bairro"),
                                "cidade" : resp.get("cidade"),
                                "uf": resp.get("uf")}}
		enderecos.insert(correio.get('endereco'))
		return str(correio)
	else:
		return "vixi erro in correios :/"

@app.route('/cadastro', methods=['POST'])
def createPessoa(pessoa=None):
	pessoa = pessoa or {'_id': request.headers['cpf'],
			  			'nome': request.headers['nome'],
			  			'idade': request.headers['idade']}
	try:
		pessoas.insert(pessoa)
	except:
		pessoas.update({'_id': pessoa.get('_id')}, {"$set": pessoa}, upsert=False)
		pass
	return dumps(pessoa)

@app.route('/cadastro', methods=['GET'])
def showPessoas():
	return dumps(pessoas.find({}))

@app.route('/cadastro/<cpf>', methods=['GET'])
def findPessoa(cpf):
	return dumps(pessoas.find({'_id': cpf})[0])


if __name__ == '__main__':
    # Correios()
    app.run(debug=True, host='0.0.0.0', port=5004)