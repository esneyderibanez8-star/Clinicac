import tkinter as tk
from tkinter import ttk, messagebox

from Persona1 import Persona


class Medico(Persona):
    def __init__(self, ide, nombres, especialidad, tipo, sueldo):
        super().__init__(ide, nombres)
        self.especialidad = especialidad
        self.tipo = tipo
        self.sueldo = float(sueldo)
        self.horarios = []
        self.pacientes = []

    def get_especialidad(self): return self.especialidad
    def set_especialidad(self, especialidad): self.especialidad = especialidad
    def get_tipo(self): return self.tipo
    def set_tipo(self, tipo): self.tipo = tipo
    def get_sueldo(self): return self.sueldo
    def set_sueldo(self, sueldo): self.sueldo = float(sueldo)
    def get_horarios(self): return self.horarios
    def get_pacientes(self): return self.pacientes

    def agregarHorario(self, horario):
        self.horarios.append(horario)

    def agregarPaciente(self, paciente):
        paciente.asignar_medico(self)

    def calcular_sueldo_anual(self):
        return self.sueldo * 12

    def verificar_disponibilidad(self, hora, dia):
        for horario in self.horarios:
            coincide = (horario.hora.strip().casefold() == hora.strip().casefold()
                        and horario.dia.strip().casefold() == dia.strip().casefold())
            if coincide:
                return horario.disponible.strip().casefold() in ("si", "sí", "true", "1")
        return None


def crear_interfaz(parent, medicos):
    tk.Label(parent, text="Registro de médicos", bg="#b8d6e8", fg="#203746",
             font=("Arial", 12, "bold"), padx=8, pady=7).pack(
                 fill="x", padx=10, pady=(10, 0)
             )
    panel = tk.LabelFrame(parent, padx=10, pady=10)
    panel.pack(fill="x", padx=10, pady=10)
    etiquetas = ("Identificación", "Nombre", "Especialidad", "Tipo", "Sueldo mensual")
    entradas = []
    for fila, texto in enumerate(etiquetas):
        tk.Label(panel, text=texto).grid(row=fila, column=0, sticky="e", padx=5, pady=3)
        entrada = tk.Entry(panel)
        entrada.grid(row=fila, column=1, sticky="ew", padx=5, pady=3)
        entradas.append(entrada)
    panel.columnconfigure(1, weight=1)

    columnas = ("id", "nombre", "especialidad", "tipo", "sueldo", "anual")
    tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=7)
    for col, titulo in zip(columnas, ("ID", "Nombre", "Especialidad", "Tipo", "Sueldo mensual", "Sueldo anual")):
        tabla.heading(col, text=titulo)
        tabla.column(col, width=125, anchor="center")
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def guardar():
        ide, nombre, especialidad, tipo, sueldo_txt = [entrada.get().strip() for entrada in entradas]
        if not all((ide, nombre, especialidad, tipo, sueldo_txt)):
            messagebox.showwarning("Datos incompletos", "Completa todos los campos.", parent=parent)
            return
        if any(medico.id == ide for medico in medicos):
            messagebox.showerror("ID repetido", "Ya existe un médico con esa identificación.", parent=parent)
            return
        try:
            sueldo = float(sueldo_txt.replace(",", "."))
            if sueldo < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Sueldo inválido", "Escribe un monto numérico igual o mayor que cero.", parent=parent)
            return
        medico = Medico(ide, nombre, especialidad, tipo, sueldo)
        medicos.append(medico)
        tabla.insert("", "end", values=(medico.id, medico.nombres, medico.especialidad,
                                         medico.tipo, f"{medico.sueldo:.2f}", f"{medico.calcular_sueldo_anual():.2f}"))
        for entrada in entradas:
            entrada.delete(0, tk.END)

    tk.Button(panel, text="Guardar médico", command=guardar).grid(row=len(etiquetas), column=0, columnspan=2, pady=8)
