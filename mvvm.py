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