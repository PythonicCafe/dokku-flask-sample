import datetime
import json
import os
from pathlib import Path

from flask import Flask, request

from db import query_data


app = Flask(__file__)
DATA_PATH = Path(os.environ["DATA_PATH"])


@app.route("/")
def index():
    # Gera HTML com últimos 10 registros capturados
    html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Log de captura de dados</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap-theme.min.css" integrity="sha384-6pzBo3FDv/PJ8r2KRkGHifhEocL+1X2rVCTTkUfGk7/0pbek5mMa1upzvWbrUbOZ" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>
      </head>
      <body>
        <nav class="navbar navbar-default">
          <ul class="nav navbar-nav">
            <li class="active"> <a href="#">Página inicial</a> </li>
            <li> <a href="/logs">Logs de captura</a> </li>
          </ul>
        </nav>
        <div class="container">
          <p> Veja os dados capturados: </p>
          <table class="table table-striped table-bordered">
            <tr>
              <th> Data </th>
              <th> Casos </th>
              <th> População </th>
              <th> Casos/100k hab. </th>
            </tr>
    """
    for row in query_data("SELECT * FROM dengue ORDER BY data DESC LIMIT 10"):
        html += f"""
          <tr>
            <td> {row["data"]} </td>
            <td> {row["casos"]} </td>
            <td> {row["populacao"]} </td>
            <td> {100_000 * (row["casos"] / row["populacao"]):.2f} </td>
          </tr>
        """
    html += """
          </table>
        </div>
      </body>
    </html>
    """

    # Salva um arquivo JSON com informações do visitante no volume persistente
    filename = DATA_PATH / f"{datetime.datetime.now().isoformat()}.json"
    user_data = {
        "ip": request.environ.get("HTTP_X_FORWARDED_FOR", request.remote_addr),
        "user_agent": request.headers.get("User-Agent"),
    }
    with filename.open(mode="w") as fobj:
        json.dump(user_data, fobj)

    return html

@app.route("/logs")
def logs():
    html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Log de captura de dados</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap-theme.min.css" integrity="sha384-6pzBo3FDv/PJ8r2KRkGHifhEocL+1X2rVCTTkUfGk7/0pbek5mMa1upzvWbrUbOZ" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>
      </head>
      <body>
        <nav class="navbar navbar-default">
          <ul class="nav navbar-nav">
            <li> <a href="/">Página inicial</a> </li>
            <li class="active"> <a href="#">Logs de captura</a> </li>
          </ul>
        </nav>
        <div class="container">
          <p> Veja o log de captura de dados: </p>
          <table class="table table-striped table-bordered">
            <tr>
              <th> Data/hora </th>
              <th> Registros capturados </th>
            </tr>
    """
    for row in query_data("SELECT * FROM log_captura ORDER BY datahora DESC"):
        html += f"""
          <tr>
            <td> {row["datahora"].strftime("%d/%m/%Y %H:%M:%S")} </td>
            <td> {row["registros"]} </td>
          </tr>
        """
    html += """
          </table>
        </div>
      </body>
    </html>
    """
    return html
