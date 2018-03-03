# -*- coding: utf-8 -*-
"""
correios.py
----------
    Api para usar dados dos Correios
"""
from flask import Flask, request
import requests
import json
import os
from bson.json_util import dumps
from pymongo import MongoClient
client = MongoClient(os.environ.get('DOCKER_HOST'), 27017)
db = client.test_database
enderecos = db.enderecos
pessoas = db.pessoas

__version__ = '0.1.0'
__author__ = {
    'Luiz Junqueira': 'lcjneto@gmail.com',
}
app = Flask(__name__)


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