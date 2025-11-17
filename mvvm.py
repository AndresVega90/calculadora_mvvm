import tkinter as tk
from tkinter import ttk

# ===========================================
#  MODELO
# ===========================================

class CalculadoraModelo:
    """ Contiene la logica de negrocio: operaciones matematicas. """

    def sumar(self, a:float, b:float)->float:
        return a + b

    def restar(self, a:float, b:float)->float:
        return a - b
    
# ===========================================
#  VIEWMODEL
# ===========================================

class CalculadoraViewModel:
    def __init__(self, modelo: CalculadoraModelo):
        self.modelo = modelo
        self.estado = {
            "valor_a": 0.0,
            "valor_b": 0.0,
            "resultado": 0.0,
        }

        # Funciones que se llamaran  al cambiar de estado
        self.suscriptores = []

    def suscribir(self, callback):
        """ Registra una funcion que se llamara cuando cambie el estado """
        self.suscriptores.append(callback)

    def _notificar(self):
        """ Notifica a todas las vistas suscritas """
        for funcion in self.suscriptores:
            funcion(self.estado)

    # Metodos internos para actualizar estado
    def _actualizar_valor(self, clave:str, texto:str):
        """
        Conveirte el texto a float
        Si el usuario escribe algo invalido, se tomoa como 0.0
        """

        try:
            valor = float(texto)
        except:
            valor = 0.0

        if clave not in self.estado:
            raise ValueError("la clave no existe") 
        self.estado[clave] = float(texto)

    # Entradas del usuario desde la vista
    def set_valor_a(self, a:str)-> None:
        self._actualizar_valor(clave="valor_a", texto=a)
        self._notificar()

    def set_valor_b(self, b:str)-> None:
        self._actualizar_valor(clave="valor_b", texto=b)
        self._notificar()


    # Acciones
    def sumar(self):
        a = self.estado["valor_a"]
        b = self.estado["valor_b"]
        resultado = self.modelo.sumar(a,b)
        self.estado["resultado"] = resultado
        self._notificar()
    
    def restar(self):
        a = self.estado["valor_a"]
        b = self.estado["valor_b"]
        resultado = self.modelo.restar(a,b)
        self.estado["resultado"] = resultado
        self._notificar()

    def reset(self):
        self.estado["valor_a"] = 0.0
        self.estado["valor_b"] = 0.0
        self.estado["resultado"] = 0.0
        self._notificar()


# ===========================================
#  VISTA CON TKINTER
# ===========================================

class CalculadoraVista(tk.Tk):
    """
    Ventana principal.
    Se suscribe al view_model y se renderiza cuando el estado cambia
    """

    def __init__(self, viewmodel: CalculadoraViewModel):
        super().__init__()

        self.viewmodel = viewmodel
        self.title("Calculadora MVVM (Tkinter)")

        # variables Tkinter
        self.variable_a = None
        self.variable_b = None
        self.variable_resultado = None

        # construir la interfaz
        self._construir_widgets()

        # suscribir vista al viewmodel
        self.viewmodel.suscribir(self.render)

        # render incial
        self.render(self.viewmodel.estado)

    def _construir_widgets(self):
        padding = {"padx": 8, "pady":8}

        # Campo valor A
        ttk.Label(self, text="Valor A").grid(row=0, column=0, sticky="e", **padding)
        self.entry_a = ttk.Entry(self)
        self.entry_a.grid(row=0,column=1, **padding)
        self.entry_a.valor_por_defecto = 0.0 #valor por defecto

        self.entry_a.bind("<FocusIn>", self._seleccionar_todo)
        self.entry_a.bind(
            "<FocusOut>",
            lambda event: self.viewmodel.set_valor_a(self.entry_a.get())
        )
        self.entry_a.bind(
            "<Return>",
            lambda event: self.viewmodel.set_valor_a(self.entry_a.get())
        )
        self.entry_a.bind(
            "<Button-3>",
            lambda event: self.viewmodel.set_valor_a(str(self.entry_a.valor_por_defecto)) #valor por defecto
        )

        # Campo valor B
        ttk.Label(self, text="Valor B").grid(row=1, column=0, sticky="e", **padding)
        self.entry_b = ttk.Entry(self)
        self.entry_b.grid(row=1,column=1, **padding)
        self.entry_b.valor_por_defecto = float(0) #valor por defecto

        self.entry_b.bind("<FocusIn>", self._seleccionar_todo)
        self.entry_b.bind(
            "<FocusOut>",
            lambda event: self.viewmodel.set_valor_b(self.entry_b.get())
        )
        self.entry_b.bind(
            "<Return>",
            lambda event: self.viewmodel.set_valor_b(self.entry_b.get())
        )
        self.entry_b.bind(
            "<Button-3>",
            lambda event: self.viewmodel.set_valor_b(str(self.entry_b.valor_por_defecto)) #valor por defecto
        )


        # Resultado solo lectura
        ttk.Label(self,text="Resultado").grid(row=2, column=0, sticky="e", **padding)
        self.entry_resultado = ttk.Entry(self, state="readonly")
        self.entry_resultado.grid(row=2, column=1, **padding)

        # Botones
        frame_botones = ttk.Frame(self)
        frame_botones.grid(row=3, column=0, columnspan=2, **padding)

        btn_sumar = ttk.Button(frame_botones, text="Sumar", command=self.viewmodel.sumar, underline=0)
        btn_sumar.grid(row=0, column=0, padx=5)

        btn_restar = ttk.Button(frame_botones, text="Restar", command=self.viewmodel.restar, underline=0)
        btn_restar.grid(row=0, column=1, padx=5)

        btn_reset = ttk.Button(frame_botones, text="Reset", command=self.viewmodel.reset, underline=1)
        btn_reset.grid(row=0, column=2, padx=5)

        self.bind_all("<Alt-s>", lambda event : btn_sumar.invoke())
        self.bind_all("<Alt-S>", lambda event : btn_sumar.invoke())

        self.bind_all("<Alt-r>", lambda event : btn_restar.invoke())
        self.bind_all("<Alt-R>", lambda event : btn_restar.invoke())

        self.bind_all("<Alt-e>", lambda event : btn_reset.invoke())
        self.bind_all("<Alt-e>", lambda event : btn_reset.invoke())

        # Diccionario de botones y su índice de subrayado
        self.subrayados = {
            btn_sumar: 0,
            btn_restar: 0,
            btn_reset: 1
        }

        # Bind para cuando se presiona ALT
        self.bind_all("<KeyPress-Alt_L>", self._activar_subrayado)
        self.bind_all("<KeyPress-Alt_R>", self._activar_subrayado)

        # Bind cuando se SUELTA ALT
        self.bind_all("<KeyRelease-Alt_L>", self._desactivar_subrayado)
        self.bind_all("<KeyRelease-Alt_R>", self._desactivar_subrayado)


    def _activar_subrayado(self, event):
        """Activa el underline en todos los botones."""
        for boton, indice in self.subrayados.items():
            boton.configure(underline=indice)

    def _desactivar_subrayado(self, event):
        """Desactiva el underline en todos los botones."""
        for boton in self.subrayados:
            boton.configure(underline=-1)  # Quita el subrayado


    def _seleccionar_todo(self, event):
        widget = event.widget
        widget.select_range(0, tk.END)
        widget.icursor(tk.END)
        return "break"
    
    def render(self, estado:dict):
        """
        Esta funcion se llama cada vez que cambia el estado en el ViewModel.
        Actuliza los StringVar que ve el usuario
        """

        self.entry_resultado.configure(state="normal")

        # Actualizar el valor A
        self.entry_a.delete(0, tk.END)
        self.entry_a.insert(0, str(estado["valor_a"]))

        # Actualizar el valor B
        self.entry_b.delete(0, tk.END)
        self.entry_b.insert(0, str(estado["valor_b"]))

        # Actualizar el valor A
        self.entry_resultado.delete(0, tk.END)
        self.entry_resultado.insert(0, str(estado["resultado"]))
        self.entry_resultado.configure(state="readonly")


def main():
    modelo = CalculadoraModelo()
    viewmodel = CalculadoraViewModel(modelo=modelo)
    app = CalculadoraVista(viewmodel=viewmodel)
    app.mainloop()

if __name__ == "__main__":
    main()