from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from settings.settings import servidor, base_datos, tabla_empleados
from settings.settings import tabla_tramites
from functions.base_datos_sqlserver import crear_base_datos

# Cadena de conexión a la base de datos específica
connection_string = f"mssql+pyodbc://{servidor}/{base_datos}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(connection_string)

# Definir la estructura de la tabla utilizando SQLAlchemy
Base = declarative_base()


class Tramites(Base):
    '''
    Tabla de trámites
    '''
    __tablename__ = tabla_tramites
    id_tramite = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=True)
    apellido = Column(String, nullable=True)
    telefono = Column(Integer, nullable=True)
    mail = Column(String, nullable=True)
    DNI = Column(String, nullable=False)
    tramite = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    horario_solicitud = Column(DateTime, nullable=False)


class Empleados(Base):
    '''
    Tabla de empleados
    '''
    __tablename__ = tabla_empleados
    id_empleado = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=True)
    apellido = Column(String, nullable=True)
    telefono = Column(Integer, nullable=True)
    mail = Column(String, nullable=True)
    DNI = Column(String, nullable=False)
    puesto = Column(String, nullable=False)


def crear_tablas():
    '''
    Crea la base de datos en el servidor si no existe.
    Luego crea las tablas.
    '''
    crear_base_datos(servidor, base_datos)
    Base.metadata.create_all(engine)
    print(f"Se ha creado la tabla {tabla_tramites} en la base de datos {base_datos}.")
    print(f"Se ha creado la tabla {tabla_empleados} en la base de datos {base_datos}")
