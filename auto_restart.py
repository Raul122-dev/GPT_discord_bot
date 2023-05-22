import hupper
import sys
import os

def main():
    # Reemplaza 'my_script.py' con el nombre de tu script
    script_name = 'my_bot.py'

    # Configura el monitoreo de archivos
    reloader = hupper.start_reloader('auto_restart.main')

    # Monitorea el script
    reloader.watch_files([script_name])

    # Importa y ejecuta tu script
    script_module = __import__(os.path.splitext(script_name)[0])
    script_module.main()

if __name__ == '__main__':
    main()
