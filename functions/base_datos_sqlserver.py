from decouple import config
import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table


def crear_base_datos(servidor, nombre_base_datos):
    '''
    Conecta al servidor y crea una base de datos.
    Recibe el servidor (str) y el nombre de la base de datos a crear (str).
    Si la base ya existe, muestra un mensaje indicando que ya existe
    '''
    connection_string = f"mssql+pyodbc://{servidor}/master?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    engine = create_engine(connection_string)
    # Crear el motor de SQLAlchemy
    engine = create_engine(connection_string, isolation_level="AUTOCOMMIT")

    # Crear la conexión
    with engine.connect() as connection:
        # Verificar si la base de datos ya existe
        result = connection.execute(text(f"SELECT * FROM sys.databases WHERE name = '{nombre_base_datos}'"))
        database_exists = result.fetchone() is not None
        if not database_exists:
            # Crear la base de datos
            connection.execute(text(f"CREATE DATABASE {nombre_base_datos}"))
            print(f"Se ha creado la base de datos '{nombre_base_datos}' exitosamente.")
        else:
            print(f"La base de datos '{nombre_base_datos}' ya existe.")


def eliminar_base_datos(servidor, nombre_base_datos):
    '''
    Elimina una base de datos del servidor.
    Recibe el servidor y el nombre de la base de datos a eliminar.
    Si la base de datos no existe, muestra un mensaje indicándolo
    '''
    # Cadena de conexión a la base de datos 'master' para poder eliminar
    # una base de datos
    connection_string = f"mssql+pyodbc://{servidor}/master?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    # Crear el motor de SQLAlchemy
    engine = create_engine(connection_string, isolation_level="AUTOCOMMIT")
    # Crear la conexión
    with engine.connect() as connection:
        # Verificar si la base de datos existe
        result = connection.execute(text(f"SELECT * FROM sys.databases WHERE name = '{nombre_base_datos}'"))
        database_exists = result.fetchone() is not None
        if database_exists:
            # Terminar conexiones activas a la base de datos
            connection.execute(text(f"""
                ALTER DATABASE {nombre_base_datos} SET SINGLE_USER WITH ROLLBACK IMMEDIATE
            """))
            # Eliminar la base de datos
            connection.execute(text(f"DROP DATABASE {nombre_base_datos}"))
            print(f"Se ha eliminado la base de datos '{nombre_base_datos}' exitosamente.")
        else:
            print(f"La base de datos '{nombre_base_datos}' no existe.")


def verificar_tabla_existe(servidor, nombre_base_datos, nombre_tabla):
    '''
    Recibe un servidor, el nombre de una base de datos y el nombre de una
    tabla.
    Verifica si la tabla existe en esa base de datos.
    Devuelve un booleano.
    '''
    # Cadena de conexión a la base de datos específica
    connection_string = f"mssql+pyodbc://{servidor}/{nombre_base_datos}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    engine = create_engine(connection_string)
    # Crear la conexión
    with engine.connect() as connection:
        # Consulta para verificar si la tabla existe
        query = text("""
            SELECT 1
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = :nombre_tabla
        """)
        result = connection.execute(query, {"nombre_tabla": nombre_tabla})
        tabla_existe = result.fetchone() is not None
    return tabla_existe


def eliminar_tabla(servidor, nombre_base_datos, nombre_tabla):
    '''
    Recibe un servidor, el nombre de la base de datos y el nombre de una
    tabla.
    Si la tabla existe en la base de datos, la elimina.
    Si no existe, muestra un mensaje advirtiendo que no existe
    '''
    # Cadena de conexión a la base de datos específica
    connection_string = f"mssql+pyodbc://{servidor}/{nombre_base_datos}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    engine = create_engine(connection_string)
    connection = engine.connect()
    # MetaData para reflejar las tablas existentes
    metadata = MetaData()
    metadata.reflect(bind=engine)
    if nombre_tabla in metadata.tables:
        # Reflejar la tabla
        tabla = Table(nombre_tabla, metadata, autoload_with=engine)
        # Eliminar la tabla
        tabla.drop(engine)
        print(f"La tabla '{nombre_tabla}' ha sido eliminada de la base de datos '{nombre_base_datos}'.")
    else:
        print(f"La tabla '{nombre_tabla}' no existe en la base de datos '{nombre_base_datos}'.")
    # Cerrar la conexión
    connection.close()


def crear_tabla(servidor, nombre_base_datos, nombre_tabla, dataframe):
    '''
    Recibe un servidor, el nombre de la base de datos, el nombre de la tabla
    y un dataframe.
    Si la tabla existe, reemplaza los valores por los del dataframe.
    Si no existe, la crea a partir del dataframe
    '''
    connection_string = f"mssql+pyodbc://{servidor}/{nombre_base_datos}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    engine = create_engine(connection_string)
    dataframe.to_sql(nombre_tabla, con=engine, index=False, if_exists='replace')
    print(f"Se ha creado tabla '{nombre_tabla}' en la base de datos '{nombre_base_datos}' exitosamente.")


def agregar_registro_a_base_datos(servidor, nombre_base_datos,
                                  nombre_tabla, dataframe):
    '''
    Recibe un servidor, el nombre de una base de datos, el nombre de la tabla
    y un dataframe.
    Agrega el dataframe a la tabla en la base de datos.
    '''
    connection_string = f"mssql+pyodbc://{servidor}/{nombre_base_datos}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    engine = create_engine(connection_string)
    # Agregar el DataFrame a la base de datos
    dataframe.to_sql(nombre_tabla, con=engine, if_exists='append', index=False)
    # print(f"Se ha agregado el registro {dataframe} a la tabla '{nombre_tabla}' 
    # en la base de datos '{nombre_base_datos}' exitosamente.")


def ejecutar_consulta(nombre_base_datos, consulta, params=None):
    '''
    Recibe el nombre de una base de datos, una consulta y un diccionario de
    parámetros, por defecto None.
    Ejecuta la consulta, en caso de que la consulta devuelva un resultado,
    retorna un dataframe con los resultados.
    Sino retorna None.
    '''
    servidor = config('DB_SERVER')
    connection_string = f"mssql+pyodbc://{servidor}/{nombre_base_datos}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        resultado = conn.execute(text(consulta), params)
        if resultado.returns_rows:
            df = pd.DataFrame(resultado.fetchall(), columns=resultado.keys())
            return df
        else:
            conn.commit()
            return None


def mostrar_tabla(nombre_base_datos, nombre_tabla):
    '''
    Recibe el nombre de la base de datos y una tabla.
    Devuelve e imprime la tabla como un dataframe
    '''
    consulta = f"SELECT * FROM {nombre_tabla}"
    df = ejecutar_consulta(nombre_base_datos, consulta)
    print(df)
    return df


def eliminar_todos_registros(nombre_base_datos, nombre_tabla):
    '''
    Recibe una base de datos y el nombre de una tabla.
    Elimina todos los registros de la tabla.
    '''
    consulta = f"delete from {nombre_tabla}"
    ejecutar_consulta(nombre_base_datos, consulta)
