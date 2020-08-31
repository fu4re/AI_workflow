import os, sqlite3
import pandas as pd

DIR_PATH = os.getcwd()
DB_NAME = "data\\students.sqlite"
CHUNK_SIZE = 2500

conn = sqlite3.connect(DB_NAME)
conn.text_factory = str
#  Объединяем таблицы с ежедневными и почасовыми данными
sql = "SELECT H.*, D.cnt AS day_cnt FROM hour AS H INNER JOIN day as D ON (H.dteday = D.dteday)"
DB_stream = pd.read_sql(sql, conn, chunksize=CHUNK_SIZE)

for j, data_chunk in enumerate(DB_stream):
    x, y = data_chunk.shape

    print(f"Порция {j + 1} - Размер загруженной порции данных: {x} прецедентов, {y} признаков")
    # Кор алгоритма