from functions.personas import Persona, Solicitante


def solicitar_datos():
    #while True:
    #    nombre = input("Ingrese su nombre: ")
    #    if nombre.isdigit() or nombre == "":
    #        print("El nombre ingresado no es correcto")
    #        continue
    #    break

    #while True:
    #    apellido = input("Ingrese su apellido: ")
    #    if apellido.isdigit() or apellido == "":
    #        print("El apellido ingresado no es correcto")
    #        continue
    #    break
    
    while True:
        DNI = input("Ingrese su DNI: ")
        if not DNI.isdigit() or len(DNI) != 8:
            print("El DNI ingresado no es válido")
            continue
        break
    DNI = int(DNI)
    
    #while True:
    #    telefono = input("Ingrese su telefono: ")
    #    if not telefono.isdigit() or len(telefono) < 8:
    #        print("El telefono ingresado no es válido")
    #   continue
    #    break
    #telefono = int(telefono)
    
    # mail optativo, sin verificación
    #mail = input("Ingrese su mail: ")
    # if mail == "":
     #   mail = None
    return DNI

def solicitar_tipo_tramite():
    tramites = {1: 'Poda', 2: 'Alta Licencias', 3: 'Alumbrado'}
    print('Seleccione el tipo de trámite que desea realizar')
    for k, v in tramites.items():
        print(f'Presione {k} para el {v}')
    # falta validar
    tramite_seleccionado = int(input('Ingrese el número: '))
    return tramite_seleccionado, tramites[tramite_seleccionado]


def solicitar_tramite():  # pasa Solicitante
    while True:
        DNI = input("Ingrese su DNI: ")
        if not DNI.isdigit() or len(DNI) != 8:
            print("El DNI ingresado no es válido")
            continue
        break
    DNI = int(DNI)


def cambiar_estado_tramite(): #Para Empleado
    pass


def registrar_solicitante():
    DNI = solicitar_datos()
    id_tramite, tipo_tramite = solicitar_tipo_tramite()
    estado = 'iniciado'
    solicitante = Solicitante(id_tramite, tipo_tramite, estado, DNI)
    return solicitante