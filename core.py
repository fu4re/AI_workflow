import os, csv

local_path = os.getcwd()
source = "data\\student-mat.csv"
#SEP = str(',')  # Для замены на другой разделитель

with open(local_path + "\\" + source) as R:
    iterator = csv.reader(R, delimiter=',')
    for n, row in enumerate(iterator):
        if n == 0:
            header = row
        else:
            # Кор алгоритма
            pass

    print(f"Всего строк: {n + 1}")
    print(f"Заголовок: {', '.join(header)}")
    print(f"Примеры значений: {', '.join(row)}")
