import pandas as pd
import pyodbc

# Cargar datos desde Excel
df = pd.read_excel(
    r'C:\Users\rrs23\OneDrive\Documentos\OneDrive\Documentos\Datos\BaseQ.xlsx', sheet_name='Base Principal')

# Limpiar nombres de columnas
df.columns = df.columns.str.strip()

# Renombrar columnas
df.rename(columns={
    'Tipo de servicio': 'tipo_de_servicio',
    'Tipo de Cirugia ': 'tipo_cirugia',
    'Fecha Cirugia': 'fecha_cirugia',
    'Correo Cliente': 'correo_cliente',
    'No Aplica': 'no_aplica',
    'Numero Telefonicorepresentante': 'telefono_representante',
    'ID REFERENCIA CLIENTE ': 'id_referencia_cliente',
    'Productos Asociados con Error': 'productos_error',
    'Productos Asociados': 'productos_asociados',
    'Correo Usuario Creador': 'correo_usuario_creador',
    'Conductor': 'nombre_conductor',
    'Ciudad': 'ciudad',
    'Documento del Conductor del Recurso': 'documento_conductor',
    'Codigo Cedi': 'codigo_cedi',  # Asegúrate de que esta columna esté renombrada
    'Descripcion': 'descripcion',  # Asegúrate de que esta columna esté presente si la usas
    'Fecha de servicio': 'fecha_de_servicio'  # Asegúrate de que esta columna esté presente
}, inplace=True)

# Limpiar columnas numéricas y asegurarse de que sean enteros
for col in ['documento_conductor', 'documento_cliente']:
    if col in df.columns:
        # Eliminar caracteres no numéricos y convertir a número
        df[col] = df[col].astype(str).str.replace(r'[^\d]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

# Eliminar duplicados antes de insertar (para evitar el error de clave primaria duplicada)
df = df.drop_duplicates(subset=['documento_conductor', 'codigo_cedi'])

# Asegurarse de que las columnas de fecha estén en formato correcto
df['fecha_cirugia'] = pd.to_datetime(df['fecha_cirugia'], errors='coerce')
df['fecha_de_servicio'] = pd.to_datetime(df['fecha_de_servicio'], errors='coerce')

# Conexión a SQL Server
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                        'SERVER=localhost;'
                        'DATABASE=quick;'
                        'Trusted_Connection=yes;')
cursor = conn.cursor()

# Función para insertar datos
def insertar_datos(tabla, query, columnas):
    try:
        for index, row in df.iterrows():
            valores = []
            for columna in columnas:
                valor = row.get(columna, None)
                # Reemplazar None por valores predeterminados si es necesario
                if valor is None:
                    valor = ''  # o 0, según lo que se necesite
                elif isinstance(valor, str):
                    valor = valor.strip()  # Eliminar espacios extras
                valores.append(valor)
            # Ejecutar la inserción con los valores
            cursor.execute(query, tuple(valores))
        conn.commit()  # Confirmar cambios
        print(f"Datos insertados correctamente en la tabla {tabla}.")
    except Exception as e:
        print(f"Error al insertar en la tabla {tabla}: {e}")
        conn.rollback()  # Revertir cambios en caso de error

# Insertar datos en 'Clientes'
insertar_datos('Clientes', """
    INSERT INTO Clientes (documento_cliente, nombre_cliente, numero_telefono, correo_cliente)
    VALUES (?, ?, ?, ?)
""", ['documento_cliente', 'nombre_cliente', 'telefono_representante', 'correo_cliente'])

# Insertar datos en 'Conductores'
insertar_datos('Conductores', """
    INSERT INTO Conductores (documento_conductor, nombre_conductor)
    VALUES (?, ?)
""", ['documento_conductor', 'nombre_conductor'])

# Insertar datos en 'Cedis'
insertar_datos('Cedis', """
    INSERT INTO Cedis (codigo_cedi, nombre_cedi, direccion_servicio, ciudad)
    VALUES (?, ?, ?, ?)
""", ['codigo_cedi', 'nombre_cedi', 'direccion_servicio', 'ciudad'])

# Insertar datos en 'Servicios'
insertar_datos('Servicios', """
    INSERT INTO Servicios (ruta, numero_del_servicio, estado, creado_por, documento_cliente, 
                        documento_conductor, codigo_cedi, fecha_de_servicio, tipo_de_servicio, descripcion)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", ['ruta', 'numero_del_servicio', 'estado', 'creado_por', 'documento_cliente',
    'documento_conductor', 'codigo_cedi', 'fecha_de_servicio', 'tipo_de_servicio', 'descripcion'])

# Cerrar conexión
conn.close()


