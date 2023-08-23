import PySimpleGUI as sg
import socket

sg.theme("DarkBrown1")

plates = []
lst = sg.Listbox(plates, size=(52, 8), font=('Arial Baltic', 12), expand_y=True, enable_events=True, key='-LIST-')

win_layout = [
    [
        sg.Text("Car Plate", size=(15), font=("Arial Baltic", 12)),
        sg.InputText(size = 37, enable_events=True, key="-PLATE-", font=("Arial Baltic", 12))
    ],
    [
        sg.Text("Car Name", size=(15), font=("Arial Baltic", 12)),
        sg.InputText(size = 37, enable_events=True, key="-NAME-", font=("Arial Baltic", 12))
    ],
    [
        sg.Text("Car Brand", size=(15), font=("Arial Baltic", 12)),
        sg.InputText(size = 37, enable_events=True, key="-BRAND-", font=("Arial Baltic", 12))
    ],
    [
        sg.Text("Car Year", size=(15), font=("Arial Baltic", 12)),
        sg.InputText(size = 37, enable_events=True, key="-YEAR-", font=("Arial Baltic", 12))
    ],
    [
        sg.Text("KM Driven", size=(15), font=("Arial Baltic", 12)),
        sg.InputText(size = 37, enable_events=True, key="-KMS-", font=("Arial Baltic", 12))
    ],
    [
        sg.Text("Fuel Type", size=(15), font=("Arial Baltic", 12)),
        sg.InputText(size = 37, enable_events=True, key="-FUEL-", font=("Arial Baltic", 12))
    ],
    [
        sg.Button("Create", size = (7), enable_events=True, key ="-ADDB-", font=("Arial Baltic", 12)),
        sg.Button("Refresh", size = (7), enable_events=True, key ="-REFB-", font=("Arial Baltic", 12)),
        sg.Button("Update", size = (7), enable_events=True, key ="-UPDB-", font=("Arial Baltic", 12)),
        sg.Button("Delete", size = (7), enable_events=True, key ="-DELB-", font=("Arial Baltic", 12)),
        sg.Button("Clear", size = (7), enable_events=True, key ="-CLRB-", font=("Arial Baltic", 12))
    ],
    [
        sg.Text("License Plate List:", size=(15), font=("Arial Baltic", 10)),
    ],
    [    
            lst
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

    window = sg.Window("CAR CRUD GUI", win_layout, enable_close_attempted_event=True, finalize=True)

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


        elif(event == "-REFB-"):
            op = '1'
            data_socket.send(op.encode())

            lst_sz = int.from_bytes(data_socket.recv(1), byteorder='big', signed=False)

            car_dict = {}
            plates = []
            for i in range(lst_sz):
                entry_sz = int.from_bytes(data_socket.recv(1), byteorder='big', signed=False)
                entry = data_socket.recv(entry_sz).decode()

                car_ins(entry, car_dict)
            
            for pl in car_dict:
                plates.append(pl)
            
            window["-LIST-"].update(plates)

        elif(event == "-LIST-"):
            sel = values[event]
            if(sel):
                item = sel[0]
                attr = car_dict[item]

                window["-PLATE-"].update(value=item)
                window["-NAME-"].update(value=attr[0])
                window["-BRAND-"].update(value=attr[1])
                window["-YEAR-"].update(value=int(attr[2]))
                window["-KMS-"].update(value=int(attr[3]))
                window["-FUEL-"].update(value=attr[4])
        
        elif(event == "-UPDB-"):
            plate = values["-PLATE-"]

            if plate in car_dict:
                plate = values["-PLATE-"]
                name = values["-NAME-"]
                brand = values["-BRAND-"]
                year = values["-YEAR-"]
                km = values["-KMS-"]
                fuel = values["-FUEL-"]

                try:
                    int(year)
                except ValueError:
                    sg.popup_ok("Invalid year", font=("Arial Baltic", 10))
                    continue

                try:
                    int(km)
                except ValueError:
                    sg.popup_ok("Invalid KMs", font=("Arial Baltic", 10))
                    continue

                op = '2'
                data_socket.send(op.encode())

                entry_str = plate + "@" + name + "@" + brand + "@" + year + "@" + km + "@" + fuel

                data_socket.send(len(entry_str).to_bytes(length=1, byteorder='big', signed=False))
                data_socket.send(entry_str.encode())


            else:
                sg.popup_ok("Plate not found", font=("Arial Baltic", 10))
        
        elif(event == "-DELB-"):
            plate = values["-PLATE-"]

            if plate in car_dict:
                op = '3'
                data_socket.send(op.encode())
                data_socket.send(len(plate).to_bytes(length=1, byteorder='big', signed=False))
                data_socket.send(plate.encode())

            else:
                sg.popup_ok("Plate not found", font=("Arial Baltic", 10))
            
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