from functions.functions_solicitante import ingresar_solicitante
from functions.functions_empleado import crear_tabla_empleados
from functions.abm_menu import mensaje_bienvenida, ingresar_id
from functions.abm_menu import mostrar_empleado
from functions.crear_tablas_db import crear_tablas


def main():
    '''
    Funcion principal
    '''
    crear_tablas()
    crear_tabla_empleados()
    while True:
        opcion = mensaje_bienvenida()
        if opcion == 1:
            ingresar_solicitante()
        elif opcion == 2:
            ingresar_id()
        elif opcion == 3:
            mostrar_empleado()
        elif opcion == 4:
            print('-'*30)
            print('Gracias por utilizar nuestros servicios')
            print('Cerrando el sistema...')
            exit()


if __name__ == '__main__':
    main()
