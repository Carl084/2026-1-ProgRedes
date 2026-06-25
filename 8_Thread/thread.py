import threading

'''
def tarefa():
    print("Executando thread")

t = threading.Thread(target=tarefa)

t.start() # chama internamente run() em uma nova thread de execução
'''

'''
def saudacao(nome):
    print(f"Olá {nome}")

t = threading.Thread(
    target=saudacao,
    args=("Carlos",)
)

t.start()
'''

'''
def tarefa(numero):
    print(f"Thread {numero}")

for i in range(5):
    t = threading.Thread(
        target=tarefa,
        args=(i,)
    )
    t.start()
'''

'''
import time

def tarefa():
    time.sleep(3)
    print("FIM")

t = threading.Thread(target=tarefa)

t.start()

t.join() # Bloquea até a thread terminara

print("Programa encerrado")
'''

'''
def tarefa():
    print(
        threading.current_thread().name # Descobre qual thread está em execução
    )

threading.Thread(
    target=tarefa,
    name="Thread-A"
).start()
'''

'''
contador = 0
lock = threading.Lock()
# Lock serve para proteger recursos compartilhados, sem ela, as duas threads 
# podem alterar ao mesmo tempo e não sair com valor esperado 

def incrementar():
    global contador

    for _ in range(100000):
        with lock: # Executar com Lock ligado
            contador += 1

threads = [] # Adicionar os threads a trabalhar

for _ in range(5):
    t = threading.Thread(target=incrementar)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(contador)
'''


