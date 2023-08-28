#!/usr/bin/env python
""" 
Este script implementa o lado cliente da aplicação
CRUD para cadastro de carros.
"""

__author__ = "Lucas Carvalho and Rafael Marasca Martins"

import socket
import codes
import gui as g

def main():
    dest_ip = "127.0.0.1"
    dest_port = 55000

    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((dest_ip, dest_port))

    interface = g.gui()
    
    while True:
        op = interface.get_event()

        if(op == codes.END):
            break 

        #Operação de Criação
        elif(op == codes.CREATE):
            #Envia o código da operação
            data_socket.send(op.to_bytes(length=1, byteorder='big', signed=False)) 

            #Pega os dados da interface
            entry = interface.get_fields()

            #Empacota os dados em uma string no formato: placa @ modelo @ marca @ ano @ km @ combustível
            entry_str = entry['plate'] + "@" + entry['name'] + "@" + entry['brand'] + "@" + \
                        entry['year'] + "@" + entry['km'] + "@" + entry['fuel']

            #Envia o tamanho da string de dados
            data_socket.send(len(entry_str).to_bytes(length=1, byteorder='big', signed=False))
            #Envia a string de dados
            data_socket.send(entry_str.encode())

            #Espera pelo código de retorno do servidor
            status = int.from_bytes(data_socket.recv(1), byteorder='big', signed=False)

            #Verifica se houve algum erro
            if(status == codes.ERROR):
                interface.pop_up("Registro Já Existente!")
            else:
                interface.pop_up("Registro Criado Com Sucesso!")

        #Operação de Leitura
        elif(op == codes.READ):
            #Envia o código de operação
            data_socket.send(op.to_bytes(length=1, byteorder='big', signed=False))

            #Pega os dados da interface
            entry = interface.get_fields()
            
            #Envia o tamanho da string de placa
            data_socket.send(len(entry['plate']).to_bytes(length = 1, byteorder = 'big', signed = False))
            
            #Envia a placa
            data_socket.send(entry['plate'].encode())

            #Recebe a resposta do servidor
            status = int.from_bytes(data_socket.recv(1), byteorder='big', signed=False)

            #Verifica se houve erro
            if(status == codes.ERROR):
                interface.pop_up("Registro Não Encontrado!")
                continue

            #Recebe o tamanho da string de dados
            entry_sz = int.from_bytes(data_socket.recv(1), byteorder='big', signed=False)

            #Recebe a string de dados
            entry = data_socket.recv(entry_sz).decode()

            #Desempacota a string
            entry = entry.split('@')
    
            #Atualiza a interface
            interface.set_fields(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5])
        
        #Operação de Atualização
        elif(op == codes.UPDATE):
            #Pega os dados da interface
            entry = interface.get_fields()

            #Faz a validação dos campos
            try:
                int(entry['year'])
            except ValueError:
                interface.pop_up("Ano Inválido")
                continue

            try:
                int(entry['km'])
            except ValueError:
                interface.pop_up("KM Inválido")
                continue

            #Envia o código de operação
            data_socket.send(op.to_bytes(length=1, byteorder='big', signed=False)) 

            #Empacota os dados em uma string no formato: placa @ modelo @ marca @ ano @ km @ combustível
            entry_str = entry['plate'] + "@" + entry['name'] + "@" + entry['brand'] + "@" + \
                        entry['year'] + "@" + entry['km'] + "@" + entry['fuel']

            #Envia o tamanho da string
            data_socket.send(len(entry_str).to_bytes(length=1, byteorder='big', signed=False))
            #Envia a string
            data_socket.send(entry_str.encode())
            
            #Recebe a resposta do servidor
            status = int.from_bytes(data_socket.recv(1), byteorder='big', signed=False)

            #Verifica se houve algum erro
            if(status == codes.ERROR):
                interface.pop_up("Registro Não Encontrado!")
            else:
                interface.pop_up("Registro Atualizado com Sucesso!")

        #Operação de Apagagem
        elif(op == codes.DELETE):
            entry = interface.get_fields()

            #Envia o código de Operação
            data_socket.send(op.to_bytes(length=1, byteorder='big', signed=False)) 
            
            #Envia o tamanho da placa
            data_socket.send(len(entry['plate']).to_bytes(length=1, byteorder='big', signed=False))

            #Envia a placa
            data_socket.send(entry['plate'].encode())

            #Recebe a resposta do servidor
            status = int.from_bytes(data_socket.recv(1), byteorder='big', signed=False)

            #Verifica se houve algum erro
            if(status == codes.ERROR):
                interface.pop_up("Registro Não Encontrado!")
            else:
                interface.pop_up("Registro Deletado Com Sucesso")
            

    #Finaliza enviando um código de fim ao servidor
    op = codes.END
    data_socket.send(op.to_bytes(length=1, byteorder='big', signed=False))
    
    #Fecha a conexão
    data_socket.close()


if __name__ == "__main__":
    main()