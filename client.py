import PySimpleGUI as sg
import socket

sg.theme("DarkBrown1")

win_layout = [
    [
        sg.Text("Placa", size=(15), font=("Arial Baltic", 12)),
        sg.InputText(size = 37, enable_events=True, key="-PLATE-", font=("Arial Baltic", 12))
    ],
    [
        sg.Text("Modelo", size=(15), font=("Arial Baltic", 12)),
        sg.InputText(size = 37, enable_events=True, key="-NAME-", font=("Arial Baltic", 12))
    ],
    [
        sg.Text("Marca", size=(15), font=("Arial Baltic", 12)),
        sg.InputText(size = 37, enable_events=True, key="-BRAND-", font=("Arial Baltic", 12))
    ],
    [
        sg.Text("Ano", size=(15), font=("Arial Baltic", 12)),
        sg.InputText(size = 37, enable_events=True, key="-YEAR-", font=("Arial Baltic", 12))
    ],
    [
        sg.Text("KM Rodados", size=(15), font=("Arial Baltic", 12)),
        sg.InputText(size = 37, enable_events=True, key="-KMS-", font=("Arial Baltic", 12))
    ],
    [
        sg.Text("Combustível", size=(15), font=("Arial Baltic", 12)),
        sg.InputText(size = 37, enable_events=True, key="-FUEL-", font=("Arial Baltic", 12))
    ],
    [
        sg.Button("Criar", size = (7), enable_events=True, key ="-ADDB-", font=("Arial Baltic", 12)),
        sg.Button("Atualizar", size = (7), enable_events=True, key ="-REFB-", font=("Arial Baltic", 12)),
        sg.Button("Editar", size = (7), enable_events=True, key ="-UPDB-", font=("Arial Baltic", 12)),
        sg.Button("Deletar", size = (7), enable_events=True, key ="-DELB-", font=("Arial Baltic", 12)),
        sg.Button("Limpar", size = (7), enable_events=True, key ="-CLRB-", font=("Arial Baltic", 12))
    ]
]

def car_ins(entry_str, car_dict):
    entry = entry_str.split('@')
    
    car_dict[entry[0]] = [entry[1], entry[2], int(entry[3]), int(entry[4]), entry[5]]


def main():
    dest_ip = "127.0.0.1"
    dest_port = 55000
    dest = (dest_ip, dest_port)

    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect(dest)

    window = sg.Window("CAR CRUD", win_layout, element_justification='c', enable_close_attempted_event=True, finalize=True)

    car_dict = {}

    while True:
        event, values = window.read()

        if(event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT) or event == "Exit":
            break 
        elif(event == "-ADDB-"):
            op = '0'
            data_socket.send(op.encode())

            plate = values["-PLATE-"]
            name = values["-NAME-"]
            brand = values["-BRAND-"]
            year = values["-YEAR-"]
            km = values["-KMS-"]
            fuel = values["-FUEL-"]
            entry_str = plate + "@" + name + "@" + brand + "@" + year + "@" + km + "@" + fuel

            data_socket.send(len(entry_str).to_bytes(length=1, byteorder='big', signed=False))
            data_socket.send(entry_str.encode())

            status = int.from_bytes(data_socket.recv(1), byteorder='big', signed=False)

            if(status == 255):
                sg.popup_ok("Registro Já Existente")
            else:
                sg.popup_ok("Registro Criado Com Sucesso")

        elif(event == "-REFB-"):
            op = '1'
            plate = values["-PLATE-"]
            data_socket.send(op.encode())
            data_socket.send(len(plate).to_bytes(length = 1, byteorder = 'big', signed = False))
            data_socket.send(plate.encode())

            entry_sz = int.from_bytes(data_socket.recv(1), byteorder='big', signed=False)

            if(entry_sz == 255):
                sg.popup_ok("Registro Não Encontrado!", font=("Arial Baltic", 10))
                continue

            entry = data_socket.recv(entry_sz).decode()

            entry = entry.split('@')
    
            window["-PLATE-"].update(value=entry[0])
            window["-NAME-"].update(value=entry[1])
            window["-BRAND-"].update(value=entry[2])
            window["-YEAR-"].update(value=int(entry[3]))
            window["-KMS-"].update(value=int(entry[4]))
            window["-FUEL-"].update(value=entry[5])
        
        elif(event == "-UPDB-"):
            plate = values["-PLATE-"]
            name = values["-NAME-"]
            brand = values["-BRAND-"]
            year = values["-YEAR-"]
            km = values["-KMS-"]
            fuel = values["-FUEL-"]

            try:
                int(year)
            except ValueError:
                sg.popup_ok("Ano Inválido", font=("Arial Baltic", 10))
                continue

            try:
                int(km)
            except ValueError:
                sg.popup_ok("KM Inválido", font=("Arial Baltic", 10))
                continue

            op = '2'
            data_socket.send(op.encode())

            entry_str = plate + "@" + name + "@" + brand + "@" + year + "@" + km + "@" + fuel

            data_socket.send(len(entry_str).to_bytes(length=1, byteorder='big', signed=False))
            data_socket.send(entry_str.encode())
            
            status = int.from_bytes(data_socket.recv(1), byteorder='big', signed=False)

            if(status == 255):
                sg.popup_ok("Registro Não Encontrado")
            else:
                sg.popup_ok("Registro Atualizado com Sucesso")

        elif(event == "-DELB-"):
            plate = values["-PLATE-"]

            op = '3'
            data_socket.send(op.encode())
            data_socket.send(len(plate).to_bytes(length=1, byteorder='big', signed=False))
            data_socket.send(plate.encode())

            status = int.from_bytes(data_socket.recv(1), byteorder='big', signed=False)

            if(status == 255):
                sg.popup_ok("Registro Não Encontrado")
            else:
                sg.popup_ok("Registro Deletado Com Sucesso")
            
        elif(event == "-CLRB-"):
            window["-PLATE-"].update("")
            window["-NAME-"].update("")
            window["-BRAND-"].update("")
            window["-YEAR-"].update("")
            window["-KMS-"].update("")
            window["-FUEL-"].update("")



    op = '4'
    data_socket.send(op.encode())
    data_socket.close()


if __name__ == "__main__":
    main()