import pandas as pd


class Base_Datos:
    def __init__(self):
        self.cantidad_datos = 0
        self.datos = pd.DataFrame()

    def agregar_persona(self, persona):
        persona_df = persona.obtener_df()
        self.datos = pd.concat([self.datos, persona_df],
                               axis=0, ignore_index=True)

    def buscar_persona(self, persona_nombre):
        if len(self.datos.query(f"name == '{persona_nombre}'")) >= 1:
            registros = len(self.datos.query(f"name == '{persona_nombre}'"))
            print(f'Se encontraron {registros} con el nombre {persona_nombre}')
            return True
        print(f'No se encontraron registros con el nombre {persona_nombre}')
        return False

    def eliminar_persona(self, persona_nombre):
        if self.buscar_persona(persona_nombre):
            datos_filtrados = self.datos[self.datos['name'] != persona_nombre]
            for index, row in self.datos[self.datos['name'] == persona_nombre].iterrows():
                print(f'Se elimino la fila {index}: {self.datos.iloc[index]}')
            self.datos = datos_filtrados
            return True
        return False
    
    def to_csv(self, nombre):
        return self.datos.to_csv(path_or_buf=nombre, sep=',', index=False)

    def __str__(self):
        return f'{self.datos}'