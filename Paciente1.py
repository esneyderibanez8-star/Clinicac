import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from Persona1 import Persona


ARCHIVO = Path(__file__).with_name("Paciente.txt")
ARCHIVO_ANTERIOR = Path(__file__).with_name("Paciente.datos")


class Paciente(Persona):
    def __init__(self, ide, nombres, edad, historia):
        super().__init__(ide, nombres)
        self.edad = int(edad)
        self.historia = historia
        self.medico = None

    def asignar_medico(self, medico):
        if self.medico is medico:
            return
        if self.medico and self in self.medico.pacientes:
            self.medico.pacientes.remove(self)
        self.medico = medico
        if medico and self not in medico.pacientes:
            medico.pacientes.append(self)


def guardar_pacientes(pacientes):
    registros = [
        {"ide": p.id, "nombres": p.nombres, "edad": p.edad, "historia": p.historia}
        for p in pacientes
    ]
    temporal = ARCHIVO.with_suffix(".tmp")
    temporal.write_text(json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8")
    temporal.replace(ARCHIVO)


def cargar_pacientes():
    archivo = ARCHIVO if ARCHIVO.exists() else ARCHIVO_ANTERIOR
    if not archivo.exists():
        return []
    try:
        datos = json.loads(archivo.read_text(encoding="utf-8"))
        if not isinstance(datos, list):
            raise ValueError("El archivo debe contener una lista de pacientes.")
        pacientes = [Paciente(**registro) for registro in datos]
        if archivo == ARCHIVO_ANTERIOR:
            guardar_pacientes(pacientes)
        return pacientes
    except (OSError, TypeError, json.JSONDecodeError) as error:
        raise ValueError(f"No se pudo leer {archivo.name}: {error}") from error


def crear_interfaz(parent, pacientes, medicos):
    tk.Label(parent, text="Registro de pacientes", bg="#b8d6e8", fg="#203746",
             font=("Arial", 12, "bold"), padx=8, pady=7).pack(fill="x", padx=10, pady=(10, 0))
    panel = tk.LabelFrame(parent, padx=10, pady=10)
    panel.pack(fill="x", padx=10, pady=10)
    etiquetas = ("Identificación", "Nombre", "Edad", "Historia clínica", "ID del médico (opcional)")
    entradas = []
    for fila, texto in enumerate(etiquetas):
        tk.Label(panel, text=texto).grid(row=fila, column=0, sticky="e", padx=5, pady=3)
        entrada = tk.Entry(panel)
        entrada.grid(row=fila, column=1, sticky="ew", padx=5, pady=3)
        entradas.append(entrada)
    panel.columnconfigure(1, weight=1)

    columnas = ("id", "nombre", "edad", "historia", "medico")
    tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=7)
    for columna, titulo in zip(columnas, ("ID", "Nombre", "Edad", "Historia", "Médico asignado")):
        tabla.heading(columna, text=titulo)
        tabla.column(columna, width=130, anchor="center")
    tabla.pack(fill="both", expand=True, padx=10, pady=10)
    seleccionado = [None]

    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        for p in pacientes:
            tabla.insert("", "end", iid=p.id, values=(
                p.id, p.nombres, p.edad, p.historia,
                p.medico.nombres if p.medico else "Sin asignar"))

    def limpiar():
        for entrada in entradas:
            entrada.delete(0, tk.END)
        seleccionado[0] = None
        tabla.selection_remove(tabla.selection())

    def seleccionar(_evento=None):
        ids = tabla.selection()
        if not ids:
            return
        p = next((item for item in pacientes if item.id == ids[0]), None)
        if p is None:
            return
        seleccionado[0] = p.id
        valores = (p.id, p.nombres, p.edad, p.historia, p.medico.id if p.medico else "")
        for entrada, valor in zip(entradas, valores):
            entrada.delete(0, tk.END)
            entrada.insert(0, str(valor))

    def guardar():
        ide, nombre, edad_txt, historia, medico_id = [e.get().strip() for e in entradas]
        if not all((ide, nombre, edad_txt, historia)):
            messagebox.showwarning("Datos incompletos", "Completa identificación, nombre, edad e historia.", parent=parent)
            return
        try:
            edad = int(edad_txt)
            if edad < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Edad inválida", "La edad debe ser un entero mayor o igual que cero.", parent=parent)
            return

        anterior = next((p for p in pacientes if p.id == seleccionado[0]), None)
        if any(p.id == ide and p is not anterior for p in pacientes):
            messagebox.showerror("ID repetido", "Ya existe un paciente con esa identificación.", parent=parent)
            return
        medico = next((m for m in medicos if m.id == medico_id), None) if medico_id else None
        if medico_id and medico is None:
            messagebox.showerror("Médico no encontrado", "Revisa el ID o registra primero al médico.", parent=parent)
            return

        actualizado = Paciente(ide, nombre, edad, historia)
        actualizado.medico = medico
        nuevos = [actualizado if p is anterior else p for p in pacientes]
        if anterior is None:
            nuevos.append(actualizado)
        try:
            guardar_pacientes(nuevos)
        except OSError as error:
            messagebox.showerror("Error al guardar", f"No se pudo escribir Paciente.txt: {error}", parent=parent)
            return
        if anterior and anterior.medico and anterior in anterior.medico.pacientes:
            anterior.medico.pacientes.remove(anterior)
        pacientes[:] = nuevos
        if medico and actualizado not in medico.pacientes:
            medico.pacientes.append(actualizado)
        actualizar_tabla()
        limpiar()

    def eliminar():
        ids = tabla.selection()
        if not ids:
            messagebox.showwarning("Selecciona un paciente", "Selecciona un paciente de la tabla.", parent=parent)
            return
        paciente = next((p for p in pacientes if p.id == ids[0]), None)
        if paciente is None or not messagebox.askyesno(
                "Confirmar eliminación", f"¿Eliminar a {paciente.nombres}?", parent=parent):
            return
        restantes = [p for p in pacientes if p is not paciente]
        try:
            guardar_pacientes(restantes)
        except OSError as error:
            messagebox.showerror("Error al guardar", f"No se pudo actualizar Paciente.txt: {error}", parent=parent)
            return
        paciente.asignar_medico(None)
        pacientes[:] = restantes
        actualizar_tabla()
        limpiar()

    botones = tk.Frame(panel)
    botones.grid(row=len(etiquetas), column=0, columnspan=2, pady=8)
    tk.Button(botones, text="Guardar / actualizar", command=guardar).pack(side="left", padx=4)
    tk.Button(botones, text="Eliminar seleccionado", command=eliminar).pack(side="left", padx=4)
    tk.Button(botones, text="Limpiar", command=limpiar).pack(side="left", padx=4)
    tabla.bind("<<TreeviewSelect>>", seleccionar)
    actualizar_tabla()


def crear_interfaz_resumen(parent, pacientes):
    tk.Label(parent, text="Consulta de datos del paciente", bg="#b8d6e8", fg="#203746",
             font=("Arial", 12, "bold"), padx=8, pady=7).pack(fill="x", padx=10, pady=(10, 0))
    panel = tk.Frame(parent, padx=10, pady=10)
    panel.pack(fill="both", expand=True)
    tk.Label(panel, text="Identificación del paciente").pack(anchor="w")
    busqueda = ttk.Frame(panel)
    busqueda.pack(fill="x", pady=5)
    entrada = tk.Entry(busqueda)
    entrada.pack(side="left", fill="x", expand=True, padx=(0, 6))
    tabla = ttk.Treeview(panel, columns=("dato", "valor"), show="headings", height=10)
    tabla.heading("dato", text="Dato")
    tabla.heading("valor", text="Información")
    tabla.column("dato", width=180, anchor="w")
    tabla.column("valor", width=520, anchor="w")
    tabla.pack(fill="both", expand=True, pady=8)

    def consultar():
        p = next((item for item in pacientes if item.id == entrada.get().strip()), None)
        if p is None:
            messagebox.showerror("Paciente no encontrado", "No se encontró ese ID.", parent=parent)
            return
        tabla.delete(*tabla.get_children())
        datos = (("Identificación", p.id), ("Nombre", p.nombres),
                 ("Edad", p.edad), ("Historia clínica", p.historia),
                 ("Médico asignado", p.medico.nombres if p.medico else "Sin asignar"))
        for dato, valor in datos:
            tabla.insert("", "end", values=(dato, valor))

    tk.Button(busqueda, text="Consultar", command=consultar).pack(side="right")
    entrada.bind("<Return>", lambda _evento: consultar())
