import numpy as np
import random

class Processo(object):
    def __init__(self, pnome, pio, ptam, prioridade, tempoChegada):
        self.nome = pnome
        self.io = pio
        self.tam = ptam
        self.prio = prioridade
        self.chegada = tempoChegada  

    def roda(self, quantum=None):
        if random.randint(1, 100) < self.io:
            self.tam -= 1
            print(self.nome, "fez e/s, falta", self.tam)
            return 1, True

        if quantum is None or self.tam < quantum:
            quantum = self.tam
        self.tam -= quantum
        print(self.nome, "rodou por", quantum, "timeslice, faltam", self.tam)
        return quantum, self.tam <= 0

class EscalonadorRoundRobin:
    def __init__(self, vprontos=[]):
        self.prontos = vprontos

    def pronto(self, processo):
        self.prontos.append(processo)

    def proximo(self):
        if self.prontos:
            return self.prontos.pop(0)
        return None

# Criação de processos
nprocs = 4
nomes = ['A', 'B', 'C', 'D']
chanceio = [0, 0, 0, 0]
tamanho = np.array([10, 20, 30, 40])

procs = []
for i in range(nprocs):
    procs.append(Processo(nomes[i], chanceio[i], tamanho[i], 0, 0))

quantum = 2

escalonador = EscalonadorRoundRobin(procs)

total = sum([p.tam for p in procs])
tempo = 0
tempo_final = 0

while total > 0:
    p = escalonador.proximo()
    if p is not None:
        rodou, terminou = p.roda(quantum)
        total -= rodou
        tempo += rodou

        if p.tam == 0: 
            tempo_final += tempo

        if not terminou:
            escalonador.pronto(p)


print("Tempo medio execucao (round robin)", tempo_final/nprocs)