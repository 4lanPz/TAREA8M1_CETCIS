# ==============================
# SISTEMA DE INVENTARIO Y PEDIDOS

inventario = []
pedidos = []

# Funciones para verificar valores ingresados
def leer_entero(mensaje, minimo=None):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"Error: el valor debe ser mayor o igual a {minimo}.")
            else:
                return valor
        except ValueError:
            print("Error: ingrese un número entero válido")

def leer_decimal(mensaje, minimo=None):
    while True:
        try:
            valor = float(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"Error: el valor debe ser mayor o igual a {minimo}.")
            else:
                return valor
        except ValueError:
            print("Error: ingrese un número válido")

# Funciones de apoyo
def buscar_producto_por_nombre(nombre):
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return producto
    return None

def mostrar_productos():
    print("\n=== LISTADO DE PRODUCTOS ===")
    if len(inventario) == 0:
        print("No hay productos registrados")
        return
    for i, producto in enumerate(inventario, start=1):
        print(f"{i}. {producto['nombre']} | Cantidad: {producto['cantidad']} | Precio: ${producto['precio']:.2f}")

def mostrar_pedidos():
    print("\n=== LISTADO DE PEDIDOS ===")
    if len(pedidos) == 0:
        print("No hay pedidos registrados.")
        return

    for i, pedido in enumerate(pedidos, start=1):
        print(
            f"{i}. Cliente: {pedido['cliente']} | "
            f"Producto: {pedido['producto']} | "
            f"Cantidad: {pedido['cantidad']} | "
            f"Total: ${pedido['total']:.2f}"
        )

# ==============================
# FUNCIONES DE INVENTARIO
def registrar_producto():
    print("\n=== REGISTRAR PRODUCTO ===")
    nombre = input("Nombre del producto: ").strip()
    if nombre == "":
        print("Error: el nombre no puede estar vacío")
        return
    producto_existente = buscar_producto_por_nombre(nombre)
    if producto_existente is not None:
        print("Ese producto ya existe en el inventario.")
        opcion = input("¿Desea aumentar la cantidad existente? (s/n): ").strip().lower()
        if opcion == "s":
            cantidad_extra = leer_entero("Cantidad a agregar: ", 1)
            precio_nuevo = leer_decimal("Nuevo precio del producto: ", 0)
            producto_existente["cantidad"] += cantidad_extra
            producto_existente["precio"] = precio_nuevo
            print("Producto actualizado correctamente")
        else:
            print("Operación cancelada")
        return
    cantidad = leer_entero("Cantidad disponible: ", 0)
    precio = leer_decimal("Precio del producto: ", 0)
    producto = {
        "nombre": nombre,
        "cantidad": cantidad,
        "precio": precio
    }
    inventario.append(producto)
    print("Producto registrado correctamente")

def editar_producto():
    print("\n=== EDITAR PRODUCTO ===")
    if len(inventario) == 0:
        print("No hay productos para editar")
        return
    mostrar_productos()
    opcion = leer_entero("Seleccione el número del producto a editar: ", 1)
    if opcion > len(inventario):
        print("Opción no válida.")
        return
    producto = inventario[opcion - 1]
    print("Presione Enter si no desea cambiar un dato")
    nuevo_nombre = input(f"Nuevo nombre [{producto['nombre']}]: ").strip()
    nueva_cantidad = input(f"Nueva cantidad [{producto['cantidad']}]: ").strip()
    nuevo_precio = input(f"Nuevo precio [{producto['precio']}]: ").strip()
    if nuevo_nombre != "":
        producto["nombre"] = nuevo_nombre
    if nueva_cantidad != "":
        try:
            cantidad_entera = int(nueva_cantidad)
            if cantidad_entera >= 0:
                producto["cantidad"] = cantidad_entera
            else:
                print("La cantidad no puede ser negativa. Se conserva el valor anterior")
        except ValueError:
            print("Cantidad no válida. Se conserva el valor anterior")
    if nuevo_precio != "":
        try:
            precio_decimal = float(nuevo_precio)
            if precio_decimal >= 0:
                producto["precio"] = precio_decimal
            else:
                print("El precio no puede ser negativo. Se conserva el valor anterior")
        except ValueError:
            print("Precio no válido. Se conserva el valor anterior")
    print("Producto editado correctamente")

def eliminar_producto():
    print("\n=== ELIMINAR PRODUCTO ===")
    if len(inventario) == 0:
        print("No hay productos para eliminar")
        return
    mostrar_productos()
    opcion = leer_entero("Seleccione el número del producto a eliminar: ", 1)
    if opcion > len(inventario):
        print("Opción no válida.")
        return
    producto_eliminado = inventario.pop(opcion - 1)
    print(f"Producto '{producto_eliminado['nombre']}' eliminado correctamente")

# ==============================
# FUNCIONES DE PEDIDOS
def registrar_pedido():
    print("\n=== REGISTRAR PEDIDO ===")
    if len(inventario) == 0:
        print("No se puede registrar un pedido porque no hay productos en inventario")
        return
    cliente = input("Nombre del cliente: ").strip()
    if cliente == "":
        print("Error: el nombre del cliente no puede estar vacío")
        return
    mostrar_productos()
    opcion = leer_entero("Seleccione el número del producto: ", 1)
    if opcion > len(inventario):
        print("Opción no válida.")
        return
    producto = inventario[opcion - 1]
    cantidad_pedida = leer_entero("Cantidad pedida: ", 1)
    if cantidad_pedida > producto["cantidad"]:
        print("Error: no hay suficiente stock disponible")
        return
    total = cantidad_pedida * producto["precio"]
    pedido = {
        "cliente": cliente,
        "producto": producto["nombre"],
        "cantidad": cantidad_pedida,
        "total": total
    }
    pedidos.append(pedido)
    producto["cantidad"] -= cantidad_pedida
    print("Pedido registrado correctamente")
    print(f"Total del pedido: ${total:.2f}")

def editar_pedido():
    print("\n=== EDITAR PEDIDO ===")
    if len(pedidos) == 0:
        print("No hay pedidos para editar")
        return
    mostrar_pedidos()
    opcion = leer_entero("Seleccione el número del pedido a editar: ", 1)
    if opcion > len(pedidos):
        print("Opción no válida.")
        return
    pedido = pedidos[opcion - 1]
    print("Presione Enter si no desea cambiar un dato")
    nuevo_cliente = input(f"Nuevo cliente [{pedido['cliente']}]: ").strip()
    nueva_cantidad = input(f"Nueva cantidad [{pedido['cantidad']}]: ").strip()

    if nuevo_cliente != "":
        pedido["cliente"] = nuevo_cliente
    if nueva_cantidad != "":
        try:
            cantidad_nueva = int(nueva_cantidad)
            if cantidad_nueva > 0:
                producto = buscar_producto_por_nombre(pedido["producto"])
                if producto is not None:
                    diferencia = cantidad_nueva - pedido["cantidad"]
                    if diferencia > 0:
                        if diferencia <= producto["cantidad"]:
                            producto["cantidad"] -= diferencia
                            pedido["cantidad"] = cantidad_nueva
                            pedido["total"] = pedido["cantidad"] * producto["precio"]
                        else:
                            print("No hay suficiente stock para aumentar esa cantidad")
                    elif diferencia < 0:
                        producto["cantidad"] += abs(diferencia)
                        pedido["cantidad"] = cantidad_nueva
                        pedido["total"] = pedido["cantidad"] * producto["precio"]
                    else:
                        print("La cantidad es la misma, no hubo cambios")
                else:
                    print("El producto asociado al pedido ya no existe en inventario")
            else:
                print("La cantidad debe ser mayor que cero")
        except ValueError:
            print("Cantidad no válida. Se conserva el valor anterior")
    print("Pedido editado correctamente")

def eliminar_pedido():
    print("\n=== ELIMINAR PEDIDO ===")
    if len(pedidos) == 0:
        print("No hay pedidos para eliminar")
        return
    mostrar_pedidos()
    opcion = leer_entero("Seleccione el número del pedido a eliminar: ", 1)
    if opcion > len(pedidos):
        print("Opción no válida.")
        return
    pedido_eliminado = pedidos.pop(opcion - 1)
    producto = buscar_producto_por_nombre(pedido_eliminado["producto"])
    if producto is not None:
        producto["cantidad"] += pedido_eliminado["cantidad"]
    print("Pedido eliminado correctamente")


# ==============================
# MENÚS

def menu_inventario():
    while True:
        print("\n=== MENÚ INVENTARIO ===")
        print("1. Registrar producto")
        print("2. Mostrar productos")
        print("3. Editar producto")
        print("4. Eliminar producto")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            editar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

def menu_pedidos():
    while True:
        print("\n=== MENÚ PEDIDOS ===")
        print("1. Registrar pedido")
        print("2. Mostrar pedidos")
        print("3. Editar pedido")
        print("4. Eliminar pedido")
        print("5. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_pedido()
        elif opcion == "2":
            mostrar_pedidos()
        elif opcion == "3":
            editar_pedido()
        elif opcion == "4":
            eliminar_pedido()
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

def menu_principal():
    while True:
        print("\n===================================")
        print("Sistema de Gestión de Inventario y Pedidos")
        print("===================================")
        print("1. Gestionar inventario")
        print("2. Gestionar pedidos")
        print("3. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            menu_inventario()
        elif opcion == "2":
            menu_pedidos()
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")


# ==============================
# INICIO DEL PROGRAMA
menu_principal()