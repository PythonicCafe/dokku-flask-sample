import csv
import datetime
import io
import math
from urllib.request import urlopen

from db import execute_query


# Baixa dados do InfoDengue em formato CSV (calcula epiweek de maneira grosseira, para simplificar - é só um exemplo)
agora = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
epiweek = math.ceil((agora.date() - datetime.date(agora.year, 1, 1)).days / 7) - 1
city_code = 3304557  # Rio de Janeiro/RJ
desease = "dengue"
url = f"https://info.dengue.mat.br/api/alertcity/?geocode={city_code}&disease={desease}&format=csv&ew_start={epiweek - 1}&ey_start={agora.year}&ew_end={epiweek}&ey_end={agora.year}"
response = urlopen(url)

# Lê CSV e insere registros no banco
fobj = io.StringIO(response.read().decode("utf-8"))
sql = "INSERT INTO dengue (data, casos, populacao) VALUES (%s, %s, %s)"
registros = 0
for row in csv.DictReader(fobj, delimiter=","):
    execute_query(sql, (row["data_iniSE"], int(row["casos"]), int(row["pop"].split(".")[0])))
    registros += 1

# Insere log de captura
execute_query("INSERT INTO log_captura (datahora, registros) VALUES (%s, %s)", (agora, registros))
