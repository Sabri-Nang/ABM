from decouple import config

servidor = config('DB_SERVER')
base_datos = config('DB_NAME')
tabla_empleados = config('TABLE_EMPLEADOS')
tabla_tramites = config('TABLE_TRAMITES')