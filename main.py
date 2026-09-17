import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from config_manager import ConfigManager


class AppConfiguracion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.config_data = ConfigManager.cargar_configuracion()

        self.title("Sistema de Gestión de Configuración")
        self.geometry("700x520")
        self.minsize(600, 450)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.var_nombre = tk.StringVar(value=self.config_data.get("nombre_usuario", ""))
        self.var_fuente = tk.IntVar(value=self.config_data.get("tamano_fuente", 12))
        self.var_color_barra = tk.StringVar(value=self.config_data.get("color_barra", "#0055A5"))
        self.var_color_letra = tk.StringVar(value=self.config_data.get("color_letra", "#FFFFFF"))

        self.crear_menu()

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.mostrar_menu_principal()
        self.aplicar_estilos_dinamicos()

    def crear_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        menu_settings = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=menu_settings)
        menu_settings.add_command(label="Configuración", command=self.mostrar_ventana_configuracion)
        menu_settings.add_separator()
        menu_settings.add_command(label="Salir", command=self.quit)

    def aplicar_estilos_dinamicos(self):
        color_barra = self.var_color_barra.get()
        color_letra = self.var_color_letra.get()
        tamano_fuente = self.var_fuente.get()

        self.style.configure("Header.TFrame", background=color_barra)
        self.style.configure("Header.TLabel", background=color_barra, foreground=color_letra,
                             font=("Helvetica", max(tamano_fuente + 4, 14), "bold"))
        self.style.configure("SubHeader.TLabel", background=color_barra, foreground=color_letra,
                             font=("Helvetica", tamano_fuente))

        self.style.configure("MainBody.TLabel", font=("Helvetica", tamano_fuente))
        self.style.configure("MainBody.TButton", font=("Helvetica", tamano_fuente), padding=6)

    def limpiar_contenedor(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def mostrar_menu_principal(self):
        self.limpiar_contenedor()

        header_frame = ttk.Frame(self.container, style="Header.TFrame", padding=20)
        header_frame.pack(fill="x", side="top")

        lbl_titulo = ttk.Label(header_frame, text="Panel Principal de Administración", style="Header.TLabel")
        lbl_titulo.pack(anchor="w")

        usuario_actual = self.var_nombre.get() if self.var_nombre.get() else "Sin usuario"
        lbl_sub = ttk.Label(header_frame, text=f"Bienvenido/a, {usuario_actual}", style="SubHeader.TLabel")
        lbl_sub.pack(anchor="w", pady=(5, 0))

        # Cuerpo principal
        body_frame = ttk.Frame(self.container, padding=30)
        body_frame.pack(fill="both", expand=True)

        lbl_info = ttk.Label(body_frame,
                             text="Selecciona 'Settings > Configuración' en el menú para personalizar la interfaz.",
                             style="MainBody.TLabel")
        lbl_info.pack(pady=20)

        btn_config = ttk.Button(body_frame, text="Abrir Configuración", style="MainBody.TButton",
                                command=self.mostrar_ventana_configuracion)
        btn_config.pack(pady=10)

    def mostrar_ventana_configuracion(self):
        win_config = tk.Toplevel(self)
        win_config.title("Ajustes de Configuración")
        win_config.grab_set()

        style_modal = ttk.Style(win_config)
        style_modal.configure("Modal.TLabel", font=("Helvetica", 10))
        style_modal.configure("ModalTitle.TLabel", font=("Helvetica", 12, "bold"))
        style_modal.configure("Modal.TButton", font=("Helvetica", 10), padding=4)

        padding_frame = ttk.Frame(win_config, padding=20)
        padding_frame.pack(fill="both", expand=True)

        ttk.Label(padding_frame, text="Configuración del Sistema", style="ModalTitle.TLabel").grid(row=0, column=0,
                                                                                                   columnspan=2,
                                                                                                   pady=(0, 15),
                                                                                                   sticky="w")

        ttk.Label(padding_frame, text="Nombre de usuario:", style="Modal.TLabel").grid(row=1, column=0, sticky="w",
                                                                                       pady=8, padx=(0, 10))
        ent_nombre = ttk.Entry(padding_frame, textvariable=self.var_nombre, width=25, font=("Helvetica", 10))
        ent_nombre.grid(row=1, column=1, sticky="e", pady=8)

        ttk.Label(padding_frame, text="Tamaño de fuente (Vista Principal):", style="Modal.TLabel").grid(row=2, column=0,
                                                                                                        sticky="w",
                                                                                                        pady=8,
                                                                                                        padx=(0, 10))
        spn_fuente = ttk.Spinbox(padding_frame, from_=10, to=22, textvariable=self.var_fuente, width=23,
                                 font=("Helvetica", 10))
        spn_fuente.grid(row=2, column=1, sticky="e", pady=8)

        ttk.Label(padding_frame, text="Color de Barra / Encabezado:", style="Modal.TLabel").grid(row=3, column=0,
                                                                                                 sticky="w", pady=8,
                                                                                                 padx=(0, 10))
        btn_color_barra = tk.Button(padding_frame, text="  Elegir Color  ", bg=self.var_color_barra.get(),
                                    command=lambda: self.seleccionar_color(self.var_color_barra, btn_color_barra))
        btn_color_barra.grid(row=3, column=1, sticky="ew", pady=8)

        ttk.Label(padding_frame, text="Color de Letra del Encabezado:", style="Modal.TLabel").grid(row=4, column=0,
                                                                                                   sticky="w", pady=8,
                                                                                                   padx=(0, 10))
        btn_color_letra = tk.Button(padding_frame, text="  Elegir Color  ", bg=self.var_color_letra.get(),
                                    command=lambda: self.seleccionar_color(self.var_color_letra, btn_color_letra))
        btn_color_letra.grid(row=4, column=1, sticky="ew", pady=8)

        frame_btn = ttk.Frame(padding_frame)
        frame_btn.grid(row=5, column=0, columnspan=2, pady=(20, 0), sticky="e")

        btn_guardar = ttk.Button(frame_btn, text="Guardar y Aplicar", style="Modal.TButton",
                                 command=lambda: self.guardar_y_aplicar(win_config))
        btn_guardar.pack(side="right", padx=5)

        btn_cancelar = ttk.Button(frame_btn, text="Cancelar", style="Modal.TButton", command=win_config.destroy)
        btn_cancelar.pack(side="right", padx=5)

        win_config.update_idletasks()
        win_config.geometry(f"{win_config.winfo_reqwidth() + 40}x{win_config.winfo_reqheight() + 20}")
        win_config.resizable(False, False)

    def seleccionar_color(self, var_target, btn_target):
        color = colorchooser.askcolor(initialcolor=var_target.get(), title="Selecciona un color")[1]
        if color:
            var_target.set(color)
            btn_target.config(bg=color)

    def guardar_y_aplicar(self, ventana_modal):
        self.config_data["nombre_usuario"] = self.var_nombre.get()
        self.config_data["tamano_fuente"] = self.var_fuente.get()
        self.config_data["color_barra"] = self.var_color_barra.get()
        self.config_data["color_letra"] = self.var_color_letra.get()

        exito, mensaje = ConfigManager.guardar_configuracion(self.config_data)

        if exito:
            self.aplicar_estilos_dinamicos()
            self.mostrar_menu_principal()
            messagebox.showinfo("Éxito", "Configuración guardada y aplicada correctamente.", parent=ventana_modal)
            ventana_modal.destroy()
        else:
            messagebox.showerror("Error", f"No se pudo guardar la configuración: {mensaje}", parent=ventana_modal)


if __name__ == "__main__":
    app = AppConfiguracion()
    app.mainloop()