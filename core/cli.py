import sys
import time
from core.process import ProcessManager
from core.scheduler import Scheduler, SchedulingAlgorithm
from core.vm import VM
from core.memory_manager import MemoryManager

class CLI:
    def __init__(self):
        """
        Inicializa o CLI com os componentes necessários: gerenciador de processos, gerenciador de memória, escalonador e máquina virtual.

        :param self: Instância do objeto CLI.
        """
        self.process_manager = ProcessManager()
        self.memory_manager = MemoryManager(max_physical_memory=3)  # Definindo o tamanho da memória física no código
        self.scheduler = Scheduler(algorithms=[SchedulingAlgorithm.SJF])
        self.vm = VM(self.scheduler, self.memory_manager)  # Passando o gerenciador de memória para a VM

    def load_process_from_file(self, file_path):
        """
        Carrega um processo a partir de um arquivo .txt e adiciona ao gerenciador de processos e ao escalonador.
        """
        try:
            with open(file_path, 'r') as file:
                instructions = [line.strip() for line in file.readlines()]
                if instructions:
                    process = self.process_manager.create_process(instructions)
                    if process:  # Verifica se o processo foi criado com sucesso
                        self.memory_manager.add_process(process)
                        # Prioridade definida de forma fixa para fins de exemplo (pode ser alterada conforme necessário)
                        priority = 0  # Por exemplo, todos começam na fila de maior prioridade
                        self.scheduler.add_process(process, priority=priority)
                        print(f"Processo carregado a partir do arquivo {file_path}")
                    else:
                        print(f"Falha ao criar o processo a partir do arquivo {file_path}")
                else:
                    print(f"Nenhuma instrução encontrada em {file_path}")
        except FileNotFoundError:
            print(f"Arquivo {file_path} não encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro ao carregar o arquivo {file_path}: {e}")

    def run_vm(self):
        """
        Executa a VM e simula a execução dos processos.
        """
        self.vm.execute()
        print("Execução da VM concluída.")

    def start(self):
        """
        Inicia a interface interativa de linha de comando para o gerenciamento de processos e execução da VM.
        """
        print("Bem-vindo à CLI da VM!")

        while True:
            command = input("\nDigite um comando (create, run, exit): ").strip().lower()
            if command == "create":
                file_path = input("Digite o caminho do arquivo .txt para o processo (ou múltiplos arquivos separados por vírgulas): ").strip()
                files = [f.strip() for f in file_path.split(",")]
                for f in files:
                    self.load_process_from_file(f)
            elif command == "run":
                self.run_vm()
                while True:
                    next_action = input("\nDigite 'add' para adicionar um novo processo, 'run' para continuar ou 'exit' para sair: ").strip().lower()
                    if next_action == "add":
                        file_path = input("Digite o caminho do arquivo .txt para o processo: ").strip()
                        self.load_process_from_file(file_path)
                    elif next_action == "run":
                        self.run_vm()
                    elif next_action == "exit":
                        sys.exit(0)
                    else:
                        print("Comando inválido. Por favor, digite 'add', 'run' ou 'exit'.")
            elif command == "exit":
                print("Saindo da CLI.")
                sys.exit(0)
            else:
                print("Comando desconhecido. Por favor, digite 'create', 'run' ou 'exit'.")
