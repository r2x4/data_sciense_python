import pandas as pd
import pyodbc

# Cargar y limpiar el DataFrame
df = pd.read_excel(
    r'C:\Users\rrs23\OneDrive\Documentos\OneDrive\Documentos\Datos\BaseQ.xlsx',
    sheet_name='Base Principal'
)

# Limpio espacios y renombro
df.columns = df.columns.str.strip()
df.rename(columns={
    'Correo Cliente': 'correo_cliente',
    'No Aplica': 'no_aplica',
    'Numero Telefonicorepresentante': 'telefono_representante',
    'ID REFERENCIA CLIENTE ': 'id_referencia_cliente',
}, inplace=True)

# Limpiar columnas numéricas
df['documento_cliente'] = (
    df['documento_cliente']
    .astype(str)
    .str.replace(r'[^\d]', '', regex=True)  # Quitar caracteres no numéricos
    .replace('', '0')                       # Convertir vacíos en '0'
)

# Extraer solo filas únicas
df_clientes = df[['documento_cliente', 'correo_cliente', 'telefono_representante']].drop_duplicates()

# Conexión y vaciar la tabla
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=quick;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Inserción de los datos
for _, row in df_clientes.iterrows():
    # Verificar si el cliente ya existe en la base de datos
    cursor.execute("""
        SELECT COUNT(*) FROM Clientes WHERE documento_cliente = ?
    """, row.documento_cliente)
    
    if cursor.fetchone()[0] == 0:  # Si no existe, insertamos el nuevo cliente
        correo = row.correo_cliente.strip() if isinstance(row.correo_cliente, str) else ''
        telefono = row.telefono_representante.strip() if isinstance(row.telefono_representante, str) else ''
        cursor.execute("""
            INSERT INTO Clientes (documento_cliente, correo_cliente, numero_telefono)
            VALUES (?, ?, ?)
        """, row.documento_cliente, correo, telefono)
        print(f"Cliente con documento {row.documento_cliente} insertado.")
    else:
        print(f"Cliente con documento {row.documento_cliente} ya existe, no se insertó.")

conn.commit()

# Verificación
cursor.execute("SELECT COUNT(*) FROM Clientes;")
print("Clientes cargados:", cursor.fetchone()[0])

conn.close()


