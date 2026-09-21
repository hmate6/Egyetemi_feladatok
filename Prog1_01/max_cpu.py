import multiprocessing

def cpu_while():
    while True:
        pass

if __name__ == "__main__":
    folyamatok = []
    logikai_cpuk = multiprocessing.cpu_count()

    for x in range(logikai_cpuk):
        p = multiprocessing.Process(target=cpu_while)
        p.start()
        folyamatok.append(p)
