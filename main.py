from functions.functions_solicitante import ingresar_solicitante
from functions.abm_menu import mensaje_bienvenida, ingresar_id, mostrar_empleado
from settings.settings import base_datos, servidor
from functions.base_datos_sqlserver import crear_base_datos
from functions.crear_tablas_db import crear_tablas


def main():
    '''
    Funcion principal
    '''
    crear_base_datos(servidor, base_datos)
    crear_tablas()
    while True:
        opcion = mensaje_bienvenida()
        if opcion == 1:
            ingresar_solicitante()
        elif opcion == 2:
            ingresar_id()
        elif opcion == 3:
            mostrar_empleado()
        elif opcion == 4:
            exit()
    

if __name__ == '__main__':
    main()





