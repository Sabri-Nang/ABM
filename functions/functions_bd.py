from functions.personas import Persona, Solicitante


def solicitar_dni():
    '''
    Solicita el DNI    
    '''
    while True:
        DNI = input("Ingrese su DNI: ")
        if not DNI.isdigit() or len(DNI) != 8:
            print("El DNI ingresado no es válido")
            continue
        break
    DNI = int(DNI)
    return DNI

def solicitar_tipo_tramite():
    tramites = {1: 'Poda', 2: 'Alta Licencias', 3: 'Alumbrado'}
    print('Seleccione el tipo de trámite que desea realizar')
    for k, v in tramites.items():
        print(f'Presione {k} para el {v}')
    # falta validar
    tramite_seleccionado = int(input('Ingrese el número: '))
    return tramite_seleccionado, tramites[tramite_seleccionado]


def cambiar_estado_tramite(): #Para Empleado
    pass


def registrar_solicitante():
    DNI = solicitar_datos()
    id_tramite, tipo_tramite = solicitar_tipo_tramite()
    estado = 'iniciado'
    solicitante = Solicitante(id_tramite, tipo_tramite, estado, DNI)
    return solicitante