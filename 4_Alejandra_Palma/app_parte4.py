# ALEJANDRA PALMA: resumen con repetición, decisión y contadores
@app.route("/resumen")
def resumen():
    conexion = conectar()
    empleados = conexion.execute("SELECT * FROM empleados ORDER BY id").fetchall()

    completos = 0
    incompletos = 0
    sin_checklist = 0
    detalle = []

    for emp in empleados:
        docs = conexion.execute(
            "SELECT estado FROM documentos WHERE empleado_id = ?", (emp["id"],)).fetchall()
        total = len(docs)
        pendientes = 0
        for d in docs:
            if d["estado"] == "Pendiente":
                pendientes = pendientes + 1

        if total == 0:
            clase = "sinchecklist"
            texto = "Sin documentos requeridos"
            sin_checklist = sin_checklist + 1
        elif pendientes == 0:
            clase = "completo"
            texto = "Completo"
            completos = completos + 1
        else:
            clase = "incompleto"
            texto = "Incompleto"
            incompletos = incompletos + 1

        detalle.append({"nombre": emp["nombre"], "perfil": emp["perfil"],
                        "pendientes": pendientes, "total": total,
                        "clase": clase, "texto": texto})

    conexion.close()
    return render_template("resumen.html", detalle=detalle, completos=completos,
                           incompletos=incompletos, sin_checklist=sin_checklist,
                           total=len(empleados))


if __name__ == "__main__":
    app.run(debug=True)
