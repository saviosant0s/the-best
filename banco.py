from hashlib import sha256

class Cliente:
    def __init__(self, nome:str, cpf:str, senha):
        self.__nome = nome
        self.__cpf = cpf
        self.__senha = senha

    def getNome(self):
        return self.__nome
    
    def getCPF(self):
        return self.__cpf
    
    def getSenha(self):
        return self.__senha
        
    def setNome(self, nome):
        self.__nome = nome
    
    def setCPF(self, cpf):
        self.__cpf = cpf
    
    def setSenha(self, senha):
        self.__senha = senha


class Conta:
    def __init__(self, numero: int, titular: Cliente, saldo: float):
        self.__numero = numero
        self.__titular = titular
        self.__saldo = 0.0
        
    def depositar(self, valor: float):
        	self.__saldo += valor
    
    def getNumero(self):
        return self.__numero
    
    def getTitular(self):
        return self.__titular
    
    def getSaldo(self):
        return self.__saldo
    
    def setNumero(self, numero):
        self.__numero = numero
    
    def setTitular(self, titular):
        self.__titular = titular
    
    def setSaldo(self, saldo):
        self.__saldo = saldo


class SistemaBancario:
    def __init__(self, clientes: list=[], contas:list=[]):
        self.__clientes = clientes
        self.__contas = contas

    def buscarCliente(self, cpf:str):
        for c in self.__clientes:
            if c.getCPF() == cpf:
                return c
        
    def cadastrarCliente(self):
        nome = input("Digite o nome do cliente: ")
        cpf = input("Digite o CPF do cliente: ")
        senha = input("Digite a senha do cliente: ")
        senha = sha256(senha.encode()).hexdigest()


        c = self.buscarCliente(cpf)
        if isinstance (c, Cliente):
            print("Cliente já cadastrado")
            return
        else:
            cliente = Cliente(nome, cpf, senha)
            self.__clientes.append(cliente)
            print("Cadastro concluido com sucesso")
    
    def alterarCliente(self):
        try:
            cpf = input("Digite o CPF do cliente que você quer alterar: ")
            cliente = self.buscarCliente(cpf)
            if not cliente:
                raise ValueError("Cliente nao encontrado")
            
            if cliente:
                senha = input("digite sua senha: ")
                novo_nome = input("Digite o novo nome (deixe em branco para não alterar): ")
                novo_cpf = input("Digite o novo CPF (deixe em branco para não alterar): ")
                
                if novo_nome:
                    cliente.setNome(novo_nome)
                if novo_cpf:
                    cliente.setCPF(novo_cpf)
                print("Cliente alterado com sucesso!")

        except ValueError as erro:
            print(f"Erro: {erro}")

    def exibirCliente(self):
       print("=" * 30)
       print("NOME\t\tCPF")
       print("=" * 30)
       for c in self.__clientes:
           print(f"{c.getNome()}\t\t{c.getCPF()}")

    def excluirCliente(self):
        cpf = input("Digite o CPF do cliente que você quer excluir: ")
        c = self.buscarCliente(cpf)
        try:
            if not c:
                raise ValueError("Cliente nao encontrado")
            
            if c:
                self.__clientes.remove(c)
                print("Excluido com sucesso")
        except ValueError as erro:
            print(f"Erro: {erro}")

    def abrirConta(self):
        try:
            cpf = input("Digite o CPF do titular: ")
            cliente = self.buscarCliente(cpf)

            if cliente is None:
                print("Cliente não encontrado. Conta não criada.")
                return

            for conta in self.__contas:
                if conta.getTitular().getCPF() == cpf:
                    print("Conta já criada para este CPF")
                    return

            if len(self.__contas) == 0:
                numero_conta = 10000
            else:
                ultimo_numero = self.__contas[-1].getNumero()
                numero_conta = ultimo_numero + 1

            nova_conta = Conta(numero_conta, cliente, 0.0)
            self.__contas.append(nova_conta)
            print(f"Conta criada com sucesso! Número: {numero_conta}")

        except Exception as e:
            print("Erro ao abrir conta:", e)
        
    def buscarConta(self, num):
        for n in self.__contas:
            if n.getNumero() == num:
                return n
        
    def exibirConta(self):
        print("=" * 40)
        print("NÚMERO DA CONTA\t\tTITULAR (CPF)")
        print("=" * 40)
        for n in self.__contas:
            print(f"{n.getNumero()}\t\t\t{n.getTitular().getNome()} ({n.getTitular().getCPF()})")

    def excluirConta(self):
	        try:
	            num_conta = int(input("Digite o número da conta que você quer excluir: "))
	            
	            conta_para_excluir = self.buscarConta(num_conta)
	            
	            if conta_para_excluir is None:
	                raise ValueError("Conta não encontrada.")
	            
	            self.__contas.remove(conta_para_excluir)
	            print(f"Conta número {num_conta} foi excluída com sucesso.")
	
	        except ValueError as erro:
	            print(f"Erro ao excluir a conta: {erro}")
	        except Exception as e:
	            print(f"Ocorreu um erro inesperado: {e}")
	
    
    def verificarSenha(self, cliente: Cliente, max_tentativas: int = 3):
	    for tentativa in range(max_tentativas):
	        senha_informada = input("Digite sua senha: ")
	        hash_informado = sha256(senha_informada.encode()).hexdigest()
	
	        if hash_informado == cliente.getSenha():
	            return True
	        else:
	            tentativas_restantes = (max_tentativas - 1) - tentativa
	            if tentativas_restantes > 0:
	                print(f"Senha incorreta. Você ainda tem {tentativas_restantes} tentativa(s).")
	
	    print("Número máximo de tentativas de senha excedido.")
	    return False
    
    def exibirSaldo(self):
	    try:
	        numero = int(input("Digite o número da conta: "))
	        conta = self.buscarConta(numero)
	
	        if conta is None:
	            raise ValueError("Conta não encontrada.")
	
	        cliente = conta.getTitular()
	
	        if self.verificarSenha(cliente):
	            print(f"\nTitular: {cliente.getNome()}")
	            print(f"Número da Conta: {conta.getNumero()}")
	            print(f"Saldo Disponível: R$ {conta.getSaldo():.2f}")
	        else:
	            print("Acesso negado. Senha incorreta.")
	    
	    except ValueError as e:
	        print(f"Erro: {e}")
	    except Exception as e:
	        print(f"Ocorreu um erro inesperado: {e}")
	    
    def depositar(self):
	    try:
	        numero = int(input("Digite o número da conta: "))
	        conta = self.buscarConta(numero)
	
	        if conta is None:
	            raise ValueError("Conta não encontrada.")
	
	        cliente = conta.getTitular()
	
	        if self.verificarSenha(cliente):
	            valor = float(input("Digite o valor a ser depositado: "))
	
	            if valor <= 0:
	                print("O valor deve ser maior que zero.")
	                return
	
	            conta.depositar(valor)
	            print(f"Depósito realizado com sucesso. Novo saldo: R$ {conta.getSaldo():.2f}")
	        else:
	            print("Acesso negado. Senha incorreta.")
	    
	    except ValueError as e:
	        print(f"Erro: {e}")
	    except Exception as e:
	        print(f"Ocorreu um erro inesperado: {e}")
    
    def sacar(self):
	    try:
	        numero = int(input("Digite o número da conta: "))
	        conta = self.buscarConta(numero)
	
	        if conta is None:
	            raise ValueError("Conta não encontrada.")
	
	        cliente = conta.getTitular()
	
	        if self.verificarSenha(cliente):
	            valor = float(input("Digite o valor a ser sacado: "))
	
	            if valor <= 0:
	                print("O valor deve ser maior que zero.")
	                return
	
	            if valor > conta.getSaldo():
	                print("Saldo insuficiente.")
	                return
	
	            conta.setSaldo(conta.getSaldo() - valor)
	            print(f"Saque realizado com sucesso. Novo saldo: R$ {conta.getSaldo():.2f}")
	        else:
	            print("Acesso negado. Senha incorreta.")
	
	    except ValueError as e:
	        print(f"Erro: {e}")
	    except Exception as e:
	        print(f"Ocorreu um erro inesperado: {e}")
	    
    def transferir(self):
	    try:
	        origem_num = int(input("Digite o número da conta de origem: "))
	        conta_origem = self.buscarConta(origem_num)
	
	        if conta_origem is None:
	            raise ValueError("Conta de origem não encontrada.")
	
	        cliente_origem = conta_origem.getTitular()
	
	        if self.verificarSenha(cliente_origem):
	            destino_num = int(input("Digite o número da conta de destino: "))
	            conta_destino = self.buscarConta(destino_num)
	
	            if conta_destino is None:
	                raise ValueError("Conta de destino não encontrada")
	
	            valor = float(input("Digite o valor a ser transferido: "))
	
	            if valor <= 0:
	                print("O valor deve ser maior que zero")
	                return
	
	            if valor > conta_origem.getSaldo():
	                print("Saldo insuficiente para transferência")
	                return
	
	            conta_origem.setSaldo(conta_origem.getSaldo() - valor)
	            conta_destino.setSaldo(conta_destino.getSaldo() + valor)
	            print(f"Transferência realizada com sucesso")
	            print(f"Novo saldo da conta de origem: R$ {conta_origem.getSaldo():.2f}")
	        else:
	            print("Acesso negado. Senha incorreta.")
	
	    except ValueError as e:
	        print(f"Erro: {e}")
	    except Exception as e:
	        print(f"Ocorreu um erro inesperado: {e}")
	