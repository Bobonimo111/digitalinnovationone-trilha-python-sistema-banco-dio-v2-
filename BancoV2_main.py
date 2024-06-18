# Estrutura de um cliente
# {
#     'nome':'nome e sobrenome de usuario',
#     'data_nascimento':'DD-MM-YYYY',
#     'cpf':'00000000000',
#     'endereco':'logradouro - n° - bairro - cidade/estado(PE)'
# }
#Não pode haver cadastros com CPF duplicados
#Um cliente pode conter varias contas.

#Estrutura da conta
# {
#     'agencia': '0001',
#     'n_conta': '1',
#     'cliente': 'cpf',
#     'limites': {
#               'saque_totais':3,
#               'saque_valor: 1000'
#                }
#     'saldo':10000.00,
#     'extrato':[
#                   {'tipo':'saque','valor':1000.00,'data':'00-00-0000'}
#               ] 
# }
# n_conta é como um id unico por conta.
# 
import pprint
usuarios = [
{
    'nome':'William',
    'data_nascimento':'00-00-0000',
    'cpf':'1234',
    'endereco':'logradouro - n° - bairro - cidade/estado(PE)'
}
]
contas = [
    {
    'agencia': '0001',
    'n_conta': '0',
    'cliente': '1234',
    'limites': {
              'saque': 1000.00,
              'limite_restante': 1000.00
               },
    'saldo':10000.00,
    'extrato':[
                  {'tipo':'saque','valor':-1000.00,'data':'00-00-0000'}
              ],
    'valor_transacoes':1000.00 
    }
]


menu_inicial = """
==== opcoes ====
[1] Acessar conta
[2] Cria conta
[0] Encerrar
"""
menu_logado = """
==== opcoes ====
[1] Saque
[2] Desposito
[3] Visualizar extrato
[4] Cria nova conta
[0] Encerrar
"""

def extrato(conta_id,contas):
    """Por posição e keyWord"""
    extrato_txt = "\n\n"
    for op in contas[conta_id]['extrato']:
        extrato_txt += f"{op['tipo']} | {op['valor']:.2f} | {op['data']} \n"


    return extrato_txt + f"\n saldo | {contas[conta_id]['saldo']}"


def deposito(conta_id,contas,valor):
    """Por posição"""
    contas[conta_id]['saldo'] += valor
    contas[conta_id]['extrato'].append({'tipo':'deposito','valor':valor,'data':'00-00-0000'})


def saque(conta_id,contas,valor):
    """keyword only"""
    """Retorno 0 significa sem limiet 1 saque efetuado"""
    if(contas[conta_id]['limites']['limite_restante'] >= valor):

        if(contas[conta_id]['saldo'] >= valor):
            contas[conta_id]['saldo'] -= valor
            contas[conta_id]['extrato'].append({'tipo':'saque','valor':-(valor),'data':'00-00-0000'})
            return [1,'Operação bem sucedida']
        else:
            return [0, "sem saldo"]
        
    else:
        #sem limite de saque ou saldo indisponivel
        return [0,"limite insuficiente"]

def novo_usuario(usuarios):
    novo = {
                'nome':input("nome: "),
                'data_nascimento':input("data de nascimento (DD-MM-YYYY): " ),
                'cpf':input("cpf(apenas numeros): "),
                'endereco':f'{input('logradouro: ')} - {input('Bairro: ')} - {input('referencia: ')} - {input('cidade/estado(PE): ')}'
            } 
    cpf_existente = -1
    
    while True:
        for x in usuarios:
            if novo['cpf'] in x['cpf']:
                print("cpf ja cadastrado tente outro")
                cpf_existente = x['cpf']
                break

        if (cpf_existente != novo['cpf']) and (novo['cpf'] != ''):
            usuarios.append(novo)
            print("CADASTRO REALIZADO")
            return novo
        else:
            print("CPF ja cadastrado ou invalido")
            novo['cpf'] = input("novo cpf")
    

def nova_conta(user_cpf,contas):
    contas.append(
        {
    'agencia': '0001',
    'n_conta': len(contas) + 1,
    'cliente': f"{user_cpf}",
    'limites': {
              'saque': 1000.00,
              'limite_restante': 1000.00
               },
    'saldo':0,
    'extrato':[],
    'valor_transacoes':0
    })
    return(contas[-1])

            


# teste operações
# deposito(0,contas=contas,valor=250)
# saque(0,contas=contas,valor=50)
# extrato(0,contas=contas)



def validar(db_usuarios,cpf):
    """
    db_usuarios (Um banco de dados para os usuarios cadastrados)
    cpf (o cpf do usuario)
    """
    for x in db_usuarios:
        if (x['cpf'] == cpf):
            return 1
    return 0 

def acessar_conta(validador,contas,usuarios):
    cpf = str(input('QUAL O CPF DA SUA CONTA(APENAS NUMEROS) :'))
    if (validador(usuarios,cpf)):
        #Todas as contas de usuarios
        user_contas = []
        conta_aberta = 0
        #Fisgar as contas do usuario
        for x in range(len(contas)): 
            if contas[x]['cliente'] == cpf:
                user_contas.append(x) 

        
        if len(user_contas) > 1:
            print("Qual das contas deseja acessar:")
            for x in user_contas:
                print(contas[x])
            while True:
                conta_aberta = int(input(""))
                if conta_aberta in user_contas:
                    break
                else:
                    print('a conta não é sua')
        else:
            conta_aberta = user_contas[0]

        print("USUARIO LOGADO COM SUCESSO")
        while True:    
            print(menu_logado)
            user_op = int(input('Digite uma das opções disponiveis: '))
            #saque
            if user_op == 1:
                print("\nSAQUE\n")
                user_valor = int(input('Qual o valor de saque: '))
                saque_return = saque(conta_id=conta_aberta,contas=contas,valor=user_valor)
                #print(saque_return)
                if saque_return[0]:
                    print(f"Saque de R${user_valor:.2f} efetuado, cheque seu extrato")
                else:
                    print(f"{saque_return[1]}")
            #deposito
            elif user_op == 2:
                print("\nDeposito\n")
                user_valor = int(input("qual o valor o do seu deposito: "))
                deposito(conta_aberta,contas,user_valor)
                print(f"Deposito  de R${user_valor:.2f} efetuado, cheque seu extrato")
            #extrato 
            elif user_op == 3:
                print(extrato(conta_aberta,contas=contas))
            #encerrar
            elif user_op == 0:
                 break
            #excessão
            else:
                 print("valor invalido tente novamente com um valor valido")
    else:
        print("USUARIO NÃO ENCONTRADA, DESEJA CRIAR UM NOVA ? ")
        user_op = input('S / N : ') 
        if(user_op.lower() == "s"):
            nova = novo_usuario(usuarios=usuarios)
            dados = nova_conta(nova['cpf']
            ,contas)
            print("DADOS DA CONTA")
            pprint.pprint(dados)
            input("Prescione qualquer tecla para continuar")

        else:
            print("Tente novamenta mais tarde")
            input("Prescione qualquer tecla para continuar")
        



def main():
    global contas
    global usuarios
    while True:
        print(menu_inicial)
        user_op = int(input('Digite uma das opções disponiveis: '))
        #Acessar conta
        if(user_op == 1):
            acessar_conta(validar,contas=contas,usuarios=usuarios)
        #Criar usuario
        elif(user_op == 2):
            novo_usuario()
        #Sair
        elif(user_op == 0):
            break
        #Invalido
        else:
            print("VALOR INVALIDO PORFAVOR TENTE NOVAMENTE!!!")
            input("PRESCIONE QUALQUER TECLA PARA CONTINUAR")


if __name__=="__main__":
     main()