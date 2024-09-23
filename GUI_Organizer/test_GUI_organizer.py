import unittest
from datetime import datetime, timedelta
from tkinter import Tk
from GUI_organizer import AgendaApp

class TestAgendaApp(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.app = AgendaApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_agregar_evento_futuro(self):
        nombre = "Evento Futuro"
        fecha = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        self.app.agregar_evento_aux(nombre, fecha)
        self.assertEqual(len(self.app.eventos_futuros), 1)
        self.assertEqual(self.app.eventos_futuros[0]['nombre'], nombre)

    def test_agregar_evento_pasado(self):
        nombre = "Evento Pasado"
        fecha = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        self.app.agregar_evento_aux(nombre, fecha)
        self.assertEqual(len(self.app.eventos_pasados), 1)
        self.assertEqual(self.app.eventos_pasados[0]['nombre'], nombre)

    def test_editar_evento_futuro(self):
        nombre = "Evento Futuro"
        fecha = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        self.app.agregar_evento_aux(nombre, fecha)
        nuevo_nombre = "Evento Futuro Editado"
        nueva_fecha = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
        self.app.editar_evento_aux(0, nuevo_nombre, nueva_fecha)
        self.assertEqual(self.app.eventos_futuros[0]['nombre'], nuevo_nombre)
        self.assertEqual(self.app.eventos_futuros[0]['fecha'].strftime("%Y-%m-%d %H:%M"), nueva_fecha)

    def test_eliminar_evento_futuro(self):
        nombre = "Evento Futuro"
        fecha = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        self.app.agregar_evento_aux(nombre, fecha)
        self.app.eliminar_evento_aux(self.app.eventos_futuros, 0)
        self.assertEqual(len(self.app.eventos_futuros), 0)

    def test_eliminar_evento_pasado(self):
        nombre = "Evento Pasado"
        fecha = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        self.app.agregar_evento_aux(nombre, fecha)
        self.app.eliminar_evento_aux(self.app.eventos_pasados, 0)
        self.assertEqual(len(self.app.eventos_pasados), 0)

    def test_actualizar_lista(self):
        nombre_futuro = "Evento Futuro"
        fecha_futuro = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        self.app.agregar_evento_aux(nombre_futuro, fecha_futuro)
        nombre_pasado = "Evento Pasado"
        fecha_pasado = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        self.app.agregar_evento_aux(nombre_pasado, fecha_pasado)
        self.app.actualizar_lista()
        self.assertEqual(len(self.app.eventos_futuros), 1)
        self.assertEqual(len(self.app.eventos_pasados), 1)

if __name__ == '__main__':
    unittest.main()