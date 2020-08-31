import os
import sqlite3, csv, glob


def define_field(s):
    try:
        int(s)
        return 'integer'
    except ValueError:
        try:
            float(s)
            return 'real'
        except:
            return 'text'


def create_sqlite_db(db='data\\database.sqlite', file_pattern=''):
    conn = sqlite3.connect(db)
    conn.text_factory = str  # Хранение файлов в кодировке UTF-8
    c = conn.cursor()

    # Обход и обработка файлов csv для последующего построения БД
    target_files = glob.glob(file_pattern)

    print(f"Создание {len(target_files)} таблиц(-ы) в {db} из файла(ов): {', '.join(target_files)}")

    for k, csvfile in enumerate(target_files):
        tablename = os.path.splitext(os.path.basename(csvfile))[0]

        with open(csvfile) as f:
            reader = csv.reader(f, delimiter=',')

            f.seek(0)
            for n, row in enumerate(reader):
                if n == 11:
                    types = map(define_field, row)
                else:
                    if n > 11:
                        break

            f.seek(0)
            for n, row in enumerate(reader):
                if n == 0:
                    # TODO: Пофиксить sql запросы (syntax-error)
                    sql = "DROP TABLE IF EXISTS %s" % tablename
                    c.execute(sql)
                    sql = "CREATE TABLE %s (%s)" % (tablename, ', '.join(["%s %s" % (col, ct) for col, ct in zip(row, types)]))
                    print(f"({k + 1}) {sql}")
                    c.execute(sql)

                    for column in row:
                        if column.endswith("_ID_hash"):
                            index = "%s__%s" % (tablename, column)
                            sql = "CREATE INDEX %s on %s (%s)" % (index, tablename, column)
                            c.execute(sql)

                    insertsql = "INSERT INTO %s VALUES (%s)" % (tablename, ', '.join(["?" for column in row]))
                    rowlen = len(row)
                else:
                    # Ошибка, если строки с неправильным числом полей
                    if len(row) == rowlen:
                        c.execute(insertsql, row)
                    else:
                        print(f"Ошибка в строке {n} в файле {csvfile}")
                        raise ValueError(f"Неверное значение в строке {n}")

            conn.commit()
            print(f"Вставлено {n} строк")

    c.close()
    conn.close()





