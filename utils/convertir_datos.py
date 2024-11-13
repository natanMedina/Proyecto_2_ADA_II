def convertir_mpl_a_dzn(datos_mpl, archivo_dzn):
    try:
        # Asumimos que los datos están en el orden que especificaste
        n = int(datos_mpl[0].strip())  # Número de personas
        m = int(datos_mpl[1].strip())  # Número de opiniones
        
        # Extraemos las listas de valores
        distribucion = datos_mpl[2].strip()  # Lista de distribución de opiniones
        valores_opiniones = datos_mpl[3].strip()  # Lista de valores de opiniones
        costos_extras = datos_mpl[4].strip()  # Lista de costos extras
        costos_desplazamiento = [line.strip() for line in datos_mpl[5:5 + m]]  # Matriz de costos
        costo_total_maximo = float(datos_mpl[5 + m].strip())  # Costo total máximo
        max_movimientos = int(datos_mpl[6 + m].strip())  # Máximo de movimientos
        
        # Creamos el archivo .dzn con los datos extraídos
        with open(archivo_dzn, 'w') as file:
            file.write(f"n = {n};\n")
            file.write(f"m = {m};\n")
            file.write(f"p = [{distribucion}];\n")
            file.write(f"v = [{valores_opiniones}];\n")
            file.write(f"ce = [{costos_extras}];\n")
            
            # Escribimos la matriz de costos de desplazamiento
            file.write("c = [| ")
            file.write(" | ".join(costos_desplazamiento))
            file.write(" |];\n")
            
            file.write(f"ct = {costo_total_maximo};\n")
            file.write(f"maxM = {max_movimientos};\n")
        
        return True  # Indica que la conversión fue exitosa

    except (IndexError, ValueError) as e:
        print(f"Error al convertir el archivo .mpl a .dzn: {e}")
        return False  # Indica que ocurrió un error durante la conversión