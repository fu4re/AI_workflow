import os
import pandas as pd

local_path = os.getcwd()
source = "data\\student-por.csv"
CHUNK_SIZE = 1000

with open(local_path + "\\" + source) as R:
    iterator = pd.read_csv(R, chunksize=CHUNK_SIZE)

    # Итератор определен, исходя из размера чанка, указанного в итераторе
    for n, data_chunk in enumerate(iterator):
        print("Размер загруженной порции данных: %i прецедентов, %i признаков" % data_chunk.shape)
        # Кор алгоритма
        pass

    print(f"Примеры значений: \n{str(data_chunk.iloc[0])}")
