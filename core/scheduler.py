from collections import deque
from enum import Enum

from core.process import ProcessState

class SchedulingAlgorithm(Enum):
    FIFO = "FIFO"
    ROUND_ROBIN = "Round Robin"
    SJF = "Shortest Job First"

# Escalonador de Processos com múltiplos algoritmos
class Scheduler:
    def __init__(self, algorithms, quantum=2):
        # Algoritmos é uma lista de algoritmos para cada nível de fila hierárquica
        self.ready_queues = [deque() for _ in algorithms]
        self.algorithms = algorithms
        self.quantum = quantum
    
    def add_process(self, process, priority=0):
        """
        Adiciona um processo à fila de prontos de acordo com a prioridade.
        """
        self.ready_queues[priority].append(process)
        print(f"Processo {process.name} com PID {process.pid} adicionado à fila de prioridade {priority}")
    
    def get_next_process(self):
        """
        Seleciona o próximo processo baseado nas filas hierárquicas.
        """
        for i, queue in enumerate(self.ready_queues):
            if queue:
                algorithm = self.algorithms[i]
                if algorithm == SchedulingAlgorithm.FIFO:
                    return self._schedule_fifo(queue)
                elif algorithm == SchedulingAlgorithm.ROUND_ROBIN:
                    return self._schedule_round_robin(queue)
                elif algorithm == SchedulingAlgorithm.SJF:
                    return self._schedule_sjf(queue)
        return None

    def _schedule_fifo(self, queue):
        """
        Algoritmo FIFO: retorna o próximo processo na fila de prontos.
        """
        next_process = queue.popleft()  # Usa a fila fornecida
        next_process.state = ProcessState.EXECUTANDO
        print(f"Processo {next_process.name} com PID {next_process.pid} está sendo executado.")
        return next_process

    def _schedule_round_robin(self, queue):
        """
        Algoritmo Round Robin: retorna o próximo processo na fila de prontos e move o processo para o fim da fila
        se não terminar no quantum.
        """
        next_process = queue.popleft()  # Usa a fila fornecida
        next_process.state = ProcessState.EXECUTANDO
        print(f"Processo {next_process.name} com PID {next_process.pid} está sendo executado")

        remaining_instructions = len(next_process.instructions) - next_process.program_counter
        if remaining_instructions > self.quantum:
            # Executa até o quantum e depois move o processo para o final da fila
            next_process.program_counter += self.quantum
            queue.append(next_process)  # Move o processo para o final da fila
            print(f"Processo {next_process.name} não finalizou dentro do quantum e foi para o final da fila")
        else:
            # Executa as instruções restantes e termina o processo
            next_process.program_counter = len(next_process.instructions)
            self.process_completed(next_process)
            print(f"Processo {next_process.name} completou sua execução")

        return next_process

    def _schedule_sjf(self, queue):
        """
        Algoritmo SJF: seleciona o processo com o menor número de instruções restantes.
        """
        next_process = min(queue, key=lambda p: len(p.instructions) - p.program_counter)
        queue.remove(next_process)  # Remove o processo selecionado da fila
        next_process.state = ProcessState.EXECUTANDO
        print(f"Processo {next_process.name} com PID {next_process.pid} (Shortest Job) está sendo executado")
        return next_process

    def process_completed(self, process):
        """
        Marca um processo como terminado e o remove da fila de prontos.
        """
        process.state = ProcessState.FINALIZADO
        # Remove o processo das filas de prontos
        for queue in self.ready_queues:
            if process in queue:
                queue.remove(process)
                break
        print(f"Processo {process.name} com PID {process.pid} completou a execução")

    def display_ready_queue(self):
        """
        Exibe os processos em todas as filas de prontos.
        """
        print("Filas de prontos:")
        for priority, queue in enumerate(self.ready_queues):
            if queue:
                print(f"  Fila de prioridade {priority}:")
                for process in queue:
                    print(f"    PID: {process.pid}, Nome: {process.name}, Estado: {process.state.name}")
            else:
                print(f"  Fila de prioridade {priority} está vazia")
