import os
import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from config_manager import ConfigManager

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación de Escritorio - Gestión de Archivos")
        self.geometry("500x400")

        self.config_data = ConfigManager.cargar_configuracion()
        self._crear_menu()
        self._crear_interfaz_principal()
        self.aplicar_estilos()

    def _crear_menu(self):
        menubar = tk.Menu(self)

        menu_archivo = tk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Nuevo (Simulado)", command=self.simular)
        menu_archivo.add_command(label="Abrir (Simulado)", command=self.simular)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)

        menu_edicion = tk.Menu(menubar, tearoff=0)
        menu_edicion.add_command(label="Deshacer (Simulado)", command=self.simular)
        menu_edicion.add_command(label="Rehacer (Simulado)", command=self.simular)
        menubar.add_cascade(label="Edición", menu=menu_edicion)

        menu_ver = tk.Menu(menubar, tearoff=0)
        menu_ver.add_command(label="Zoom (Simulado)", command=self.simular)
        menubar.add_cascade(label="Ver", menu=menu_ver)

        menu_settings = tk.Menu(menubar, tearoff=0)
        menu_settings.add_command(label="Configuración", command=self.abrir_ventana_settings)
        menubar.add_cascade(label="Settings", menu=menu_settings)

        self.config(menu=menubar)

    def _crear_interfaz_principal(self):
        self.frame_contenido = tk.Frame(self)
        self.frame_contenido.pack(fill="both", expand=True, padx=20, pady=20)

        self.lbl_bienvenida = tk.Label(self.frame_contenido)
        self.lbl_bienvenida.pack(pady=10)

        self.lbl_info = tk.Label(self.frame_contenido)
        self.lbl_info.pack(pady=10)

        self.lbl_foto = tk.Label(self.frame_contenido)
        self.lbl_foto.pack(pady=10)

    def aplicar_estilos(self):
        color_barra = self.config_data.get("color_barra", "#0055A5")
        color_letra = self.config_data.get("color_letra", "#000000")
        tamano = self.config_data.get("tamano_fuente", 12)

        self.config(bg=color_barra)
        self.frame_contenido.config(bg=color_barra)

        self.lbl_bienvenida.config(
            text=f"¡Bienvenido, {self.config_data['nombre_usuario']}!",
            fg=color_letra, bg=color_barra, font=("Arial", tamano, "bold")
        )
        self.lbl_info.config(
            text=f"Idioma: {self.config_data['idioma']} | Tema: {self.config_data['tema']}",
            fg=color_letra, bg=color_barra, font=("Arial", tamano)
        )
        foto = self.config_data.get("foto_perfil", "")
        texto_foto = f"Foto: {os.path.basename(foto)}" if foto and os.path.exists(foto) else "[ Sin foto ]"
        self.lbl_foto.config(text=texto_foto, fg=color_letra, bg=color_barra, font=("Arial", tamano))

    def simular(self):
        messagebox.showinfo("Simulación", "Esta es una opción simulada del menú.")

    def abrir_ventana_settings(self):
        VentanaSettings(self)


class VentanaSettings(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Settings")
        self.geometry("400x450")
        self.data = parent.config_data.copy()

        pad = {'padx': 10, 'pady': 5}

        tk.Label(self, text="Nombre:").grid(row=0, column=0, sticky="w", **pad)
        self.ent_usuario = tk.Entry(self, width=25)
        self.ent_usuario.insert(0, self.data.get("nombre_usuario", ""))
        self.ent_usuario.grid(row=0, column=1, **pad)

        tk.Label(self, text="Tema:").grid(row=1, column=0, sticky="w", **pad)
        self.cmb_tema = ttk.Combobox(self, values=["Claro", "Oscuro"], state="readonly")
        self.cmb_tema.set(self.data.get("tema", "Claro"))
        self.cmb_tema.grid(row=1, column=1, **pad)

        tk.Label(self, text="Idioma:").grid(row=2, column=0, sticky="w", **pad)
        self.cmb_idioma = ttk.Combobox(self, values=["es-ES", "en-US"], state="readonly")
        self.cmb_idioma.set(self.data.get("idioma", "es-ES"))
        self.cmb_idioma.grid(row=2, column=1, **pad)

        tk.Label(self, text="Tamaño fuente:").grid(row=3, column=0, sticky="w", **pad)
        self.spn_fuente = tk.Spinbox(self, from_=8, to=32, width=23)
        self.spn_fuente.delete(0, "end")
        self.spn_fuente.insert(0, self.data.get("tamano_fuente", 12))
        self.spn_fuente.grid(row=3, column=1, **pad)

        tk.Button(self, text="Color de Fondo", command=self._elegir_color_barra).grid(row=4, column=0, columnspan=2, **pad)
        tk.Button(self, text="Color de Letra", command=self._elegir_color_letra).grid(row=5, column=0, columnspan=2, **pad)
        tk.Button(self, text="Seleccionar Foto", command=self._elegir_foto).grid(row=6, column=0, columnspan=2, **pad)

        tk.Button(self, text="Guardar", bg="#4CAF50", fg="white", command=self._guardar).grid(row=7, column=0, columnspan=2, pady=15)

    def _elegir_color_barra(self):
        color = colorchooser.askcolor(title="Color de Fondo")
        if color[1]:
            self.data["color_barra"] = color[1]

    def _elegir_color_letra(self):
        color = colorchooser.askcolor(title="Color de Letra")
        if color[1]:
            self.data["color_letra"] = color[1]

    def _elegir_foto(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if ruta:
            self.data["foto_perfil"] = ruta

    def _guardar(self):
        try:
            self.data["tamano_fuente"] = int(self.spn_fuente.get())
        except ValueError:
            messagebox.showerror("Error", "El tamaño de fuente debe ser numérico.")
            return

        self.data["nombre_usuario"] = self.ent_usuario.get()
        self.data["tema"] = self.cmb_tema.get()
        self.data["idioma"] = self.cmb_idioma.get()

        éxito, mensaje = ConfigManager.guardar_configuracion(self.data)
        if éxito:
            self.parent.config_data = self.data
            self.parent.aplicar_estilos()
            messagebox.showinfo("Éxito", mensaje)
            self.destroy()
        else:
            messagebox.showerror("Error", mensaje)

if __name__ == "__main__":
    app = App()
    app.mainloop()