##CRUD de carros utilizando socket em Python

### Campos do objeto: <br />
    - Placa (string) <br />
    - Nome  (string) <br />
    - Marca (string) <br />
    - Ano   (int) <br />
    - KM rodados (int) <br />
    - Tipo de combustivel (string) <br />

### Formato do objeto empacotado: PLACA@NOME@MARCA@ANO@KM@COMBUSTIVEL (string)

### Comandos (server side): <br />
    - '0': create <br />
    - '1': read <br />
    - '2': update <br />
    - '3': delete <br />
    - '4': close <br />

### Dependências: <br />
    - PySimpleGui