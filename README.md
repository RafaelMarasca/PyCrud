CRUD de carros utilizando socket em Python

=> Campos do objeto: 
    - Placa (string)
    - Nome  (string)
    - Marca (string)
    - Ano   (int)
    - KM rodados (int)
    - Tipo de combustivel (string)

=> Formato do objeto empacotado: PLACA@NOME@MARCA@ANO@KM@COMBUSTIVEL (string)

=> Comandos (server side):
    - '0': create
    - '1': read
    - '2': update
    - '3': delete
    - '4': close

=> Dependências:
    - PySimpleGui