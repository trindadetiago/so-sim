from core.process import ProcessState
import time

class VM:
    def __init__(self, scheduler, memory_manager=None):
        self.scheduler = scheduler
        self.memory_manager = memory_manager

    def execute(self):
        """
        Ciclo principal de execução da VM.
        """
        while True:
            # Obtém o próximo processo a ser executado
            process = self.scheduler.get_next_process()
            if not process:
                print("Nenhum processo restante para executar.")
                break  # Nenhum processo restante para executar

            # Verifica se o processo já foi finalizado
            if process.state == ProcessState.FINALIZADO:
                continue

            # Ciclo de execução do processo
            while process.state == ProcessState.EXECUTANDO:
                self.execute_instruction(process)

                # Se o processo completar todas as instruções
                if process.program_counter >= len(process.instructions):
                    self.scheduler.process_completed(process)
                    break

            # Verifica se todas as filas estão vazias ou todos os processos foram finalizados
            if all(p.state == ProcessState.FINALIZADO for queue in self.scheduler.ready_queues for p in queue):
                print("Todos os processos foram finalizados.")
                break

    def execute_instruction(self, process):
        """
        Executa a instrução atual do processo.
        """
        if process.state == ProcessState.FINALIZADO:
            return  # Não executar instruções de um processo finalizado

        instruction = process.instructions[process.program_counter]
        print(f"Executando instrução: {instruction} para processo PID {process.pid}")

        # Simular a execução de diferentes tipos de instruções
        if instruction.startswith("LOAD"):
            self.execute_load(process, instruction)
        elif instruction.startswith("STORE"):
            self.execute_store(process, instruction)
        elif instruction.startswith("ADD"):
            self.execute_add(process, instruction)
        elif instruction.startswith("SUB"):
            self.execute_sub(process, instruction)
        elif instruction.startswith("MUL"):
            self.execute_mul(process, instruction)

        # Atualiza o contador de programa (PC)
        process.program_counter += 1


    def execute_load(self, process, instruction):
        """
        Simula a execução da instrução LOAD.
        """
        _, value = instruction.split()
        process.registers['ACC'] = int(value)
        print(f"Processo PID {process.pid}: Carregado {value} no ACC")

    def execute_store(self, process, instruction):
        """
        Simula a execução da instrução STORE.
        """
        _, address = instruction.split()
        process.memory_allocated.append((address, process.registers.get('ACC', 0)))
        print(f"Processo PID {process.pid}: Armazenado valor de ACC {process.registers.get('ACC', 0)} no endereço {address}")

    def execute_add(self, process, instruction):
        """
        Simula a execução da instrução ADD.
        """
        _, value = instruction.split()
        process.registers['ACC'] += int(value)
        print(f"Processo PID {process.pid}: Adicionado {value} ao ACC. Novo valor de ACC: {process.registers['ACC']}")

    def execute_sub(self, process, instruction):
        """
        Simula a execução da instrução SUB.
        """
        _, value = instruction.split()
        process.registers['ACC'] -= int(value)
        print(f"Processo PID {process.pid}: Subtraído {value} do ACC. Novo valor de ACC: {process.registers['ACC']}")

    def execute_mul(self, process, instruction):
        """
        Simula a execução da instrução MUL.
        """
        _, value = instruction.split()
        process.registers['ACC'] *= int(value)
        print(f"Processo PID {process.pid}: Multiplicado {value} pelo ACC. Novo valor de ACC: {process.registers['ACC']}")

