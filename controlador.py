# Se importa la clase Tk para crear la ventana principal.
from tkinter import Tk

# Se importa el modulo Vista.
import vista

# Condición que verifica si el script se está ejecutando como el programa principal.
if __name__ == "__main__":
    # Crea una instancia de la clase Tk, que representa la ventana principal de la aplicación.
    root = Tk()
    # Llama a la función vista_principal del módulo vista con el argumento root referenciando la ventana principal.
    vista.vista_principal(root)

    # Inicia el bucle principal
    root.mainloop()
