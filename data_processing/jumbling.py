import os
import zlib
from random import shuffle
import pandas as pd
import numpy as np


#  В оперативной памяти
def ram_shuffle(filename_in, filename_out, header=True):
    with open(filename_in, 'rb') as f:
        #  Открываем файл для побитового чтения и сжимаем строку
        zlines = [zlib.compress(line, 9) for line in f]
        if header:
            first_row = zlines.pop(0)
    shuffle(zlines)

    with open(filename_out, 'wb') as f:
        if header:
            f.write(zlib.decompress(first_row))
        for zline in zlines:
            f.write(zlib.decompress(zline))


#  На диске
def disk_shuffle(filename_in, filename_out, header=True,
                 iterations=3, CHUNK_SIZE=2500, SEP=','):
    for i in range(iterations):
        with open(filename_in, 'rb') as R:
            iterator = pd.read_csv(R, chunksize=CHUNK_SIZE)
            for n, df in enumerate(iterator):
                if n == 0 and header:
                    header_cols = SEP.join(df.columns) + '\n'
                # Вызываем представление iloc из pandas на основе permutation из numpy, которая
                # перемешивает массив(или подмассив) по его длине в его копии(!), с сохранением исходных данных
                df.iloc[np.random.permutation(len(df))].to_csv(str(n) + "_chunk.csv",
                                                               index=False, header=False, sep=SEP)
        ordering = list(range(0, n + 1))
        shuffle(ordering)

        with open(filename_out, 'w') as W:
            if header:
                W.write(header_cols)
            for f in ordering:
                with open(str(f) + "_chunk.csv", 'r') as R:
                    for line in R:
                        W.write(line)
                os.remove(str(f) + "_chunk.csv")  # Убираем копии

        filename_in = filename_out
        CHUNK_SIZE = int(CHUNK_SIZE / 2)


'''
local_path = os.getcwd()
source = "data\\hour.csv"

ram_shuffle(filename_in=local_path + "\\" + source, filename_out=local_path + "\\" + "\\data\\shuffled_hour.csv")
disk_shuffle(filename_in=local_path + "\\" + source, filename_out=local_path + "\\" + "\\data\\shuffled_hour.csv",
             header=True)
'''
