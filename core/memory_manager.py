import time

class MemoryManager:
    def __init__(self, max_physical_memory):
        self.max_physical_memory = max_physical_memory
        self.physical_memory = {}  # PID -> Processo
        self.virtual_memory = {}   # PID -> Processo
        self.access_history = []   # Histórico de acesso para política de substituição
    
    def add_process(self, process):
        if len(self.physical_memory) < self.max_physical_memory:
            self.physical_memory[process.pid] = process
            self.access_history.append(process.pid)
            print(f"Processo PID {process.pid} adicionado à memória física.")
        else:
            self.move_to_virtual_memory(process)

    def move_to_virtual_memory(self, process):
        if len(self.physical_memory) >= self.max_physical_memory:
            pid_to_move = self.choose_process_to_swap()
            swapped_process = self.physical_memory.pop(pid_to_move)
            self.virtual_memory[pid_to_move] = swapped_process
            print(f"Processo PID {pid_to_move} movido para a memória virtual.")

            # Simular o atraso na movimentação
            self.simulate_copy_delay()

        # Agora, adicionar o novo processo à memória física
        self.physical_memory[process.pid] = process
        self.access_history.append(process.pid)
        print(f"Processo PID {process.pid} adicionado à memória física após swap.")


    def simulate_copy_delay(self):
        """
        Simula o atraso durante a cópia de um processo para a memória virtual.
        """
        print("Movendo processo para a memória virtual, por favor aguarde...")
        time.sleep(1)  # Pausa de 1 segundo para simular o custo de cópia
        print("Processo movido com sucesso.")
    
    def choose_process_to_swap(self):
        return self.access_history.pop(0)  # Exemplo com FIFO
