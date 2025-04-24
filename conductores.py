import pandas as pd
import pyodbc

# 1) Cargo y limpio el DataFrame
df = pd.read_excel(
    r'C:\Users\rrs23\OneDrive\Documentos\OneDrive\Documentos\Datos\BaseQ.xlsx',
    sheet_name='Base Principal'
)

# Limpio espacios y renombro
df.columns = df.columns.str.strip()
df.rename(columns={
    'Conductor': 'nombre_conductor',
    'Documento del Conductor del Recurso': 'documento_conductor'
}, inplace=True)

# 2) Sanear 'documento_conductor' a entero
df['documento_conductor'] = (
    df['documento_conductor']
    .astype(str)
    .str.replace(r'[^\d]', '', regex=True)  # quita no dígitos
    .replace('', '0')                       # convierte vacíos en '0'
    .astype(int)
)

# 3) Extraer solo filas únicas
df_cd = df[['documento_conductor', 'nombre_conductor']].drop_duplicates()

# 4) Conexión y vacío la tabla
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=quick;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()
cursor.execute("DELETE FROM Conductores;")
conn.commit()

# 5) Inserción
for _, row in df_cd.iterrows():
    nombre = row.nombre_conductor.strip() if isinstance(row.nombre_conductor, str) else ''
    cursor.execute("""
        INSERT INTO Conductores (documento_conductor, nombre_conductor)
        VALUES (?, ?)
    """, row.documento_conductor, nombre)
conn.commit()

# 6) Verificación
cursor.execute("SELECT COUNT(*) FROM Conductores;")
print("Conductores cargados:", cursor.fetchone()[0])

conn.close()

