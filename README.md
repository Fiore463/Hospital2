# Hospital-T2: Expedientes Digitales (Fase 2)

## Qué hace el sistema
Administra los expedientes digitales del personal del Hospital de Diagnóstico. Permite registrar empleados, consultar el estado de sus documentos según su perfil, modificar el estado de un documento y eliminar empleados. El resumen clasifica cada expediente como completo o incompleto y cuenta cuántos hay de cada tipo.

## Cómo ejecutarlo
```
pip install flask
python crear_bd.py
python app.py
```
Abrir en el navegador:
- http://127.0.0.1:5000/empleados
- http://127.0.0.1:5000/empleados/nuevo
- http://127.0.0.1:5000/resumen

## Estructura de archivos
```
app.py          rutas de Flask y lógica del sistema
crear_bd.py     crea las tablas y carga 5 empleados de ejemplo
README.md       documentación
templates/      base.html, empleados.html, nuevo.html, editar.html, resumen.html
static/         style.css (única hoja de estilos)
```

## Rutas
| Ruta | Método | Qué hace |
|---|---|---|
| `/empleados` | GET | Lista empleados con el estado de cada documento y de su expediente |
| `/empleados/nuevo` | GET, POST | Formulario de registro con validación |
| `/empleados/eliminar/<id>` | POST | Elimina un empleado y sus documentos (pide confirmación) |
| `/documentos/editar/<id>` | GET, POST | Modifica el estado de un documento con validación |
| `/resumen` | GET | Clasifica y cuenta los expedientes |

## Base de datos (SQLite: hospital.db)
- `empleados`: id (entero), nombre (texto), perfil (texto), fecha_ingreso (texto), correo (texto)
- `checklist`: id (entero), perfil (texto), documento (texto)
- `documentos`: id (entero), empleado_id (entero), documento (texto), estado (texto: Completo o Pendiente)

## Cómo funciona el resumen
Lee todos los empleados y recorre cada uno con `for`. Para cada empleado revisa sus documentos con otro `for` y cuenta los pendientes. Luego decide con `if/elif/else`: sin documentos requeridos, completo (0 pendientes) o incompleto (1 o más). Tres contadores acumulan cuántos hay de cada clasificación y se muestran con colores distintos (verde, rojo, amarillo).

## Equipo: parte de código desarrollada por cada integrante
- Nombre 1: implementó `crear_bd.py`, la conexión y la estructura del repositorio
- Nombre 2: implementó el registro con validación y la eliminación
- Nombre 3: implementó el listado y la modificación con validación
- Nombre 4: implementó el resumen (bucle, decisión y contadores) y `style.css`
