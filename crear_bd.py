# crear_bd.py - crea las tablas y carga datos de ejemplo (PERSONA 1)
import sqlite3

# Documentos que exige cada perfil (antes estaba fijo en Hospital-T2.py)
DOCUMENTOS_PERFIL = {
    "administrativo": ["DUI", "Título", "Antecedentes Penal", "Solvencia PNP"],
    "medico": ["DUI", "Título", "Antecedentes Penal", "Solvencia PNP", "Colegiatura médica", "Especialidad"],
    "enfermeria": ["DUI", "Título", "Antecedentes Penal", "Solvencia PNP", "Junta de Vigilancia"],
}

# nombre, perfil, fecha de ingreso, correo, documentos que ya entregó
EMPLEADOS = [
    ("Ana", "administrativo", "2022-03-15", "ana@hospital.com",
     ["DUI", "Título", "Antecedentes Penal", "Solvencia PNP"]),
    ("Carlos", "medico", "2021-07-01", "carlos@hospital.com",
     ["DUI", "Título", "Antecedentes Penal", "Colegiatura médica"]),
    ("Maria", "enfermeria", "2023-01-10", "maria@hospital.com",
     ["DUI", "Título", "Antecedentes Penal", "Solvencia PNP", "Junta de Vigilancia"]),
    ("Luis", "administrativo", "2024-05-20", "luis@hospital.com",
     ["DUI"]),
    ("Sofia", "medico", "2020-11-02", "sofia@hospital.com",
     ["DUI", "Título", "Antecedentes Penal", "Solvencia PNP", "Colegiatura médica", "Especialidad"]),
]

conexion = sqlite3.connect("hospital.db")

conexion.execute("DROP TABLE IF EXISTS documentos")
conexion.execute("DROP TABLE IF EXISTS empleados")
conexion.execute("DROP TABLE IF EXISTS checklist")

conexion.execute("""CREATE TABLE checklist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    perfil TEXT NOT NULL,
    documento TEXT NOT NULL)""")

conexion.execute("""CREATE TABLE empleados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    perfil TEXT NOT NULL,
    fecha_ingreso TEXT NOT NULL,
    correo TEXT NOT NULL)""")

conexion.execute("""CREATE TABLE documentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empleado_id INTEGER NOT NULL,
    documento TEXT NOT NULL,
    estado TEXT NOT NULL)""")

for perfil, docs in DOCUMENTOS_PERFIL.items():
    for doc in docs:
        conexion.execute("INSERT INTO checklist (perfil, documento) VALUES (?, ?)", (perfil, doc))

for nombre, perfil, fecha, correo, entregados in EMPLEADOS:
    cursor = conexion.execute(
        "INSERT INTO empleados (nombre, perfil, fecha_ingreso, correo) VALUES (?, ?, ?, ?)",
        (nombre, perfil, fecha, correo))
    emp_id = cursor.lastrowid
    for doc in DOCUMENTOS_PERFIL[perfil]:
        if doc in entregados:
            estado = "Completo"
        else:
            estado = "Pendiente"
        conexion.execute(
            "INSERT INTO documentos (empleado_id, documento, estado) VALUES (?, ?, ?)",
            (emp_id, doc, estado))

conexion.commit()
conexion.close()
print("Base de datos hospital.db creada con", len(EMPLEADOS), "empleados.")
