import pandas as pd


class Persona:
    def __init__(self, nombre, apellido, DNI, telefono, mail=None):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__DNI = DNI
        self.__telefono = telefono
        self.__mail = mail

    def obtener_nombre(self):
        return self.__nombre

    def modificar_nombre(self, nombre):
        self.__nombre = nombre
 
    def obtener_apellido(self):
        return self.__apellido

    def cambiar_apellido(self, apellido):
        self.__apellido = apellido

    def obtener_DNI(self):
        return self.__DNI

    def modificar_DNI(self, DNI):
        self.__DNI = DNI

    def obtener_telefono(self):
        return self.__telefono

    def cambiar_telefono(self, telefono):
        self.__telefono = telefono

    def obtener_mail(self):
        return self.__mail
    
    def cambiar_mail(self, mail):
        self.__mail = mail

    def __str__(self):
        diccionario = {}
        for clave, valor in self.__dict__.items():
            diccionario[clave[10:]] = valor
        return f'{diccionario}'
        # return '\n'.join(f'{atributo[10:]}: {valor}' for atributo, valor in self.__dict__.items())
    
    def obtener_dictionario(self):
        diccionario = {}
        for clave, valor in self.__dict__.items():
            diccionario[clave[10:]] = valor
        return diccionario

    def obtener_df(self):
        return pd.DataFrame([self.obtener_dictionario()])
    

class Solicitante(Persona):
    def __init__(self, tramite: str, estado: str, *args):
        """
        Solicitante pertenece a la clase Persona.
        tramite: tramite que realizará.
        estado: en que estado se encuentra el trámite.
        """
        super().__init__(*args) # inicializamos la clase padre
        self.__tramite = tramite
        self.__estado = estado

    def get_tramite(self):
        return self.__tramite
    
    def set_tramite(self, tramite):
        """
        Modifica el trámite a realizar
        """
        self.__tramite = tramite

    def get_estado(self):
        return self.__estado
    
    def set_estado(self, estado):
        self.__estado = estado





