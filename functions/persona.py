import pandas as pd


class Persona:
    def __init__(self, name, last_name, DNI=None, phone=None, mail=None):
        self.__name = name
        self.__last_name = last_name
        self.__DNI = DNI
        self.__phone = phone
        self.__mail = mail

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name
 
    def get_last_name(self):
        return self.__last_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def get_DNI(self):
        return self.__DNI

    def set_DNI(self, DNI):
        self.__DNI = DNI

    def get_phone(self):
        return self.__phone

    def set_phone(self, phone):
        self.__phone = phone

    def get_mail(self):
        return self.__mail

    def __str__(self):
        diccionario = {}
        for clave, valor in self.__dict__.items():
            diccionario[clave[10:]] = valor
        return f'{diccionario}'
        # return '\n'.join(f'{atributo[10:]}: {valor}' for atributo, valor in self.__dict__.items())
    
    def get_dictionary(self):
        diccionario = {}
        for clave, valor in self.__dict__.items():
            diccionario[clave[10:]] = valor
        return diccionario

    def get_df(self):
        return pd.DataFrame([self.get_dictionary()])
    


