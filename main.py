from functions.base_datos import Base_Datos
from functions.personas import Solicitante, Empleado
from functions.functions_bd import registrar_solicitante


def crear_base_empleados():
    base_empleados = Base_Datos()

    empleado1 = Empleado('Alumbrado', 12345678)
    empleado2 = Empleado('Poda', 12345678)
    empleado3 = Empleado('Licencias', 45789963)
    base_empleados.agregar_persona(empleado1)
    base_empleados.agregar_persona(empleado2)
    base_empleados.agregar_persona(empleado3)
    return base_empleados


def ingresan_solicitantes():
    pass


def resolver_tramites():
    # Empleados
    pass


def main():
    '''
    Funcion principal
    '''
    base_solicitantes = Base_Datos()
    solicitante1 = registrar_solicitante()
    print(solicitante1)
    base_solicitantes.agregar_persona(solicitante1)
    print(base_solicitantes)
    #persona1 = registrar_persona()
    #print(persona1)
    #base_personas.agregar_persona(persona1)
    
    #base.agregar_persona(persona1)
    #print(base_personas)
    #solicitar_tipo_tramite()

main()