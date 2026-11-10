import tkinter as tk
from tkinter import ttk, messagebox


class Horario:
    def __init__(self, medico, hora, dia, disponible):
        self.medico = medico
        self.hora = str(hora).strip()
        self.dia = str(dia).strip()
        self.disponible = str(disponible).strip()

    def get_medico(self): return self.medico
    def set_medico(self, medico): self.medico = medico
    def get_hora(self): return self.hora
    def set_hora(self, hora): self.hora = hora
    def get_dia(self): return self.dia
    def set_dia(self, dia): self.dia = dia
    def get_disponible(self): return self.disponible
    def set_disponible(self, disponible): self.disponible = disponible


def crear_interfaz(parent, medicos, horarios):
    tk.Label(parent, text="Agenda de médicos", bg="#b8d6e8", fg="#203746",
             font=("Arial", 12, "bold"), padx=8, pady=7).pack(
                 fill="x", padx=10, pady=(10, 0)
             )
    panel = tk.LabelFrame(parent, padx=10, pady=10)
    panel.pack(fill="x", padx=10, pady=10)
    entradas = {}
    for fila, (clave, texto) in enumerate((("medico", "ID del médico"), ("hora", "Hora"), ("dia", "Día"))):
        tk.Label(panel, text=texto).grid(row=fila, column=0, sticky="e", padx=5, pady=3)
        entrada = tk.Entry(panel)
        entrada.grid(row=fila, column=1, sticky="ew", padx=5, pady=3)
        entradas[clave] = entrada

    tk.Label(panel, text="Disponibilidad").grid(row=3, column=0, sticky="e", padx=5, pady=3)
    estado = tk.StringVar(value="Sí")
    ttk.Combobox(panel, textvariable=estado, values=("Sí", "No"), state="readonly").grid(
        row=3, column=1, sticky="ew", padx=5, pady=3
    )
    panel.columnconfigure(1, weight=1)

    columnas = ("id", "medico", "dia", "hora", "disponible")
    tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=7)
    for col, titulo in zip(columnas, ("ID médico", "Médico", "Día", "Hora", "Disponible")):
        tabla.heading(col, text=titulo)
        tabla.column(col, width=125, anchor="center")
    tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def buscar_medico():
        ide = entradas["medico"].get().strip()
        return next((medico for medico in medicos if medico.id == ide), None)

    def guardar():
        medico = buscar_medico()
        hora, dia = entradas["hora"].get().strip(), entradas["dia"].get().strip()
        if medico is None:
            messagebox.showerror("Médico no encontrado", "Escribe el ID de un médico registrado.", parent=parent)
            return
        if not hora or not dia:
            messagebox.showwarning("Datos incompletos", "Escribe el día y la hora.", parent=parent)
            return
        duplicado = any(item.medico is medico and item.hora.casefold() == hora.casefold()
                        and item.dia.casefold() == dia.casefold() for item in horarios)
        if duplicado:
            messagebox.showwarning("Horario repetido", "Ya existe un registro para ese día y hora.", parent=parent)
            return
        horario = Horario(medico, hora, dia, estado.get())
        medico.agregarHorario(horario)
        horarios.append(horario)
        tabla.insert("", "end", values=(medico.id, medico.nombres, dia, hora, estado.get()))
        for entrada in entradas.values():
            entrada.delete(0, tk.END)

    def consultar():
        medico = buscar_medico()
        hora, dia = entradas["hora"].get().strip(), entradas["dia"].get().strip()
        if medico is None:
            messagebox.showerror("Médico no encontrado", "Escribe el ID de un médico registrado.", parent=parent)
            return
        if not hora or not dia:
            messagebox.showwarning("Datos incompletos", "Escribe el día y la hora que quieres consultar.", parent=parent)
            return
        disponible = medico.verificar_disponibilidad(hora, dia)
        if disponible is None:
            texto = f"No hay horario registrado para {dia} a las {hora}."
        elif disponible:
            texto = f"El médico está disponible el {dia} a las {hora}."
        else:
            texto = f"El médico no está disponible el {dia} a las {hora}."
        messagebox.showinfo("Disponibilidad", texto, parent=parent)

    botones = ttk.Frame(panel)
    botones.grid(row=4, column=0, columnspan=2, pady=8)
    tk.Button(botones, text="Guardar horario", command=guardar).pack(side="left", padx=5)
    tk.Button(botones, text="Consultar disponibilidad", command=consultar).pack(side="left", padx=5)
