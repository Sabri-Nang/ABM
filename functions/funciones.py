def saludar(nombre='Sabrina'):
    print(f'Hola {nombre}')

class Persona:
    def __init__(self, nombre, apellido):
        self.__nombre = nombre
        self.apellido = apellido

    def __str__(self):
        return f'{self.__nombre} {self.apellido}'
    
    def obtener_nombre(self):
        return self.__nombre
    

