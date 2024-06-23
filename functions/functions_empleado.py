from functions.base_datos_sqlserver import ejecutar_consulta
from functions.base_datos_sqlserver import eliminar_todos_registros
from functions.base_datos_sqlserver import agregar_registro_a_base_datos
from functions.personas import Empleado
from settings.settings import base_datos, tabla_empleados
from settings.settings import servidor, tabla_tramites


def crear_tabla_empleados():
    '''
    Crea la tabla empleados.
    Se asignaron 3 empleados
    '''
    empleado1 = Empleado('Alumbrado', 33787488, 'Sabrina',
                         'Sanches')
    empleado2 = Empleado('Poda', 38345678, 'Florencia',
                         'Sánchez')
    empleado3 = Empleado('Licencias', 45789963, 'Christian',
                         'Velásquez')
    empleados = [empleado1, empleado2, empleado3]
    cantidad_empleados = len(empleados)
    empleados_tabla = contar_empleados(base_datos)
    if cantidad_empleados != empleados_tabla:
        eliminar_todos_registros(base_datos, tabla_empleados)
        for empleado in empleados:
            agregar_registro_a_base_datos(servidor, base_datos,
                                          tabla_empleados,
                                          empleado.obtener_df())


def contar_empleados(nombre_base_datos):
    '''
    Cuenta la cantidad de empleados en la tabla empleados
    '''
    consulta = f"SELECT COUNT(*) AS cantidad FROM {tabla_empleados}"
    df = ejecutar_consulta(nombre_base_datos, consulta)
    cantidad = df['cantidad'][0]
    return cantidad


def cambiar_estado_tramite() -> str:  # Para Empleado
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


def verificar_dni_empleado(dni):
    '''
    Recibe un dni.
    Busca ese dni en la tabla empleados.
    Devuelve un dataframe con el resultado de la consulta
    '''
    consulta = f"SELECT * FROM {tabla_empleados} WHERE dni = :dni;"
    df = ejecutar_consulta(base_datos, consulta, {'dni': dni})
    return df


def mostrar_tramites_iniciados(puesto):
    '''
    Recibe un puesto (str).
    Devuelve un dataframe con los trámites con estado iniciado según
    el puesto del empleado.
    '''
    puesto_tramite = {'Poda': 'Poda',
                      'Licencias': 'Alta Licencias',
                      'Alumbrado': 'Alumbrado'}
    tramite = puesto_tramite[puesto]
    estado = 'iniciado'
    consulta = f'SELECT * from {tabla_tramites} WHERE estado = :estado AND tramite = :tramite'
    df = ejecutar_consulta(base_datos, consulta, {'estado': estado,
                                                  'tramite': tramite})
    return df


def resolver_siguiente_tramite(puesto):
    '''
    Recibe un puesto.
    Devuelve una serie con el trámite con estado iniciado que primero 
    se haya solicitado.
    Si no hay trámites con estado iniciado, muestra un mensaje y devuelve
    None
    '''
    df = mostrar_tramites_iniciados(puesto)
    if not df.empty:
        tramite_a_resolver = df.iloc[0]
        return tramite_a_resolver
    print('No hay trámites que resolver'.upper())
    return None


def actualizar_estado_tramite(tramite_a_resolver):
    '''
    Recibe una serie con un trámite con estado iniciado.
    Modifica el estado según el valor ingresado.
    '''
    id_tramite = int(tramite_a_resolver['id_tramite'])
    nuevo_estado = cambiar_estado_tramite()
    consulta = f"UPDATE {tabla_tramites} SET estado = :estado WHERE id_tramite = :id_tramite"
    ejecutar_consulta(base_datos, consulta, {'estado': nuevo_estado,
                                             'id_tramite': id_tramite})
    print('-'*30)
    print(f'El estado del trámite con id: {id_tramite} ha sido modificado a {nuevo_estado.upper()}')
