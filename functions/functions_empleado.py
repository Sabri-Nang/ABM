from functions.personas import Empleado


def cambiar_estado_tramite() -> str: #Para Empleado
    '''
    Cambia el estado del trámite.
    Devuelve el estado seleccionado.
    '''
    estados = {1: 'iniciado', 2: 'en proceso', 3: 'resuelto'}
    print('Seleccione el estado del trámite')
    while True:
        for k, v in estados.items():
            print(f'Presione {k} para el {v}')
        try:
            estado_seleccionado = int(input('Ingrese el número: '))
            if estado_seleccionado not in [1, 2, 3]:
                print('El valor ingresado no es válido')
                continue
            break
        except ValueError:
            print('El estado seleccionado no es valido')
            continue
    return estados[estado_seleccionado]

