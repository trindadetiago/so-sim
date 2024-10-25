from enum import Enum
import itertools

# Definindo os estados possíveis de um processo
class ProcessState(Enum):
    PRONTO = "PRONTO"
    EXECUTANDO = "EXECUTANDO"
    AGUARDANDO = "AGUARDANDO"
    FINALIZADO = "FINALIZADO"

# Estrutura do Processo (PCB - Process Control Block)
class Process:
    _pid_counter = itertools.count(1)  # Gera PIDs únicos

    def __init__(self, instructions):
        self.pid = next(Process._pid_counter)
        self.state = ProcessState.PRONTO
        self.program_counter = 0
        self.registers = {'ACC': 0}
        self.instructions = instructions
        self.memory_allocated = []
        self.name = f"Process_{self.pid}"

    def __repr__(self):
        return (f"<Process {self.name} | PID: {self.pid} | State: {self.state.name} "
                f"| PC: {self.program_counter} | Instructions: {len(self.instructions)}>")
    
# Gerenciador de Processos
class ProcessManager:
    def __init__(self):
        self.processes = {}
        self.ready_queue = []

    def create_process(self, instructions):
        process = Process(instructions)
        self.processes[process.pid] = process
        self.ready_queue.append(process)
        print(f"Processo {process.name} criado com PID {process.pid}")
        return process  # Retorna o processo criado

    def terminate_process(self, pid):
        process = self.processes.get(pid)
        if process and process.state != ProcessState.FINALIZADO:
            process.state = ProcessState.FINALIZADO
            print(f"Processo {process.name} com PID {process.pid} foi finalizado")
        else:
            print(f"Processo com PID {pid} não encontrado ou já encontrado")

    def get_process_state(self, pid):
        process = self.processes.get(pid)
        if process:
            return process.state
        else:
            return None

    def list_processes(self):
        for pid, process in self.processes.items():
            print(process)