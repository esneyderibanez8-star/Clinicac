import tkinter as tk
from tkinter import ttk, messagebox


class Persona:
    def __init__(self, ide, nombres, anio="", mes="", dia="",
                 genero="", direccion="", codigo_postal=""):
        self.id = str(ide)
        self.nombres = nombres
        self.anio = anio
        self.mes = mes
        self.dia = dia
        self.genero = genero
        self.direccion = direccion
        self.codigo_postal = codigo_postal

    def get_id(self): return self.id
    def set_id(self, ide): self.id = str(ide)
    def get_nombres(self): return self.nombres
    def set_nombres(self, nombres): self.nombres = nombres
    def get_anio(self): return self.anio
    def set_anio(self, anio): self.anio = anio
    def get_mes(self): return self.mes
    def set_mes(self, mes): self.mes = mes
    def get_dia(self): return self.dia
    def set_dia(self, dia): self.dia = dia
    def get_genero(self): return self.genero
    def set_genero(self, genero): self.genero = genero
    def get_direccion(self): return self.direccion
    def set_direccion(self, direccion): self.direccion = direccion
    def get_codigo_postal(self): return self.codigo_postal
    def set_codigo_postal(self, codigo_postal): self.codigo_postal = codigo_postal


def crear_interfaz(parent, personas):
    tk.Label(parent, text="Registro de personas", bg="#b8d6e8", fg="#203746",
             font=("Arial", 12, "bold"), padx=8, pady=7).pack(
                 fill="x", padx=10, pady=(10, 0)
             )
    panel = tk.LabelFrame(parent, padx=10, pady=10)
    panel.pack(fill="x", padx=10, pady=10)
    etiquetas = ("Identificación", "Nombre", "Año de nacimiento", "Mes de nacimiento",
                 "Día de nacimiento", "Género", "Dirección", "Código postal")
    entradas = []
    for fila, texto in enumerate(etiquetas):
        tk.Label(panel, text=texto).grid(row=fila, column=0, sticky="e", padx=5, pady=3)
        entrada = tk.Entry(panel)
        entrada.grid(row=fila, column=1, sticky="ew", padx=5, pady=3)
        entradas.append(entrada)
    panel.columnconfigure(1, weight=1)

    columnas = ("id", "nombre", "anio", "mes", "dia", "genero", "direccion", "codigo")
    tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=7)
    for col, titulo in zip(columnas, ("ID", "Nombre", "Año", "Mes", "Día", "Género", "Dirección", "Código postal")):
        tabla.heading(col, text=titulo)
        tabla.column(col, width=110, anchor="center")
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def guardar():
        datos = [entrada.get().strip() for entrada in entradas]
        if not all(datos):
            messagebox.showwarning("Datos incompletos", "Completa todos los campos.", parent=parent)
            return
        if any(persona.id == datos[0] for persona in personas):
            messagebox.showerror("ID repetido", "Ya existe una persona con esa identificación.", parent=parent)
            return
        try:
            anio, mes, dia = map(int, datos[2:5])
        except ValueError:
            messagebox.showerror("Fecha inválida", "Año, mes y día deben ser números.", parent=parent)
            return
        if not 1 <= mes <= 12 or not 1 <= dia <= 31:
            messagebox.showerror("Fecha inválida", "El mes debe estar entre 1 y 12 y el día entre 1 y 31.", parent=parent)
            return

        persona = Persona(datos[0], datos[1], anio, mes, dia, datos[5], datos[6], datos[7])
        personas.append(persona)
        tabla.insert("", "end", values=(persona.id, persona.nombres, anio, mes, dia,
                                         persona.genero, persona.direccion, persona.codigo_postal))
        for entrada in entradas:
            entrada.delete(0, tk.END)

    tk.Button(panel, text="Guardar persona", command=guardar).grid(row=len(etiquetas), column=0, columnspan=2, pady=8)
