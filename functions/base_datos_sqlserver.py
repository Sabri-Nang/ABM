from decouple import config
import pandas as pd
import pyodbc
from sqlalchemy import create_engine, text, MetaData, Table

servidor = config('DB_SERVER')


def crear_base_datos(servidor, nombre_base_datos):
    connection_string = f"mssql+pyodbc://{servidor}/master?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    engine = create_engine(connection_string)
        # Crear la conexión
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
    # Cadena de conexión a la base de datos 'master' para poder eliminar una base de datos
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
    # Cadena de conexión a la base de datos específica
    connection_string = f"mssql+pyodbc://{servidor}/{nombre_base_datos}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    
    # Crear el motor de SQLAlchemy
    engine = create_engine(connection_string)
    
    # Crear la conexión
    with engine.connect() as connection:
        # Consulta para verificar si la tabla existe
        query = text(f"""
            SELECT 1 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = :nombre_tabla
        """)
        result = connection.execute(query, {"nombre_tabla": nombre_tabla})
        tabla_existe = result.fetchone() is not None

    return tabla_existe


def eliminar_tabla(servidor, nombre_base_datos, nombre_tabla):
    # Cadena de conexión a la base de datos específica
    connection_string = f"mssql+pyodbc://{servidor}/{nombre_base_datos}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    engine = create_engine(connection_string)

    # Conectar al motor
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
    connection_string = f"mssql+pyodbc://{servidor}/{nombre_base_datos}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    engine = create_engine(connection_string)
    dataframe.to_sql(nombre_tabla, con=engine, index=False)
    print(f"Se ha creado tabla '{nombre_tabla}' en la base de datos '{nombre_base_datos}' exitosamente.")


def agregar_dataframe_a_base_datos(servidor, nombre_base_datos, nombre_tabla, dataframe):
    connection_string = f"mssql+pyodbc://{servidor}/{nombre_base_datos}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    # Crear el motor de SQLAlchemy
    engine = create_engine(connection_string)
    # Agregar el DataFrame a la base de datos
    dataframe.to_sql(nombre_tabla, con=engine, if_exists='append', index=False)
    print(f"Se ha agregado el DataFrame a la tabla '{nombre_tabla}' en la base de datos '{nombre_base_datos}' exitosamente.")


def ejecutar_consulta(nombre_base_datos, consulta):
    # Cadena de conexión a SQL Server
    servidor = config('DB_SERVER')
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={servidor};DATABASE={nombre_base_datos};Trusted_Connection=yes;"
    # Conectarse a la base de datos
    conn = pyodbc.connect(connection_string)
    # Crear una instancia del cursor
    #cursor = conn.cursor()
    # Ejecutar la consulta para obtener todos los elementos de la tabla
    #query = f"SELECT * FROM {nombre_tabla}"
    # Leer la consulta en un DataFrame
    df = pd.read_sql(consulta, conn)
    # Cerrar la conexión
    conn.close()
    # Mostrar el DataFrame
    return df


def traer_tabla(nombre_base_datos, nombre_tabla):
    consulta = f"SELECT * FROM {nombre_tabla}"
    df = ejecutar_consulta(nombre_base_datos, consulta)
    return df

