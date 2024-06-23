from functions.functions_solicitante import obtener_estado_tramite
from functions.functions_solicitante import contar_datos_estado
from functions.functions_solicitante import calcular_espera
from functions.functions_empleado import verificar_dni_empleado
from functions.functions_empleado import mostrar_tramites_iniciados
from functions.functions_empleado import resolver_siguiente_tramite
from functions.functions_empleado import actualizar_estado_tramite


def mostrar_opciones(diccionario):
    '''
    Imprime clave: valor de un diccionario
    '''
    for k, v in diccionario.items():
        print(f'{k}: {v}')


def mensaje_bienvenida():
    '''
    Mensaje de bienvenida al sistema.
    Muestra las opciones según lo que se desee realizar.
    Verifica que la opción ingresada es correcta.
    Devuelve la opcion ingresada.
    '''
    print('-'*30)
    print('Bienvenido al sistema de turnos municipales')
    print('¿Qué desea hacer?')
    diccionario_opciones = {1: 'Solicitar turno', 2: 'Ver estado de mi trámite',
                            3: 'Soy empleado', 4: 'Salir'}
    while True:
        mostrar_opciones(diccionario_opciones)
        try:
            opcion = int(input('Ingrese la opción deseada: '))
            if opcion not in [1, 2, 3, 4]:
                print('La opción ingresada no es válida')
                continue
            return opcion
        except ValueError:
            print('El valor ingresado no es válido')
            continue


def mostrar_estado(dataframe):
    '''
    Recibe un dataframe con columnas, tramite, DNI, estado y id_tramite
    Muestra un mensaje con los datos.
    Si el estado es iniciado, muestra cuantas personas hay antes con el 
    mismo tipo de trámite y el tiempo de espera.
    '''
    tramite = dataframe['tramite'][0]
    DNI = dataframe['DNI'][0]
    estado = dataframe['estado'][0]
    cantidad = contar_datos_estado(estado, tramite) - 1
    print('-'*30)
    print("{:-^30}".format(' ESTADO DE TRÁMITE '))
    print(f'DNI: {DNI}')
    print(f'Usted a solicitado un turno para {tramite.upper()}')
    print(f'El estado de su trámite es: {estado}')
    if estado == 'iniciado':
        print(f'Usted tiene {cantidad} personas antes')
        horas, minutos = calcular_espera(cantidad)
        print(f'El tiempo de espera es de {horas} horas y {minutos} minutos aproximadamente')
        print('Por favor aguarde y será atendido')
    elif estado == 'en proceso':
        print('Su trámite esta siendo gestionado en estos momentos')
        print('Será informado al momento de que su estado se resuelva')
    elif estado == 'resuelto':
        print('Su trámite ha sido resuelto')
    print('Gracias por utilizar nuestros servicios')
    print('-'*30)


def ingresar_id():
    '''
    Pide el ingreso de un id_tramite. 
    Si el id_tramite se encuentra en la base de datos, 
    llama la funcion mostrar_estado.
    Si no existe o es inválido, lo vuelve a solicitar.
    '''
    while True:
        try:
            id_ingresado = int(input('Ingrese el ID de su trámite: '))
            df = obtener_estado_tramite(id_ingresado)
            if df.empty:
                print('El ID ingresado no se encuentra en la base de datos')
                print('Por favor, ingrese el id correcto')
                continue
            mostrar_estado(df)
            break
        except ValueError:
            print('El id ingresado no es válido')
            continue


def ingresar_dni_empleado():
    '''
    Muestra el menú para los empleados solicitando su DNI.
    Si el DNI existe en la base de datos empleado, devuelve los datos del empleado.
    Sino vuelve a solicitarlo.
    Si se ingresa el valor 0, se vuelve al menú de bienvenida
    '''
    while True:
        try:
            dni = int(input('Ingrese su DNI o presione 0 para volver al menu anterior: '))
            if dni == 0:
                return None, None, None, None
            else:
                df = verificar_dni_empleado(dni)
                if df.empty:
                    print('El DNI ingresado no se encuentra en la base de datos de empleados')
                    continue
                return df['DNI'][0], df['puesto'][0], df['nombre'][0], df['apellido'][0]
        except ValueError:
            print('El dni ingresado no es válido')
            print('Por favor verifique los valores ingresados')
            continue


def mostrar_opciones_empleado():
    '''
    
    '''
    diccionario_opciones = {1: 'Ver trámites iniciados',
                            2: 'Resolver siguiente trámite',
                            3: 'Volver al inicio'}
    while True:
        print('¿Qué desea hacer?')
        mostrar_opciones(diccionario_opciones)
        try:
            opcion = int(input('Ingrese la opción deseada: '))
            if opcion not in [1, 2, 3]:
                print('La opción ingresada no es correcta')
                print('Por favor seleccione la opción correcta')
                print('-'*30)
                continue
            print('-'*30)
            return opcion
        except ValueError:
            print('El valor ingresado no es válido.')
            print('Por favor seleccione la opción correcta')


def determinar_opcion_empleado(opcion, puesto):
    '''
    
    '''
    if opcion == 1:
        df = mostrar_tramites_iniciados(puesto)
        if not df.empty:
            print(df[['id_tramite', 'DNI', 'tramite',
                      'estado', 'horario_solicitud']])
        else:
            print('No se encontraron trámites con estado \'iniciado\'')
    elif opcion == 2:
        resolver = resolver_siguiente_tramite(puesto)
        if resolver is not None:
            print(resolver)
            actualizar_estado_tramite(resolver)
    elif opcion == 3:
        mensaje_bienvenida()


def mostrar_empleado():
    '''
    
    '''
    dni, puesto, nombre, apellido = ingresar_dni_empleado()
    if dni is not None:
        print("{:-^30}".format(' GESTIÓN EMPLEADOS '))
        print(f'Bienvenido/a {nombre} {apellido} al sistema')
        print(f'DNI: {dni}')
        print(f'Puesto: {puesto.upper()}')
        opcion = mostrar_opciones_empleado()
        while opcion != 3:
            determinar_opcion_empleado(opcion, puesto)
            print('-'*30)
            opcion = mostrar_opciones_empleado()
