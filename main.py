from functions.base_datos import Base_Datos
from functions.personas import Persona
from functions.functions_bd import registrar_persona


def main():
    '''
    Funcion principal
    '''
    base = Base_Datos()
    persona1 = registrar_persona()
    print(persona1)
    base.agregar_persona(persona1)

    #base.agregar_persona(persona1)
    print(base)

main()