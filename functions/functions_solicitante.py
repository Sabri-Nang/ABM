from datetime import timedelta
import pandas as pd
from typing import Tuple
from settings.settings import base_datos, tabla_tramites, servidor
from functions.personas import Solicitante
from functions.base_datos_sqlserver import ejecutar_consulta
from functions.base_datos_sqlserver import agregar_registro_a_base_datos


def contar_datos_estado(estado: str, tramite: str) -> int:
    consulta = f"SELECT COUNT(*) AS cantidad FROM {tabla_tramites} WHERE estado = :estado AND tramite = :tramite;"
    df = ejecutar_consulta(base_datos, consulta, {'estado': estado,
                                                  'tramite': tramite})
    cantidad = df['cantidad'][0]
    return cantidad


def obtener_id_tramite() -> int:
    consulta = f"select top 1 id_tramite from {tabla_tramites} order by id_tramite desc;"
    df = ejecutar_consulta(base_datos, consulta)
    id_tramite = df['id_tramite'][0]
    return id_tramite


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


def solicitar_tipo_tramite() -> Tuple[int, str]:
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


def registrar_solicitante() -> Tuple[int, str, Solicitante]:
    DNI = solicitar_dni()
    tramite_seleccionado, tipo_tramite = solicitar_tipo_tramite()
    estado = 'iniciado'
    solicitante = Solicitante(tipo_tramite, estado, DNI)
    return tramite_seleccionado, tipo_tramite, solicitante


def calcular_espera(cantidad) -> Tuple[int, int]:
    cinco_minutos = timedelta(minutes=5)
    tiempo_espera = cantidad * cinco_minutos
    segundos = tiempo_espera.total_seconds()
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    return int(horas), int(minutos)


def ingresar_solicitante():
    tramite, tipo_tramite, solicitante = registrar_solicitante()
    cantidad = contar_datos_estado(estado='iniciado', tramite=tipo_tramite)
    print('-'*30)
    print(f'Usuario: {solicitante.obtener_DNI()}')
    print(f'El tramite seleccionado es: {tipo_tramite}')
    print(f'Usted tiene {cantidad} personas antes')
    horas, minutos = calcular_espera(cantidad)
    print(f'El tiempo de espera es {horas} horas y {minutos} minutos')
    agregar_registro_a_base_datos(servidor, base_datos,
                                  tabla_tramites, solicitante.obtener_df())
    id_tramite = obtener_id_tramite()
    print(f'Su ID de trámite es: {id_tramite}')
    print('Muchas gracias por utilizar el servicio')
    print('-'*30)


def obtener_estado_tramite(id_tramite) -> pd.DataFrame:
    consulta = f"SELECT * FROM {tabla_tramites} WHERE id_tramite = :id_tramite;"
    df = ejecutar_consulta(base_datos, consulta, {'id_tramite': id_tramite})
    return df
