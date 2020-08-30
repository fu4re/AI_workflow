import requests, io, os
import numpy as np
import tarfile, zipfile, gzip


def unzip_from_UCI(UCI_url, dest=''):
    response = requests.get(UCI_url)
    compressed_file = io.BytesIO(response.content)
    z = zipfile.ZipFile(compressed_file)
    print(f"Извлечение в {os.getcwd()}" + "\\" + dest)
    for name in z.namelist():
        if '.csv' in name:
            print(f"\tРаспакован {name}")
            z.extract(name, os.getcwd() + "\\" + dest)


def gzip_from_UCI(UCI_url):
    response = requests.get(UCI_url)
    compressed_file = io.BytesIO(response.content)
    decompressed_file = gzip.GzipFile(fileobj=compressed_file)
    filename = UCI_url.split('/')[-1][:-3]
    with open(os.getcwd() + "\\" + filename, 'wb') as outfile:
        outfile.write(decompressed_file.read())
    print(f"Файл {filename} разархивирован")


def targzip_from_UCI(UCI_url, dest=''):
    response = requests.get(UCI_url)
    compressed_file = io.BytesIO(response.content)
    tar = tarfile.open(mode='r:gz', fileobj=compressed_file)
    tar.extractall(path=dest)
    datasets = tar.getnames()
    for dataset in datasets:
        size = os.path.getsize(dest + "\\" + dataset)
        print(f"Файл {dataset} составляет {size} байт")
    tar.close()


def load_matrix(UCI_url):
    return np.loadtxt(requests.get(UCI_url).text)
