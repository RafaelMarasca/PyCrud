import socket

def car_reg_init(file_name):
    car_r = {}
    with open(file_name, 'r') as reg:
        lin = reg.readlines()

        for line in lin:
            reg = line.split()
            car_r[reg[0]] = [reg[1], reg[2], int(reg[3]), int(reg[4]), reg[5]]

    return car_r


def car_create(car_register, lic_plate, car_attr, file_name):
    car_id = lic_plate

    car_register[car_id] = car_attr

    car_reg_str = car_id + " " + car_attr[0] + " " + car_attr[1] + " " + str(car_attr[2]) + " " + str(car_attr[3]) + " " + car_attr[4] + "\n"

    with(open(file_name, 'a')) as reg:
        reg.write(car_reg_str)

def car_read(car_register, car_id):
    return car_register[car_id]


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
    car_dict = car_reg_init(fi_name)

    ip = "127.0.0.1"
    port = 55000
    addr = (ip, port)

    conn_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_server.bind(addr)

    conn_server.listen(1)
    [socket_data, client_data] = conn_server.accept()

    op = None
    
    #'0' = create; '1' = read; '2' = update; '3' = delete; '4' = end
    while op != '4':
        op = (socket_data.recv(1)).decode()

        if(op == '0'):
            entry_sz = int.from_bytes(socket_data.recv(1), byteorder='big', signed=False)
            entry = socket_data.recv(entry_sz).decode()

            entry_lst = entry.split('@')
            entry_lst[3] = int(entry_lst[3])
            entry_lst[4] = int(entry_lst[4])

            car_create(car_dict, entry_lst[0], entry_lst[1:], fi_name)


        elif(op == '1'):
            socket_data.send(len(car_dict).to_bytes(length=1, byteorder='big', signed=False))

            for plate, attr in car_dict.items():
                entry_str = plate + "@" + attr[0] + "@" + attr[1] + "@" + str(attr[2]) + "@" + str(attr[3]) + "@" + attr[4]

                socket_data.send(len(entry_str).to_bytes(length=1, byteorder='big', signed=False))

                socket_data.send(entry_str.encode())


        elif(op == '2'):
            entry_sz = int.from_bytes(socket_data.recv(1), byteorder='big', signed=False)
            entry = socket_data.recv(entry_sz).decode()

            entry_lst = entry.split('@')
            entry_lst[3] = int(entry_lst[3])
            entry_lst[4] = int(entry_lst[4])

            car_update(car_dict, entry_lst[0], entry_lst[1:], fi_name)

        elif(op == '3'):
            plate_sz = int.from_bytes(socket_data.recv(1), byteorder='big', signed=False)
            plate = socket_data.recv(plate_sz).decode()

            car_delete(car_dict, plate, fi_name)



    
    socket_data.close()
    conn_server.close()




if __name__ == "__main__":
    main()