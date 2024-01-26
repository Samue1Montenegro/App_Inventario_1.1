# Se importa ttk para crear widgets.
from tkinter import ttk

# Asigna el modulo tkinter a tk para facilitar su uso.
import tkinter as tk

# Se importa la clase Label para mostrar texto o imágenes en una ventana de la interfaz.
from tkinter import Label

# Se importa la clase Entry para crear campos de entrada de texto.
from tkinter import Entry

# Se importa la clase Scrollbar para agregar barra de desplazamiento en el Treeview.
from tkinter import Scrollbar

# Se importa la clase Button para crear botones en una interfaz.
from tkinter import Button

# Se importan funciones desde el modulo modelo para ser utilizadas.
from modelo import actualizar_treeview
from modelo import alta
from modelo import modificar_seleccionado
from modelo import realizar_consulta
from modelo import borrar


# ----------------------------------------------------------------------------------
# ######################       VISTA                ########################
# ----------------------------------------------------------------------------------
# Se crea una funcion para almacenar la creacion de la ventana completa, para exportarla al modulo controlador.
def vista_principal(root):
    # Se crea un titulo para la ventana.
    root.title("Inventario")

    # Titulo general de la aplicacion.
    titulo = Label(
        root,
        text="INGRESE SUS PRODUCTOS",
        bg="#00758f",
        fg="white",
        height=3,
        width=60,
    )
    titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky="w" + "e")

    # Titulos que indican en la entrada de datos en productos y configuracion de posicion.
    producto = Label(root, text="PRODUCTO")
    producto.grid(row=1, column=0, sticky="w")

    # Titulos que indican en la entrada de datos en cantidad y configuracion de posicion.
    cantidad = Label(root, text="CANTIDAD")
    cantidad.grid(row=2, column=0, sticky="w")

    # Titulos que indican en la entrada de datos en codigo del producto y configuracion de posicion.
    id_prod = Label(root, text="CODIGO")
    id_prod.grid(row=3, column=0, sticky="w")

    # Titulos que indican en la entrada de datos en consulta y configuracion de posicion.
    consulta_label = Label(root, text="CONSULTA DEL PRODUCTO")
    consulta_label.grid(row=4, column=0, sticky="w")

    # Se definen variables para tomar valores de campos de entrada.
    producto_val = tk.StringVar()
    consulta_val = tk.StringVar()
    cantidad_val = tk.IntVar()
    codigo_val = tk.IntVar()

    w_ancho = 40

    # Se definen variables globales a las variables que contengan entry para luego ser utilizadas por funciones.
    global entrada_producto, entrada_cantidad, entrada_codigo, consulta_entry

    # Formulario para Campo de entrada de producto.
    entrada_producto = Entry(root, textvariable=producto_val, width=w_ancho)
    entrada_producto.grid(row=1, column=1)

    # Formulario para Campo de entrada en cantidad del producto.
    entrada_cantidad = Entry(root, textvariable=cantidad_val, width=w_ancho)
    entrada_cantidad.grid(row=2, column=1)

    # Formularios para Campo de entrada del codigo del producto.
    entrada_codigo = Entry(root, textvariable=codigo_val, width=w_ancho)
    entrada_codigo.grid(row=3, column=1)

    # Formulario para Campo de consulta de producto
    consulta_entry = Entry(root, textvariable=consulta_val, width=w_ancho)
    consulta_entry.grid(row=4, column=1)

    # ----------------------------------------------------------------------------------
    # ######################          TREEVIEW             ######################
    # ----------------------------------------------------------------------------------
    # Crea el treeview para mostrar el inventario en la ventana
    global tree

    # Se le pasa como parametro al treeview la variable root, las columnas que contiene....
    # .... y el argumento show para indicarle que solo muestre las columnas deseadas
    tree = ttk.Treeview(root, columns=("ID", "Producto", "Cantidad"), show="headings")

    # Columnas para Producto, codigo y cantidad
    tree["columns"] = ("ID", "Producto", "Cantidad")
    tree.column("ID", width=100, minwidth=50, anchor="center")
    tree.column("Producto", width=300, minwidth=80, anchor="center")
    tree.column("Cantidad", width=300, minwidth=80, anchor="center")

    # Nombre de columnas
    tree.heading("ID", text="CODIGO")
    tree.heading("Producto", text="PRODUCTO")
    tree.heading("Cantidad", text="CANTIDAD")
    tree.grid(row=10, column=0, columnspan=4)

    # Crea la barra de deslizamiento vertical.
    tree_scrollbar = Scrollbar(root, command=tree.yview)
    tree.configure(yscrollcommand=tree_scrollbar.set)
    tree_scrollbar.grid(row=10, column=4, sticky="ns")

    # Crea una barra de separacion
    separador = ttk.Separator(
        root,
        orient="horizontal",
    )
    separador.grid(row=6, pady=4)
    # Se llama a la funcion actualizar_treeview para que introduzca los elementos de la base de datos en cuanto se abra la aplicacion.
    actualizar_treeview(tree)

    # Boton para dar de alta un producto y sus configuraciones.
    global boton_alta
    boton_alta = Button(
        root,
        text="Agregar",
        width=10,
        activeforeground="green",
        command=lambda: alta(
            codigo_val,
            producto_val,
            cantidad_val,
            tree,
        ),
    )
    boton_alta.grid(row=1, column=2)

    # Boton para borrar un producto y sus configuraciones.
    global boton_borrar
    boton_borrar = Button(
        root,
        text="Borrar",
        width=10,
        activeforeground="red",
        command=lambda: borrar(codigo_val, tree),
    )
    boton_borrar.grid(row=2, column=2, pady=(1, 0))

    # Se crea el botón Modificar Producto para modificar el elemento seleccionado  y las configuraciones del boton.
    global modificar_boton
    modificar_boton = Button(
        root,
        text="Modificar Producto",
        activeforeground="cyan",
        command=lambda: modificar_seleccionado(
            codigo_val,
            producto_val,
            cantidad_val,
            tree,
        ),
    )
    modificar_boton.grid(row=3, column=2, pady=(1, 0))

    # Boton para realizar una consulta sobre un producto y sus configuraciones.
    global boton_consulta
    boton_consulta = Button(
        root,
        text="Consultar",
        width=10,
        activeforeground="yellow",
        command=lambda: realizar_consulta(consulta_val, tree),
    )
    boton_consulta.grid(row=4, column=2, pady=(1, 0))

    # Boton para poder actualizar el inventario luego de realizar una consulta y sus configuraciones.
    global boton_actualizar
    boton_consulta = Button(
        root,
        text="Actualizar",
        width=10,
        activeforeground="deep pink",
        command=lambda: actualizar_treeview(tree),
    )
    boton_consulta.grid(row=5, column=2, pady=(1, 0))
