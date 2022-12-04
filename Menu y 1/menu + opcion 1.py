import cv2
import numpy as np


# Función del menú
def menu():
    titulo = ('\033[1m' + "APLICACIÓN ESTEGANOCR" + '\033[0m')
    print(titulo.center(90))
    print("1) Insertar mensaje oculto en una imagen"
          "\n2) Extraer mensaje oculto de una imagen"
          "\n3) Convertir la imagen a escala de grises"
          "\n4) Extraer cadena visible en una imagen"
          "\n5) Informe de las extracciones (PDF)"
          "\n6) Salir")


# Pasa el mensaje a binario
def messageToBinary(message):
    if type(message) == str:  # Filtro si es string
        return ''.join([format(ord(i), "08b") for i in message])
    elif type(message) == bytes or type(message) == np.ndarray:  # Filtro si es ya binario o un array
        return [format(i, "08b") for i in message]
    elif type(message) == int or type(message) == np.uint8:  # Filtro si es un número o una imagen
        return format(message, "08b")
    else:
        raise TypeError("Error de tipo de archivo enviado")  # Si no es nada de lo anterior reporto el error


# Codifica el texto
def hideData(image, secret_message):
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    if len(secret_message) > n_bytes:
        # Veo si hay más bytes que cadena en el mensaje para dar error
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")
    secret_message += "#####"
    data_index = 0
    binary_secret_msg = messageToBinary(secret_message)  # Paso a binario
    data_len = len(binary_secret_msg)  # Obtengo el tamaño de los binarios
    for values in image:  # Recorro los elementos de la image
        for pixel in values:  # Recorro los pixeles de antes en la imagen para obtener los bytes
            r, g, b = messageToBinary(pixel)  # Obtengo los bytes del pixel
            if data_index < data_len:
                # Compruebo el valor final del byte y lo modifico
                pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
                # Compruebo el valor final del byte y lo modifico
            if data_index < data_len:
                pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
                # Compruebo el valor final del byte y lo modifico
            if data_index < data_len:
                pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            # Compruebo el valor final del byte y lo modifico
            if data_index >= data_len:
                break
    return image


# Inserta el mensaje a ocultar dentro de la imagen
def insertar():
    print('\033[1m' + "OPCIÓN: Insertar mensaje oculto en una imagen" + '\033[0m')
    imagen = cv2.imread("proyimag1T.png")  # Leo la imagen
    imgname = "Proyimag1T.png"  # doy el nombre de imagen
    tamano = imagen.shape  # Obtengo los tamaños de la imagen
    anchura = tamano[0]
    altura = tamano[1]
    print(f"{imgname} tiene de {anchura} de ancho y de {altura} de alto.")
    mensaje = input("Introduzca el mensaje de texto a ocultar: ")  # Pido el mensaje oculto
    archivo = "Proyimod1T.png"
    encoded_image = hideData(imagen, mensaje)  # Paso a la función la imagen y el mensaje a ocultar
    cv2.imwrite(archivo, encoded_image)  # Escribo sobre la imagen el texto
    mi_txt = open('Extraccion.txt', 'w')
    mi_txt.write(mensaje + '\n')  # Guardo el texto oculto en el txt
    mi_txt.close()


# Función principal
bolean = 0
while bolean != 1:  # Sale del bucle si se introduce el número 6
    menu()  # Llamamos a la función menú que nos lo imprime
    i = int(input("Opción: "))  # Pedimos la opción que quiere ejecute
    # Filtro la opción
    if i == 1:
        insertar()
    if i == 2:
        print('extraer_oculto()')
    if i == 3:
        print('convertir()')
    if i == 4:
        print('extraer_visible()')
    if i == 5:
        print('informe()')
    if i == 6:
        bolean = 1