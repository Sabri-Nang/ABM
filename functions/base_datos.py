import pandas as pd


class Base_Datos:
    def __init__(self):
        self.cantidad_datos = 0
        self.datos = pd.DataFrame()

    def agregar_registro(self, registro):
        self.cantidad_datos += 1
        registro_df = registro.obtener_df()
        self.datos = pd.concat([self.datos, registro_df],
                               axis=0, ignore_index=True)

    def buscar_registro(self, atributo, valor):
        if len(self.datos.query(f"{atributo} == '{valor}'")) >= 1:
            registros = len(self.datos.query(f"{atributo} == '{valor}'"))
            print(f'Se encontraron {registros} con el {atributo} {valor}')
            return True
        print(f'No se encontraron registros con el {atributo} {valor}')
        return False

    def eliminar_registro(self, atributo, valor):
        if self.buscar_registro(atributo, valor):
            datos_filtrados = self.datos[self.datos[f'{atributo}'] != valor]
            for index, row in self.datos[self.datos[f'{atributo}'] == valor].iterrows():
                print(f'Se elimino la fila {index}: {self.datos.iloc[index]}')
            self.datos = datos_filtrados
            self.cantidad_datos = self.size
            return True
        return False
    
    def to_csv(self, nombre):
        return self.datos.to_csv(path_or_buf=nombre, sep=',', index=False)

    def __str__(self):
        return f'{self.datos}'
    
