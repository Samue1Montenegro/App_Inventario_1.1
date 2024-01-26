# Importa simpledialog para poder lanzar un cuadro de dialogo simple, en este caso para poder modificar datos mediante un campo de entrada.
from tkinter import simpledialog

# Importa messagebox para poder realizar notificaciones como mensajes de alerta o confirmaciones
from tkinter import messagebox

# Importa re para poder utilizar expresiones regulares, en este caso para validar campos de entrada.
import re

import sqlite3

# ----------------------------------------------------------------------------------
# ######################      MODELO              ########################
# ----------------------------------------------------------------------------------


# Se crea la base de datos conectandola a sqlite3.
def conexion():
    conex = sqlite3.connect("mibase.db")
    return conex


# Se crea la tabla de la base de datos con sus columnas.
def crear_tabla(conex):
    conex = conexion()
    cursor = conex.cursor()
    sql = """CREATE TABLE IF NOT EXISTS productos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             codigo INTEGER,
             producto TEXT,
             cantidad INTEGER)
    """
    cursor.execute(sql)
    conex.commit()


# Se le asigna una variable a la funcion conexion para su posterior uso.
conex = conexion()

# Se crea un manejo de errores para la creacion y llamado a la base de datos y la tabla.
try:
    conexion()
    crear_tabla(conex)
except sqlite3.Error as e:
    print(f"Error al crear la base o tabla: {e}")


# Funcion para dar de alta un prodcuto
def alta(codigo, producto, cantidad, tree):
    # Expresiones regulares para controlar los campos de entrada.
    patron_id_prod = "^[0-9]+$"
    patron_producto = "^[A-Za-záéíóúñÑ0-9\s/_']+$"
    patron_cantidad = "^[0-9]+$"
    # Se toman los valores de los campos de entrada y se asignan a variables para su manipulacion.
    valor_codigo = str(codigo.get())
    valor_producto = str(producto.get())
    valor_cantidad = str(cantidad.get())
    print(
        "campos: ", valor_codigo, valor_producto, valor_cantidad
    )  # Impresion en consola para control.

    # Se realiza un if para ejecutar el control de caracteres en los campos de entradas.
    if (
        re.fullmatch(patron_id_prod, valor_codigo)
        and re.fullmatch(patron_producto, valor_producto)
        and re.fullmatch(patron_cantidad, valor_cantidad)
    ):
        # Se crea un control de datos para los campos de entrada Codigo y Cantidad. Se convierten a enteros los valores para no crear conflictos.
        try:
            val_codigo = int(valor_codigo)
            val_cantidad = int(valor_cantidad)
        except ValueError:
            print(
                "Error: El código y la cantidad deben ser números enteros."
            )  # Impresion en consola para control.
            # En caso de ocurrir un error se notifica al usuario.
            mostrar_notificacion(
                "Error: El código y la cantidad deben ser números enteros."
            )
            return False

        print(valor_producto, val_cantidad)  # Impresion en consola para control.
        # Se establece una conexión a la base de datos utilizando la función conexion() asignandola a una variable.
        conex = conexion()
        # Se asigna a una variable el objeto cursor() para ejecutar comandos y recuperar resultados.
        cursor = conex.cursor()
        # Se crea una tupla llamada data que contiene los valores que se insertarán en las columnas correspondientes de la tabla.
        # Estos valores provienen de las variables valor_codigo, valor_producto, valor_cantidad.
        data = (val_codigo, valor_producto, val_cantidad)
        # Se define la consulta SQL de inserción. La consulta utiliza parámetros de sustitución (?) para evitar conflictos.
        sql = "INSERT INTO productos(codigo, producto, cantidad) VALUES(?, ?, ?)"
        # Se ejecuta la consulta SQL con los valores de la tupla 'data'. Los valores se sustituyen en lugar de los marcadores de posición (?).
        cursor.execute(sql, data)
        # Se realiza la confirmación de los cambios en la base de datos.
        conex.commit()
        print("Estoy en alta todo ok")  # Impresion en consola para control.
        # Se llama a la funcion que actualiza el Treeview
        actualizar_treeview(tree)
        # Se limpian los campos de entrada despues que se ejecuta la accion.
        codigo.set(0)
        producto.set("")
        cantidad.set(0)
        # Se notifica al usuario de la accion exitosa.
        mostrar_notificacion("Producto agregado con éxito.")
    else:
        print("Error en campos de entrada")  # Impresion en consola para control.
        # Se notifica al usuario como debe introducir los datos en campos de entrada en caso de error.
        mostrar_notificacion(
            "Elementos no válidos!. Para Producto: solo letras incluida la ñ, números, caracteres /, _, ' y espacios permitidos.\n"
            "Para Cantidad: solo números enteros y decimales separados con una coma.\n"
            "Para numero ID/Codigo: Solo números enteros."
        )
        return False


# Funcion para eliminar un elemento seleccionandolo en el Treeview.
def borrar(codigo, tree):
    # Tomo los valores seleccionando el producto para eliminarlo completamente con sus valores.
    valor = tree.selection()
    print(valor)  # Impresion en consola para control.

    # Para asegurar que se ha seleccionado un producto se crea un condicional.
    if valor:
        # Obtiene la información de la fila seleccionada y la separa en un diccionario, se le asigna a una varaiable.
        item = tree.item(valor)
        print(item)  # Impresion por consola para control.
        #  Se accede al valor asociado con la clave "text" en el diccionario 'item', es decir, la primera columna del ítem en el Treeview
        codigo = item["text"]
        print("itens borrar", codigo)  # Impresion por consola para control.
        # Se establece una conexión a la base de datos utilizando la función conexion(), asignandola a una variable.
        conex = conexion()
        # Se asigna a una variable el objeto cursor() para ejecutar comandos y recuperar resultados.
        cursor = conex.cursor()
        # Se crea una tupla llamada 'data'que contiene el valor de codigo. La coma después de codigo asegura que data sea una tupla.
        # Se utiliza para reemplazar al marcador '?'.
        data = (codigo,)
        # Se define una instruccion SQL que representa una consulta de eliminación, que elimina filas de la tabla 'productos' coincidiendo con el valor de la columna 'id'
        sql = "DELETE FROM productos WHERE id = ?"
        #  Se ejecuta la consulta SQL utilizando el cursor. El valor de codigo se sustituye en la consulta donde aparece el marcador '?'
        cursor.execute(sql, data)
        # Se realiza la confirmación de los cambios en la base de datos.
        conex.commit()
        # Se le notifica al usuario que la accion es exitosa.
        mostrar_notificacion("Elemento eliminado con éxito.")
        # Se actualiza el Treeview luego de la accion.
        actualizar_treeview(tree)
    else:
        # En caso de no detectar una seleccion correcta se le notifica.
        mostrar_notificacion("Ocurrio un errror al eliminar el elemento ")


# Función para mostrar el inventario actualizado en el treeview, ya sea creado o modificado.
def actualizar_treeview(tree):
    # Elimina todas las filas existentes en el treeview para actualizarlo.
    for item in tree.get_children():
        tree.delete(item)
    # Se define una instruccion SQL que representa una consulta de selección.
    # Selecciona todas las columnas (*) de la tabla productos y las ordena en orden descendente (DESC) según la columna 'id'
    sql = "SELECT * FROM productos ORDER BY codigo DESC"
    # Se establece una conexión a la base de datos utilizando la función conexion() asignandola a una variable.
    conex = conexion()
    # Se asigna a una variable el objeto cursor() para ejecutar comandos y recuperar resultados.
    cursor = conex.cursor()
    # Se ejecuta la consulta SQL utilizando el cursor y se almacenan los resultados en la variable datos.
    datos = cursor.execute(sql)
    # Se recuperan todos los resultados de la consulta y se almacenan en la variable 'resultado'
    # 'fetchall()' devuelve una lista de tuplas, donde cada tupla representa una fila de resultados.
    resultado = datos.fetchall()
    # Variable para identidicar las filas pares de las impares.
    fondo_par = True
    # Este bucle itera a través de cada fila en los resultados obtenidos de la consulta.
    for fila in resultado:
        # Inserta una nueva fila en el treeview con los valores del producto actual.
        tree.insert(
            "",  # El primer argumento es el ID.
            0,  # El segundo argumento es la posición donde se insertará la nueva fila.
            text=fila[0],
            # Los valores de las columnas para la nueva fila.
            values=(fila[1], fila[2], fila[3]),
            # Etiqueta que determina el color de fondo de la fila.
            tags=(
                "odd" if fondo_par else "even"
            ),  # Se utilizan las etiquetas "odd" y "even" para poder asignarles configuraciones de color.
        )
        # Alterna el fondo para la próxima fila.
        fondo_par = not fondo_par
        # Agrega los colores de fondo para las filas impares y pares.
        tree.tag_configure("odd", background="#E8E8E8")  # Fondo gris claro.
        tree.tag_configure("even", background="white")  # Fondo blanco.


def modificar_seleccionado(codigo, producto, cantidad, tree):
    # Obtiene la selección actual en el treeview de consulta.
    seleccion = tree.selection()

    # Verifica si hay una selección.
    if seleccion:
        # Obtiene la información de la fila seleccionada y la separa en un diccionario, se le asigna a una varaiable.
        item = tree.item(seleccion)
        # El método item() de Treeview devuelve un diccionario con información de una fila seleccionada.
        # La clave "values" en ese diccionario contiene una tupla con los valores de cada columna en esa fila. Los valos se asignan a las variables.
        codigo, producto_actual, cantidad_actual = item["values"]

        # Muestra un cuadro de diálogo para ingresar el nuevo nombre.
        nuevo_producto = simpledialog.askstring(
            "Modificar Nombre",
            f"Ingrese el nuevo nombre para el producto (ID: {codigo}):",
            initialvalue=producto_actual,
        )

        # Verifica si se hizo clic en "Cancelar".
        if nuevo_producto is None:
            return producto

        # Muestra un cuadro de diálogo para ingresar la nueva cantidad.
        nueva_cantidad = simpledialog.askinteger(
            "Modificar Cantidad",
            f"Ingrese la nueva cantidad para {producto_actual} (ID: {codigo}):",
            initialvalue=cantidad_actual,
        )

        # Verifica si se hizo clic en "Cancelar".
        if nueva_cantidad is None:
            return cantidad

        # Actualiza la fila seleccionada en el treeview.
        tree.item(seleccion, values=(codigo, nuevo_producto, nueva_cantidad))

        # Se establece una conexión a la base de datos utilizando la función conexion() asignandola a una variable.
        conex = conexion()
        # Se asigna a una variable el objeto cursor() para ejecutar comandos y recuperar resultados.
        cursor = conex.cursor()
        # Se asignan los nuevos valores para producto, cantidad y el código del producto seleccionado a una variable.
        data = nuevo_producto, nueva_cantidad, codigo
        # Se define una instruccion SQL para realizar una actualización (UPDATE) en la tabla 'productos'.
        sql = "UPDATE productos SET producto = ?, cantidad = ?  WHERE codigo = ?;"
        # Se ejecuta la consulta SQL utilizando los valores contenidos en la variable 'data'
        cursor.execute(sql, data)
        # Se realiza la confirmación de los cambios en la base de datos.
        conex.commit()
        # Se notifica al usuario que la accion es exitosa.
        mostrar_notificacion("Producto modificado con éxito!")
    else:
        # Se notifica al usuario en caso de ocurrir un error.
        mostrar_notificacion("No se ha seleccionado ningún elemento!")


# Función para realizar la consulta y mostrar los resultados en el treeview de consulta.
def realizar_consulta(
    consulta,
    tree,
):
    try:
        # Obtiene la palabra clave de la entrada de consulta.
        # Toma la palabra clave y se convierte a minúsculas.
        # .strip() verifica si el campo de consulta no esta vacio
        palabra_clave = consulta.get().lower().strip()
        print("consulta", palabra_clave)  # Se imprime por consola para control.
        # Se establece una conexión a la base de datos utilizando la función conexion() asignandola a una variable.
        conex = conexion()
        # Se asigna a una variable el objeto cursor() para ejecutar comandos y recuperar resultados.
        cursor = conex.cursor()
        # Ejecuta una instruccion SQL para obtener los resultados filtrados por palabra clave.
        cursor.execute(
            "SELECT * FROM productos WHERE producto LIKE ?",
            ("%" + palabra_clave + "%",),
        )
        # Se recuperan todos los resultados de la consulta y se almacenan en la variable 'resultado'
        # 'fetchall()' devuelve una lista de tuplas, donde cada tupla representa una fila de resultados.
        resultados = cursor.fetchall()
        print("Resultados:", resultados)  # Se imprime por consola para control.
        print(
            "Resultados antes de limpiar:", resultados
        )  # Se imprime por consola para control.
        # Elimina todas las filas existentes en el treeview para actualizarlo.
        for i in tree.get_children():
            tree.delete(i)
        # Este bucle  iterar a través de los resultados obtenidos de una consulta a la base de datos y actualiza el treeview con esos resultados
        for resultado in resultados:
            # Inserta una nueva fila en el treeview con los valores del producto actual.
            tree.insert(
                "",
                "end",
                values=(resultado[1], resultado[2], resultado[3]),
                tags=(resultado[1] % 2),
            )
        # Se imprime por consola para control.
        print("Resultados después de agregar al treeview:", resultados)
        # Se limpia el campo de entrada despues que se ejecuta la accion.
        consulta.set("")
        # Se realiza la confirmación de los cambios en la base de datos.
        conex.commit()
    # Entra en este bloque cuando ocurre una excepción de cualquier tipo. y Asigna la instancia a la varible e para ser utilizada.
    except Exception as e:
        # Se le notifica al usuario en caso de error y se muestran detaller del error.
        mostrar_notificacion(f"Hubo un error: {str(e)}")


# Funcion para poder mostrar notificaciones en las acciones o mostrar errores.
def mostrar_notificacion(mensaje):
    messagebox.showinfo("Notificación", mensaje)
