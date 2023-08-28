#!/usr/bin/env python
""" 
Este script implementa o lado servido da aplicação
CRUD para cadastro de carros.
"""

__author__ = "Lucas Carvalho and Rafael Marasca Martins"

import socket
import codes

#Abre o arquivo de armazenamento permanente
def car_reg_init(file_name):
    car_r = {}
    with open(file_name, 'r') as reg:
        lin = reg.readlines()

        for line in lin:
            reg = line.split()
            car_r[reg[0]] = [reg[1], reg[2], int(reg[3]), int(reg[4]), reg[5]]

    return car_r

#Adiciona um registro no arquivo de armazenamento permanente
def car_create(car_register, lic_plate, car_attr, file_name):
    car_id = lic_plate

    car_register[car_id] = car_attr

    car_reg_str = car_id + " " + car_attr[0] + " " + car_attr[1] + " " + str(car_attr[2]) + " " + str(car_attr[3]) + " " + car_attr[4] + "\n"

    with(open(file_name, 'a')) as reg:
        reg.write(car_reg_str)


#Lê os registro de um carro
def car_read(car_register, car_id):
    return car_register[car_id]

#Atualiza o registro de um carro
def car_update(car_register, car_id, car_attr, file_name):
    car_reg_str = car_id + " " + car_attr[0] + " " + car_attr[1] + " " + str(car_attr[2]) + " " + str(car_attr[3]) + " " + car_attr[4] + "\n"
    
    car_register.pop(car_id, None)
    car_register[car_id] = car_attr

    with open(file_name, 'r') as reg:
        lin = reg.readlines()

    with open(file_name, 'w') as reg:
        for line in lin:
            target_id = line.split()[0]
            if(target_id != car_id):
                reg.write(line)
            else:
                reg.write(car_reg_str)
    
#Deleta um carro do registro
def car_delete(car_register, car_id, file_name):
    lin = []
    with open(file_name, 'r') as reg:
        lin = reg.readlines()

    with open(file_name, 'w') as reg:
        for line in lin:
            target_id = line.split()[0]
            if(target_id != car_id):
                reg.write(line)
    
    car_register.pop(car_id, None)

def main():
    fi_name = "car_reg.txt"
    #Lê o registro de carros para a memória principal
    car_dict = car_reg_init(fi_name) 

    ip = "127.0.0.1"
    port = 55000

    #Cria um socket tpc na porta e ip especificados
    conn_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_server.bind((ip, port))

    conn_server.listen(1)
    [socket_data, client_data] = conn_server.accept()

    op = None
    
    while op != codes.END:
        #Lê o código de operação
        op = int.from_bytes(socket_data.recv(1), byteorder='big', signed=False)

        #Operação de Leitura
        if(op == codes.CREATE):
            #Lê o tamanho da string de dados
            entry_sz = int.from_bytes(socket_data.recv(1), byteorder='big', signed=False)
            #Lê a string de dados
            entry = socket_data.recv(entry_sz).decode()

            #Separa os dados da string
            entry_lst = entry.split('@')
            entry_lst[3] = int(entry_lst[3])
            entry_lst[4] = int(entry_lst[4])

            #Verifica se o registro ja existe na base de dados
            if(car_dict.get(entry_lst[0], None) != None):
                #Caso exista, envia o código de erro
                socket_data.send(codes.ERROR.to_bytes(length = 1, byteorder = 'big', signed = False))
            else:
                #Caso não exista, envia o código de sucesso 
                socket_data.send(codes.SUCCESS.to_bytes(length = 1, byteorder = 'big', signed = False))
                #Cria o carro na base de dados
                car_create(car_dict, entry_lst[0], entry_lst[1:], fi_name)

        #Operação de Leitura
        elif(op == codes.READ):

            #Obtém o tamanho da placa
            plate_sz = int.from_bytes(socket_data.recv(1), byteorder='big', signed=False)
            
            #Obtém a placa
            plate = socket_data.recv(plate_sz)
            plate = plate.decode()

            #Verifica se o carro existe na base de dados
            if(car_dict.get(plate, None) != None):
                #Caso exista
                #Busca o registro
                attr = car_dict[plate]

                #Empacota a string de dados
                entry_str = plate + "@" + attr[0] + "@" + attr[1] + "@" + str(attr[2]) + "@" + str(attr[3]) + "@" + attr[4]

                #Envia o código de sucesso
                socket_data.send(codes.SUCCESS.to_bytes(length = 1, byteorder = 'big', signed = False))
                
                #Envia o tamanho da string de dados
                socket_data.send(len(entry_str).to_bytes(length=1, byteorder='big', signed=False))

                #Envia a string de dados
                socket_data.send(entry_str.encode())
            else:
                #Caso não exista, envia o código de erro
                socket_data.send(codes.ERROR.to_bytes(length = 1, byteorder = 'big', signed = False))

        #Operação de Atualização
        elif(op == codes.UPDATE):

            #Recupera o tamanho da string de dados
            entry_sz = int.from_bytes(socket_data.recv(1), byteorder='big', signed=False)
            #Recupera a string de dados
            entry = socket_data.recv(entry_sz).decode()

            #Separa os dados
            entry_lst = entry.split('@')
            entry_lst[3] = int(entry_lst[3])
            entry_lst[4] = int(entry_lst[4])

            #Verifica se o carro está no registro
            if(car_dict.get(entry_lst[0]) == None):
                #Caso não exista, envia o código de erro
                socket_data.send(codes.ERROR.to_bytes(length = 1, byteorder = 'big', signed = False))
            else:
                #Caso exista, envia o código de sucesso
                socket_data.send(codes.SUCCESS.to_bytes(length = 1, byteorder = 'big', signed = False))
                #Atualiza a entrada no registro
                car_update(car_dict, entry_lst[0], entry_lst[1:], fi_name)

        #Operação de Apagagem
        elif(op == codes.DELETE):
            #Recupera o tamanho da string de dados
            plate_sz = int.from_bytes(socket_data.recv(1), byteorder='big', signed=False)
            #Recupera a placa
            plate = socket_data.recv(plate_sz).decode()

            if(car_dict.get(plate, None) == None):
                #Caso não exista, envia o código de erro
                socket_data.send(codes.ERROR.to_bytes(length = 1, byteorder = 'big', signed = False))
            else:
                #Caso exista, envia o código de sucesso
                socket_data.send(codes.SUCCESS.to_bytes(length = 1, byteorder = 'big', signed = False))
                #Deleta o carro do registro
                car_delete(car_dict, plate, fi_name)
    
    socket_data.close()
    conn_server.close()


if __name__ == "__main__":
    main()