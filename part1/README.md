# Datalake Backend Challenge Part 1/2

Esta parte do teste consiste na construção de uma API web, que seja capaz de ignorar solicitações com o mesmo corpo em um curto espaço de tempo (10 minutos).

Foi construído usando Python com auxilio da biblioteca Flask

Como base de dados, foi utilizado um json, algo simples para a resolução do problema, a mesma base de dados  são utilizados nos testes.

## Pré-requisitos
- [Flask]{https://pypi.org/project/Flask/}
- [Python 3.8.2]{https://www.python.org/downloads/}


## Executando os testes


```bash
python3 test_app.py
```


## Rodando aplicação

Essa aplicação ira executar uma aplicação web simples, onde irá exibir e cadastrar produtos ignorando requisições com o mesmo corpo no espaço de 10 min.

Formato do json esperado:
```json
"id": "product_id",
"name": "product_name"
```

Para executar aplicação basta rodar o script `app.py` utilizando o Python. A aplicação web será levantada no endereço "127.0.0.1:5000".

```bash
python3 app.py
```
