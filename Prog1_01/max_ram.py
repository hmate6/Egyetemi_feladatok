import psutil
import time

data = []

total = psutil.virtual_memory().total
total_round = round(total/1024**3, 2)

while True:
    data.append(bytearray(50_000_000))  # 50MB
    time.sleep(0.1)

    current = round(psutil.virtual_memory().used / 1024**3, 2)
    print(f"{current}Gb / {total_round}Gb felhasználva ")
