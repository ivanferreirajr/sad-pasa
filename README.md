# Problema de Alocação de Salas de Aula

## Objetivo
O principal objetivo é aumentar a efetividade da distribuição de salas de uma universidade. O problema estudo é enominado Problema da Alocação de Salas de Aula (PASA) é um subproblema do Problemas da Tabela de Horários de Cursos Universitários.

## Tecnologias
- Python
- Streamlit
- Pandas
- Psycopg

## Guia de Instalação

Você precisará de Python 3 e pip. É recomendado utilizar ambientes virtuais com o virtualenv e o arquivo `requirements.txt` para instalar os pacotes dependências:

Linux

```bash
$ pip3 install virtualenv
$ virtualenv venv -p python3
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Windows

```bash
> pip3 install virtualenv
> virtualenv ..\venv -p python
> ..\venv\Scripts\Activate.psl
> pip install -r requirements.txt
```

Quando finalizado, você pode desativar o ambiente virtual do virtualenv com:

```bash
$ deactivate
```

Depois da instalação dos pacotes necessários, é preciso criar um arquivo `.env` no diretório raiz do projeto seguindo o padrão definido no `example.env`. Nesse arquivo adicione as informações necessárias para configuração do banco de dados.

Para executar o programa, basta usar o seguinte comando:

```bash
$ streamlit run src/app.py
```

## Deploy

- [Deploy on Heroku](https://sad-pasa.herokuapp.com/) 🚀

---
Obs: Os dados são fictícios, mas tentam representar a realidade de uma base de turmas e salas da UFS