API Correios
============
    python correios_test.py
    version = 3.6

Run local
------------
    you can download the source from [GitHub][git] and run
    $ python correios.py

Correio
------------
=> http://localhost:5004/correios/04113000

Consulta da CEP:
    ● receber como parâmetro um CEP, acionar a URL: <https://viacep.com.br/ws/<CEP>/xml/>;
    ● gravar, em um mongoDB local, os campos “Bairro”, “Cidade”, “UF”, “CEP”, “Logradouro”, “Complemento”;

    Some simple examples of what api-correios code looks like:
    {“sucesso” : true,
     “endereco” :  {“cep” : <cep>,
                    “logr” : <logradouro>,
                    “compl” : <complemento>,
                    “bairro” : <bairro>,
                    “cidade” : <cidade>,
                    “uf”: <uf>
                }
    }

Pessoa
------------
    curl -X POST -H "cpf: 57823417936" -H "nome: joao" -H "idade: 23" http://localhost:5004/cadastro
