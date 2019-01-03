import os
import json


def load_from_json(file):
    try:
        with open(file) as config:
            program_data = json.load(config)
        return program_data
    except FileNotFoundError:
        print("Nie znaleziono podanego pliku konfiguracyjnego!")
        exit(-1)


conf = os.getcwd() + "/config.json"
data = load_from_json(conf)
H = data["H"]
L = data["L"]
nH = data["nH"]
nL = data["nL"]
K = data["K"]
C = data["C"]
Ro = data["Ro"]
alfa = data["alfa"]
amb_temp = data["amb_temp"]
time_step = data["time_step"]
time = data["time"]
temp_start = data["temp_start"]
