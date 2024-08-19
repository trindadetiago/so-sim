from core.vm import VM
from core.process import Process
from core.scheduler import Scheduler, SchedulingAlgorithm

def main():
    # Configuração inicial do Scheduler (utilizando o algoritmo FIFO)
    scheduler = Scheduler(algorithm=SchedulingAlgorithm.ROUND_ROBIN)
    
    # Criação dos processos com conjuntos de instruções fictícias
    process1 = Process(["LOAD 1", "ADD 2", "STORE 100", "JMP 4", "ADD 1"])
    process2 = Process(["LOAD 5", "SUB 3", "STORE 200"])
    process3 = Process(["LOAD 2", "MUL 3", "STORE 300"])
    
    # Adicionando os processos ao Scheduler
    scheduler.add_process(process1)
    scheduler.add_process(process2)
    scheduler.add_process(process3)
    
    # Instanciando a VM com o Scheduler configurado
    vm = VM(scheduler)
    
    # Executando a VM (que por sua vez executa os processos)
    vm.execute()

if __name__ == "__main__":
    main()