import json
import os
import shutil

CONFIG_FILE = "config.json"
BACKUP_FILE = "config.bak"
TEMP_FILE = "config.tmp"

DEFAULT_CONFIG = {
    "nombre_usuario": "Usuario_Default",
    "tema": "Claro",
    "idioma": "es-ES",
    "tamano_fuente": 12,
    "color_barra": "#0055A5",
    "color_letra": "#000000",
    "foto_perfil": ""
}

class ConfigManager:
    @staticmethod
    def cargar_configuracion():
        """Carga la configuración manejando archivo ausente, corrupto o sin permisos."""
        if not os.path.exists(CONFIG_FILE):
            print("[INFO] Archivo ausente. Cargando valores por defecto.")
            return DEFAULT_CONFIG.copy()
        
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                for key, value in DEFAULT_CONFIG.items():
                    config.setdefault(key, value)
                return config
        except (json.JSONDecodeError, ValueError):
            print("[ERROR] Archivo corrupto. Intentando recuperar desde .bak...")
            return ConfigManager._recuperar_bak()
        except PermissionError:
            print("[ERROR] Sin permisos de lectura. Usando valores por defecto.")
            return DEFAULT_CONFIG.copy()
        except Exception:
            return DEFAULT_CONFIG.copy()

    @staticmethod
    def _recuperar_bak():
        """Recupera la configuración desde el archivo de respaldo .bak si existe."""
        if os.path.exists(BACKUP_FILE):
            try:
                with open(BACKUP_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return DEFAULT_CONFIG.copy()

    @staticmethod
    def guardar_configuracion(config_data):
        """Escritura segura mediante archivo temporal (.tmp) y copia de respaldo (.bak)."""
        if os.path.exists(CONFIG_FILE):
            try:
                shutil.copy2(CONFIG_FILE, BACKUP_FILE)
            except Exception as e:
                print(f"[ADVERTENCIA] No se creó el backup: {e}")

        try:
            with open(TEMP_FILE, "w", encoding="utf-8") as f:
                json.dump(config_data, f, ensure_ascii=False, indent=4)
            
            os.replace(TEMP_FILE, CONFIG_FILE)
            return True, "Configuración guardada exitosamente."
        except PermissionError:
            if os.path.exists(TEMP_FILE):
                os.remove(TEMP_FILE)
            return False, "Error de permisos al escribir el archivo."
        except Exception as e:
            if os.path.exists(TEMP_FILE):
                os.remove(TEMP_FILE)
            return False, f"Error al guardar: {str(e)}"