import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from Persona1 import crear_interfaz as interfaz_persona
from Medico1 import crear_interfaz as interfaz_medico
from Paciente1 import crear_interfaz as interfaz_paciente
from Paciente1 import crear_interfaz_resumen, cargar_pacientes
from Horario1 import crear_interfaz as interfaz_horario


class AplicacionClinica:
    def __init__(self, ventana):
        self.ventana = ventana
        self.personas = []
        self.medicos = []
        try:
            self.pacientes = cargar_pacientes()
        except ValueError as error:
            self.pacientes = []
            messagebox.showerror("Error al cargar pacientes", str(error), parent=ventana)
        self.horarios = []
        self.configurar_ventana()
        self.crear_pestanas()

    def configurar_ventana(self):
        self.ventana.title("Sistema de personas y citas")
        self.ventana.geometry("1000x720")
        self.ventana.minsize(850, 600)

    def crear_pestanas(self):
        self.pasos = (
            ("Personas", lambda marco: interfaz_persona(marco, self.personas)),
            ("Médicos", lambda marco: interfaz_medico(marco, self.medicos)),
            ("Pacientes", lambda marco: interfaz_paciente(marco, self.pacientes, self.medicos)),
            ("Horarios", lambda marco: interfaz_horario(marco, self.medicos, self.horarios)),
            ("Resumen", lambda marco: crear_interfaz_resumen(marco, self.pacientes)),
        )

        self.indice_paso = 0
        zona_contenido = ttk.Frame(self.ventana)
        zona_contenido.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        self.paginas = []
        for _titulo, crear in self.pasos:
            pagina = ttk.Frame(zona_contenido)
            pagina.place(relx=0, rely=0, relwidth=1, relheight=1)
            crear(pagina)
            self.paginas.append(pagina)

        pie = ttk.Frame(self.ventana, padding=10)
        pie.pack(fill="x", padx=10, pady=(0, 8))

        self.etiqueta_paso = ttk.Label(pie, text="")
        self.etiqueta_paso.pack(side="left", padx=5)

        self.boton_anterior = tk.Button(
            pie, text="Anterior", command=self.paso_anterior, state="disabled"
        )
        self.boton_anterior.pack(side="right", padx=5)

        self.boton_siguiente = tk.Button(
            pie, text="Continuar", command=self.paso_siguiente
        )
        self.boton_siguiente.pack(side="right", padx=5)

        self.mostrar_paso()

    def mostrar_paso(self):
        self.paginas[self.indice_paso].tkraise()
        titulo = self.pasos[self.indice_paso][0]
        self.etiqueta_paso.config(
            text=f"Paso {self.indice_paso + 1} de {len(self.pasos)}: {titulo}"
        )
        self.boton_anterior.config(
            state="normal" if self.indice_paso > 0 else "disabled"
        )
        texto_boton = (
            "Finalizar" if self.indice_paso == len(self.pasos) - 1
            else "Continuar"
        )
        self.boton_siguiente.config(text=texto_boton)

    def paso_anterior(self):
        if self.indice_paso > 0:
            self.indice_paso -= 1
            self.mostrar_paso()

    def paso_siguiente(self):
        if self.indice_paso < len(self.pasos) - 1:
            self.indice_paso += 1
            self.mostrar_paso()
        else:
            self.ventana.destroy()


def iniciar():
    ventana = tk.Tk()
    AplicacionClinica(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    iniciar()
