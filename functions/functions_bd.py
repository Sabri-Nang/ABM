from functions.personas import Persona


def solicitar_datos():
    while True:
        nombre = input("Ingrese su nombre: ")
        if nombre.isdigit() or nombre == "":
            print("El nombre ingresado no es correcto")
            continue
        break

    while True:
        apellido = input("Ingrese su apellido: ")
        if apellido.isdigit() or apellido == "":
            print("El apellido ingresado no es correcto")
            continue
        break
    
    while True:
        DNI = input("Ingrese su DNI: ")
        if not DNI.isdigit() or len(DNI) != 8:
            print("El DNI ingresado no es válido")
            continue
        break
    DNI = int(DNI)
    
    while True:
        telefono = input("Ingrese su telefono: ")
        if not telefono.isdigit() or len(telefono) < 8:
            print("El telefono ingresado no es válido")
            continue
        break
    telefono = int(telefono)
    
    # mail optativo, sin verificación
    mail = input("Ingrese su mail: ")
    if mail == "":
        mail = None
    return nombre, apellido, DNI, telefono, mail      


def registrar_persona():
    nombre, apellido, DNI, telefono, mail = solicitar_datos()
    persona = Persona(nombre, apellido, DNI, telefono, mail)
    return persona
