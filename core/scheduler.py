from collections import deque
from enum import Enum

from core.process import ProcessState

class SchedulingAlgorithm(Enum):
    FIFO = "FIFO"
    ROUND_ROBIN = "Round Robin"
    SJF = "Shortest Job First"

# Escalonador de Processos com múltiplos algoritmos
class Scheduler:
    def __init__(self, algorithm=SchedulingAlgorithm.FIFO, quantum=2):
        self.ready_queue = deque()
        self.algorithm = algorithm
        self.quantum = quantum

    def add_process(self, process):
        """
        Adiciona um processo à fila de prontos.
        """
        self.ready_queue.append(process)
        print(f"Processo {process.name} com PID {process.pid} adicionado à fila de prontos")

    def get_next_process(self):
        """
        Seleciona o próximo processo a ser executado de acordo com o algoritmo de escalonamento escolhido.
        """
        if not self.ready_queue:
            print("Sem processos na fila de prontos")
            return None

        if self.algorithm == SchedulingAlgorithm.FIFO:
            return self._schedule_fifo()
        elif self.algorithm == SchedulingAlgorithm.ROUND_ROBIN:
            return self._schedule_round_robin()
        elif self.algorithm == SchedulingAlgorithm.SJF:
            return self._schedule_sjf()

    def _schedule_fifo(self):
        """
        Algoritmo FIFO: retorna o próximo processo na fila de prontos.
        """
        next_process = self.ready_queue.popleft()
        next_process.state = ProcessState.EXECUTANDO
        print(f"Processo {next_process.name} com PID {next_process.pid} está sendo executado.")
        return next_process

    def _schedule_round_robin(self):
        """
        Algoritmo Round Robin: retorna o próximo processo na fila de prontos e move o processo para o fim da fila
        se não terminar no quantum.
        """
        next_process = self.ready_queue.popleft()
        next_process.state = ProcessState.EXECUTANDO
        print(f"Processo {next_process.name} com PID {next_process.pid} está sendo executado")

        remaining_instructions = len(next_process.instructions) - next_process.program_counter
        if remaining_instructions > self.quantum:
            # Executa até o quantum e depois move o processo para o final da fila
            next_process.program_counter += self.quantum
            self.ready_queue.append(next_process)
            print(f"Processo {next_process.name} não finalizou dentro do quantum e foi para o final da fila")
        else:
            # Executa as instruções restantes e termina o processo
            next_process.program_counter = len(next_process.instructions)
            self.process_completed(next_process)
            print(f"Processo {next_process.name} completou sua execução")

        return next_process


    def _schedule_sjf(self):
        """
        Algoritmo SJF: seleciona o processo com o menor número de instruções restantes.
        """
        next_process = min(self.ready_queue, key=lambda p: len(p.instructions) - p.program_counter)
        self.ready_queue.remove(next_process)
        next_process.state = ProcessState.EXECUTANDO
        print(f"Processo {next_process.name} com PID {next_process.pid} (Shortest Job) está sendo executado")
        return next_process

    def process_completed(self, process):
        """
        Marca um processo como terminado.
        """
        process.state = ProcessState.FINALIZADO
        print(f"Processo {process.name} com PID {process.pid} completou a execução")

    def display_ready_queue(self):
        """
        Exibe os processos na fila de prontos.
        """
        if self.ready_queue:
            print("Ready Queue:")
            for process in self.ready_queue:
                print(f"  PID: {process.pid}, Nome: {process.name}, Estado: {process.state.name}")
        else:
            print("Fila de prontos está vazia")