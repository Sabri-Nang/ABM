from functions.personas import Solicitante
import random


def solicitar_dni() -> int:
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


def solicitar_tipo_tramite() -> str:
    '''
    Solicita el tipo de trámite.
    Devuelde el trámite solicitado
    '''
    tramites = {1: 'Poda', 2: 'Alta Licencias', 3: 'Alumbrado'}
    print('Seleccione el tipo de trámite que desea realizar')
    while True:
        for k, v in tramites.items():
            print(f'Presione {k} para el {v}')
        try:
            tramite_seleccionado = int(input('Ingrese el número: '))
            if tramite_seleccionado not in [1, 2, 3]:
                continue
            break
        except ValueError:
            print('El trámite seleccionado no es valido')
            continue
    return tramite_seleccionado, tramites[tramite_seleccionado]


def registrar_solicitante():
    DNI = solicitar_dni()
    tramite_seleccionado, tipo_tramite = solicitar_tipo_tramite()
    id_tramite = random.randint(1, 10000)
    estado = 'iniciado'
    solicitante = Solicitante(id_tramite, tipo_tramite, estado, DNI)
    return tramite_seleccionado, solicitante