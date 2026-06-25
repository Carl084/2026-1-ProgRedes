import threading

def tarefa():
    print("Executando thread")

t = threading.Thread(target=tarefa)

t.start()