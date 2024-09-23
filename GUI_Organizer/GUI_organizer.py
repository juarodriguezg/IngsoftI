import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda de Eventos")
        self.root.configure(bg="#f0f0f0")  # Cambiar el fondo de la ventana principal
        self.eventos_futuros = []
        self.eventos_pasados = []

        # Título
        self.titulo = tk.Label(self.root, text="Agenda de Eventos", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.titulo.pack(pady=10)
        
        # Frame para mostrar la lista de eventos
        self.frame_eventos = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_eventos.pack(pady=10)

        # Título para eventos futuros
        self.titulo_futuros = tk.Label(self.frame_eventos, text="Eventos Futuros", font=("Helvetica", 10, "bold"), bg="#f0f0f0")
        self.titulo_futuros.pack(pady=3)

        # Text widget para eventos futuros
        self.text_eventos_futuros = tk.Text(self.frame_eventos, height=15, width=50, bg="#ffffff", fg="#000000", font=("Helvetica", 12))
        self.text_eventos_futuros.pack(pady=5)
        self.text_eventos_futuros.config(state=tk.DISABLED)  # Hacer el Text widget de solo lectura

        # Título para eventos pasados
        self.titulo_pasados = tk.Label(self.frame_eventos, text="Eventos Pasados", font=("Helvetica", 10, "bold"), bg="#f0f0f0")
        self.titulo_pasados.pack(pady=5)

        # Text widget para eventos pasados
        self.text_eventos_pasados = tk.Text(self.frame_eventos, height=15, width=50, bg="#f0f0f0", fg="#000000", font=("Helvetica", 12))
        self.text_eventos_pasados.pack(pady=5)
        self.text_eventos_pasados.config(state=tk.DISABLED)  # Hacer el Text widget de solo lectura

        # Frame para los botones
        self.frame_botones = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_botones.pack(pady=10)

        # Botones
        self.boton_agregar = tk.Button(self.frame_botones, text="Agregar Evento", command=self.agregar_evento, bg="#4CAF50", fg="#ffffff", font=("Helvetica", 10, "bold"))
        self.boton_agregar.grid(row=0, column=0, padx=5, pady=5)

        self.boton_editar = tk.Button(self.frame_botones, text="Editar Evento", command=self.editar_evento, bg="#2196F3", fg="#ffffff", font=("Helvetica", 10, "bold"))
        self.boton_editar.grid(row=0, column=1, padx=5, pady=5)

        self.boton_eliminar = tk.Button(self.frame_botones, text="Eliminar Evento", command=self.eliminar_evento, bg="#f44336", fg="#ffffff", font=("Helvetica", 10, "bold"))
        self.boton_eliminar.grid(row=0, column=2, padx=5, pady=5)

        # Actualizar lista de eventos
        self.actualizar_lista()

    def agregar_evento_aux(self, nombre, fecha_str):
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
            if fecha > datetime.now():
                self.eventos_futuros.append({"nombre": nombre, "fecha": fecha})
            else:
                self.eventos_pasados.append({"nombre": nombre, "fecha": fecha})
            self.actualizar_lista()
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha y hora incorrecto. Use YYYY-MM-DD HH:MM")

    def editar_evento_aux(self, index, nuevo_nombre, nueva_fecha_str):
        try:
            nueva_fecha = datetime.strptime(nueva_fecha_str, "%Y-%m-%d %H:%M")
            if nueva_fecha > datetime.now():
                if index < len(self.eventos_pasados):
                    evento = self.eventos_pasados.pop(index)
                    evento['nombre'] = nuevo_nombre
                    evento['fecha'] = nueva_fecha
                    self.eventos_futuros.append(evento)
                else:
                    evento = self.eventos_futuros[index - len(self.eventos_pasados)]
                    evento['nombre'] = nuevo_nombre
                    evento['fecha'] = nueva_fecha
            else:
                if index < len(self.eventos_futuros):
                    evento = self.eventos_futuros.pop(index)
                    evento['nombre'] = nuevo_nombre
                    evento['fecha'] = nueva_fecha
                    self.eventos_pasados.append(evento)
                else:
                    evento = self.eventos_pasados[index - len(self.eventos_futuros)]
                    evento['nombre'] = nuevo_nombre
                    evento['fecha'] = nueva_fecha
            self.actualizar_lista()
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha y hora incorrecto. Use YYYY-MM-DD HH:MM")

    def eliminar_evento_aux(self, lista, index):
        del lista[index]
        self.actualizar_lista()

    def agregar_evento(self):
        ventana_agregar = tk.Toplevel(self.root)
        ventana_agregar.title("Agregar Evento")

        # Campos de entrada
        tk.Label(ventana_agregar, text="Nombre del evento").pack(pady=5)
        nombre_entry = tk.Entry(ventana_agregar)
        nombre_entry.pack(pady=5)

        tk.Label(ventana_agregar, text="Fecha y hora (YYYY-MM-DD HH:MM)").pack(pady=5)
        fecha_entry = tk.Entry(ventana_agregar)
        fecha_entry.pack(pady=5)

        def guardar_evento():
            nombre = nombre_entry.get()
            fecha_str = fecha_entry.get()
            self.agregar_evento_aux(nombre, fecha_str)
            ventana_agregar.destroy()
        tk.Button(ventana_agregar, text="Guardar", command=guardar_evento, bg="#4CAF50", fg="#ffffff", font=("Helvetica", 10, "bold")).pack(pady=10)

    def editar_evento(self):
        seleccionado_futuro = self.text_eventos_futuros.tag_ranges("sel")
        seleccionado_pasado = self.text_eventos_pasados.tag_ranges("sel")
        if seleccionado_futuro:
            lista = self.eventos_futuros
            text_widget = self.text_eventos_futuros
        elif seleccionado_pasado:
            lista = self.eventos_pasados
            text_widget = self.text_eventos_pasados
        else:
            messagebox.showwarning("Advertencia", "Seleccione un evento para editar.")
            return

        index = int(text_widget.index(seleccionado_futuro[0] if seleccionado_futuro else seleccionado_pasado[0]).split('.')[0]) - 1
        evento = lista[index]

        ventana_editar = tk.Toplevel(self.root)
        ventana_editar.title("Editar Evento")

        tk.Label(ventana_editar, text="Nombre del evento").pack(pady=5)
        nombre_entry = tk.Entry(ventana_editar)
        nombre_entry.insert(0, evento['nombre'])
        nombre_entry.pack(pady=5)

        tk.Label(ventana_editar, text="Fecha y hora (YYYY-MM-DD HH:MM)").pack(pady=5)
        fecha_entry = tk.Entry(ventana_editar)
        fecha_entry.insert(0, evento['fecha'].strftime("%Y-%m-%d %H:%M"))
        fecha_entry.pack(pady=5)

        def guardar_cambios():
            nuevo_nombre = nombre_entry.get()
            nueva_fecha_str = fecha_entry.get()
            self.editar_evento_aux(index, nuevo_nombre, nueva_fecha_str)
            ventana_editar.destroy()    

        tk.Button(ventana_editar, text="Guardar", command=guardar_cambios, bg="#4CAF50", fg="#ffffff", font=("Helvetica", 10, "bold")).pack(pady=10)

    def eliminar_evento(self):
        seleccionado_futuro = self.text_eventos_futuros.tag_ranges("sel")
        seleccionado_pasado = self.text_eventos_pasados.tag_ranges("sel")

        if seleccionado_futuro:
            lista = self.eventos_futuros
            text_widget = self.text_eventos_futuros
        elif seleccionado_pasado:
            lista = self.eventos_pasados
            text_widget = self.text_eventos_pasados
        else:
            messagebox.showwarning("Advertencia", "Seleccione un evento para eliminar.")
            return

        index = int(text_widget.index(seleccionado_futuro[0] if seleccionado_futuro else seleccionado_pasado[0]).split('.')[0]) - 1
        self.eliminar_evento_aux(lista,index)  
        

    def actualizar_lista(self):
        self.text_eventos_futuros.config(state=tk.NORMAL)  # Habilitar edición temporalmente
        self.text_eventos_futuros.delete(1.0, tk.END)
        self.text_eventos_pasados.config(state=tk.NORMAL)  # Habilitar edición temporalmente
        self.text_eventos_pasados.delete(1.0, tk.END)
        ahora = datetime.now()

        # Ordenar eventos por fecha
        self.eventos_futuros.sort(key=lambda x: x['fecha'])
        self.eventos_pasados.sort(key=lambda x: x['fecha'])

        # Mover eventos pasados de la lista de futuros a la lista de pasados
        eventos_a_mover = [evento for evento in self.eventos_futuros if evento['fecha'] < ahora]
        for evento in eventos_a_mover:
            self.eventos_futuros.remove(evento)
            self.eventos_pasados.append(evento)

        # Actualizar la lista de eventos futuros
        for i, evento in enumerate(self.eventos_futuros):
            diferencia = evento['fecha'] - ahora
            tag = f"evento_futuro_{i}"
            self.text_eventos_futuros.insert(tk.END, f"  {evento['nombre']} - {evento['fecha']} ({diferencia.days} días, {diferencia.seconds // 3600} horas restantes)\n", tag)
            self.text_eventos_futuros.tag_config(tag, background=self.get_color(i), font=("Lucida Bright", 12, "bold"), lmargin1=10, lmargin2=10)

        # Actualizar la lista de eventos pasados
        for i, evento in enumerate(self.eventos_pasados):
            diferencia = ahora - evento['fecha']
            tag = f"evento_pasado_{i}"
            self.text_eventos_pasados.insert(tk.END, f"  {evento['nombre']} - {evento['fecha']} (hace {diferencia.days} días, {diferencia.seconds // 3600} horas)\n", tag)
            self.text_eventos_pasados.tag_config(tag, background=self.get_color(i), font=("Lucida Bright", 12, "bold"), lmargin1=10, lmargin2=10)

        self.text_eventos_futuros.config(state=tk.DISABLED)  # Deshabilitar edición nuevamente
        self.text_eventos_pasados.config(state=tk.DISABLED)  # Deshabilitar edición nuevamente

    def get_color(self, index):
        # Alternar colores para cada evento
        colors = ["#FFCCCC", "#CCFFCC", "#CCCCFF", "#FFFFCC"]
        return colors[index % len(colors)]

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()