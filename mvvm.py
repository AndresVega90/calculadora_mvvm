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
        self.variable_a = tk.StringVar()
        self.variable_b = tk.StringVar()
        self.variable_resultado = tk.StringVar()

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
        entry_a = ttk.Entry(self, textvariable=self.variable_a)
        entry_a.grid(row=0,column=1, **padding)

        entry_a.bind(
            "<KeyRelease>",
            lambda event: self.viewmodel.set_valor_a(self.variable_a.get())
        )

        # Campo valor B
        ttk.Label(self, text="Valor B").grid(row=1, column=0, sticky="e", **padding)
        entry_b = ttk.Entry(self, textvariable=self.variable_b)
        entry_b.grid(row=1,column=1, **padding)

        entry_b.bind(
            "<KeyRelease>",
            lambda event: self.viewmodel.set_valor_b(self.variable_b.get())
        )

        # Resultado solo lectura
        ttk.Label(self,text="Resultado").grid(row=2, column=0, sticky="e", **padding)
        entry_resultado = ttk.Entry(self, textvariable=self.variable_resultado, state="readonly")
        entry_resultado.grid(row=2, column=1, **padding)

        # Botones
        frame_botones = ttk.Frame(self)
        frame_botones.grid(row=3, column=0, columnspan=2, **padding)

        btn_sumar = ttk.Button(frame_botones, text="Sumar", command=self.viewmodel.sumar)
        btn_sumar.grid(row=0, column=0, padx=5)

        btn_restar = ttk.Button(frame_botones, text="Restar", command=self.viewmodel.restar)
        btn_restar.grid(row=0, column=1, padx=5)

        btn_reset = ttk.Button(frame_botones, text="Reset", command=self.viewmodel.reset)
        btn_reset.grid(row=0, column=2, padx=5)



    
    def render(self, estado:dict):
        """
        Esta funcion se llama cada vez que cambia el estado en el ViewModel.
        Actuliza los StringVar que ve el usuario
        """

        # Convertimos los float a texto
        self.variable_a.set(str(estado["valor_a"]))
        self.variable_b.set(str(estado["valor_b"]))
        self.variable_resultado.set(str(estado["resultado"]))


def main():
    modelo = CalculadoraModelo()
    viewmodel = CalculadoraViewModel(modelo=modelo)
    app = CalculadoraVista(viewmodel=viewmodel)
    app.mainloop()

if __name__ == "__main__":
    main()