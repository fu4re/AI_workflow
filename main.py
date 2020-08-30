from UCI import unzip_from_UCI
from database_core import create_sqlite_db

UCI_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00320/student.zip"
unzip_from_UCI(UCI_url)

create_sqlite_db(db="data\\students.sqlite", file_pattern="data\\*.csv")