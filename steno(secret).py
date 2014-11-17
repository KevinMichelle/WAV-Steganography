import sys
import os.path
import datetime
import math
import random

def crear_abecedario(control):
	abecedario = []
	if control:
		for i in xrange(33, 97):
			if i == 34:
				abecedario.append(chr(126))
			elif i == 39:
				abecedario.append(chr(123))
			elif i == 96:
				abecedario.append(chr(125))
			else:
				abecedario.append(chr(i).lower())
	else:
		for i in xrange(0, 256):
			abecedario.append(chr(i))
	return abecedario
	
def bits_a_numero(cadena):
	return int(cadena, 2)
	
def numero_a_bits(numero, numero_de_bits):
	formato_de_bits = "{0:0" + str(numero_de_bits) + "b}"
	return formato_de_bits.format(numero)
	
def organizar_posiciones(mensaje_preparado, numero_de_bits, control):
	pos_actual = 44
	posiciones = []
	for letra in mensaje_preparado:
		nuevas_posiciones = crear_posiciones(pos_actual, numero_de_bits, control)
		pos_actual = nuevas_posiciones[len(nuevas_posiciones) - 1]
		for i in nuevas_posiciones:
			posiciones.append(i)
	return posiciones
	
def posiciones_recuperar(clave, numero_de_bits, control):
	pos_actual = 44
	posiciones = []
	while True:
		nuevas_posiciones = crear_posiciones(pos_actual, numero_de_bits, control)
		pos_actual = nuevas_posiciones[len(nuevas_posiciones) - 1]
		if pos_actual == clave:
			for i in nuevas_posiciones:
				posiciones.append(i)
			break
		elif pos_actual > clave:
			print "\n\tEs posible que te salga basura en tu mensaje"
			break
		else:
			for i in nuevas_posiciones:
				posiciones.append(i)
	return posiciones
		
def crear_posiciones(pos_actual, numero_de_bits, control):
	posiciones = []
	... No disponible hasta que lo revise la maestra
	return posiciones
	
	
def buscar_en_abecedario(letra, abecedario):
	for i in abecedario:
		if letra == i:
			return True
	return False

def preparar_mensaje(temporal, abecedario):
	mensaje = (temporal.lower()).strip()
	mensaje_lista = []
	for i in mensaje:
		if i == " " or i == "\n":
			mensaje_lista.append(chr(92) + chr(92)) #caracrer \
		elif buscar_en_abecedario(i, abecedario):
			mensaje_lista.append(i)
		else:
			mensaje_lista.append(abecedario[30]) #caracter ?
	return "".join(mensaje_lista)
	
def cambiar_cadena_binaria(cadena_binaria, bit):
	nueva_cadena = []
	for i in xrange(len(cadena_binaria)):
		if i == 7:
			nueva_cadena.append(bit)
		else:
			nueva_cadena.append(cadena_binaria[i])
	return "".join(nueva_cadena)
	
def crear_nuevo_archivo(arreglo, ext, nombre):
	inicio = datetime.datetime.now()
	filename = nombre + ext
	with open(filename, "wb") as nombre:
		nombre.writelines(arreglo)
	fin = datetime.datetime.now()
	tiempo_ejecucion = fin - inicio
	print "\tTiempo para guardar el nuevo archivo : {} segundos".format(tiempo_ejecucion)
	print "\n\tEl archivo se guardo bajo el nombre de: " + filename
	
		
def cifrado(mensaje, abecedario, numero_de_bits, clave):
	formato_de_bits = "{0:0" + str(numero_de_bits) + "b}"
	mensaje_cadena_binaria = []
	for i in xrange(len(mensaje)):
		indice = abecedario.index(mensaje[i])
		mensaje_cadena_binaria.append(formato_de_bits.format(indice))
	mensaje_cadena = "".join(mensaje_cadena_binaria)
	cadena_cifrada = xor(mensaje_cadena, clave)
	contador = 0
	mensaje_cifrado_binario = []
	for i in xrange(len(cadena_cifrada)):
		if (i > 0 and i % numero_de_bits == 0):
			mensaje_cifrado_binario.append(caracter_temporal)
			caracter_temporal = []
			caracter_temporal.append(cadena_cifrada[i])
		elif i == 0:
			caracter_temporal = []
			caracter_temporal.append(cadena_cifrada[i])
		elif i == len(cadena_cifrada) - 1:
			caracter_temporal.append(cadena_cifrada[i])
			mensaje_cifrado_binario.append(caracter_temporal)
		else:
			caracter_temporal.append(cadena_cifrada[i])
	mensaje_cifrado_lista = []
	for i in xrange(len(mensaje_cifrado_binario)):
		nuevo_caracter = int("".join(mensaje_cifrado_binario[i]), 2)
		mensaje_cifrado_lista.append(abecedario[nuevo_caracter])
	return "".join(mensaje_cifrado_lista)

def xor(mensaje, clave):
	cifrado = []
	for i in xrange(len(mensaje)):
		cifrado.append(str(int(mensaje[i]) ^ int(clave[i%len(clave)])))
	return "".join(cifrado)
	
def actualizar_arreglo_bytes(arreglo_bytes, bytes_a_cambiar, mensaje, abecedario, numero_de_bits):
	actual = 0
	for i in xrange(len(mensaje)):
		#Preparar caracter en mensaje
		caracter = mensaje[i]
		pos_caracter = abecedario.index(caracter)
		cadena_binaria_caracter = numero_a_bits(pos_caracter, numero_de_bits)
		#Fin preparar caracter en mensaje
		contador_bit_caracter = 0
		for j in xrange(actual, actual + (numero_de_bits)):
			
			#Datos del byte en arreglo
			byte_por_cambiar = bytes_a_cambiar[j]
			byte_caracter = ord(arreglo_bytes[byte_por_cambiar])
			bits_caracter = numero_a_bits(byte_caracter, 8) #de 0 a 255
			bit_caracter_mensaje = cadena_binaria_caracter[contador_bit_caracter]
			#Fin datos del byte en arreglo
			
			#Cambiar cadena binaria del byte
			nueva_cadena_binaria = cambiar_cadena_binaria(bits_caracter, bit_caracter_mensaje)
			nuevo_byte = bits_a_numero(nueva_cadena_binaria)
			#Fin cadena binaria del byte
			
			contador_bit_caracter += 1
			arreglo_bytes[byte_por_cambiar] = chr(nuevo_byte)
			
		actual += numero_de_bits 
	return arreglo_bytes

def ocultar(name, archivo_a_ocultar):
	#Checar si se va a guardar un archivo binario o un mensaje de texto
	datos_archivo = os.path.splitext(archivo_a_ocultar)
	file_ext_archivo = datos_archivo[len(datos_archivo) - 1]
	mensaje_texto = True
	if file_ext_archivo == ".txt":
		archivo_texto = open(archivo_a_ocultar, 'r')
		texto = archivo_texto.read()
		archivo_texto.close()
		abecedario = crear_abecedario(True)
		mensaje_preparado = preparar_mensaje(texto, abecedario)
	else:
		mensaje_texto = False
		mensaje_preparado = leer_bytes(archivo_a_ocultar)
		abecedario = crear_abecedario(False)
	arreglo_bytes = leer_bytes(name)
	
	inicio = datetime.datetime.now()
	
	datos_audio = os.path.splitext(name)
	file_ext = datos_audio[len(datos_audio) - 1]
	maximo = "{0:b}".format(len(abecedario) - 1)
	numero_de_bits = len(maximo)
	
	if mensaje_texto:
		bytes_a_cambiar = organizar_posiciones(mensaje_preparado, numero_de_bits, True)
	else:
		bytes_a_cambiar = organizar_posiciones(mensaje_preparado, numero_de_bits, False)
	ultimo_byte_por_cambiar = bytes_a_cambiar[len(bytes_a_cambiar) - 1]
	if ultimo_byte_por_cambiar < len(arreglo_bytes):
		clave_binaria_texto = "{0:0b}".format(ultimo_byte_por_cambiar)
		clave_secreta = random.randrange(1, 999)
		clave_secreta_binaria = "{0:0b}".format(clave_secreta)
		if mensaje_texto:
			llave_clave = cifrado(str(ultimo_byte_por_cambiar), abecedario, numero_de_bits, clave_secreta_binaria)
			mensaje_cifrado = cifrado(mensaje_preparado, abecedario, numero_de_bits, clave_binaria_texto)
			arreglo_bytes = actualizar_arreglo_bytes(arreglo_bytes, bytes_a_cambiar, mensaje_cifrado, abecedario, numero_de_bits)
			crear_nuevo_archivo(arreglo_bytes, file_ext, "nuevo")
			print '\tClaves para recuperar el mensaje: "{}" {}'.format(llave_clave, clave_secreta)
			print "\n\tLongitud del mensaje original ({}), del mensaje preparado ({}), del mensaje cifrado ({})".format(len(texto), len(mensaje_preparado), len(mensaje_cifrado))
			fin = datetime.datetime.now()
			tiempo_ejecucion = fin - inicio
			print "\n\tTiempo para ocultar un mensaje de {} caracteres: {} segundos".format(len(texto), tiempo_ejecucion)
		else:
			llave_clave_temporal = cifrado(str(ultimo_byte_por_cambiar), abecedario, numero_de_bits, clave_secreta_binaria)
			llave_clave_lista = []
			for i in xrange(len(llave_clave_temporal)):
				llave_clave_lista.append(str(abecedario.index(llave_clave_temporal[i])).zfill(3))
			llave_clave = "".join(llave_clave_lista)
			arreglo_bytes = actualizar_arreglo_bytes(arreglo_bytes, bytes_a_cambiar, mensaje_preparado, abecedario, numero_de_bits)
			crear_nuevo_archivo(arreglo_bytes, file_ext, "nuevo")
			print '\tClaves para recuperar el mensaje: "{}" {}b'.format(llave_clave, clave_secreta)
			print "\n\tLongitud del mensaje original ({}), del mensaje no cifrado ({})".format(len(mensaje_preparado), len(mensaje_preparado))
			fin = datetime.datetime.now()
			tiempo_ejecucion = fin - inicio
			print "\n\tTiempo para ocultar un archivo binario de {} bytes: {} segundos".format(len(arreglo_bytes), tiempo_ejecucion)
			
	else:
		print "\tNo es posible guardar el mensaje por la longitud de caracteres"
		print ultimo_byte_por_cambiar, len(arreglo_bytes)
	
		
	
def recuperar(name, llave_clave, clave, mensaje_texto):
	if mensaje_texto:
		abecedario = crear_abecedario(True)
	else:
		abecedario = crear_abecedario(False)
	maximo = "{0:b}".format(len(abecedario) - 1)
	numero_de_bits = len(maximo)
	bits_recuperados = []
	clave_secreta_binaria = "{0:0b}".format(clave)
	if mensaje_texto:
		clave_del_texto_recuperado = cifrado(llave_clave, abecedario, numero_de_bits, clave_secreta_binaria)
	else:
		llave_clave_lista = []
		for i in xrange(int(len(llave_clave)/3.0)):
			pos_temporal = (i * 3)
			llave_clave_lista.append(abecedario[int(llave_clave[pos_temporal:pos_temporal+3])])
		llave_clave_real = "".join(llave_clave_lista)
		clave_del_texto_recuperado = cifrado(llave_clave_real, abecedario, numero_de_bits, clave_secreta_binaria)
	if not clave_del_texto_recuperado.isdigit():
		print "\tLas claves son sospechosas"
		exit(1)
	clave_del_texto_recuperado_binaria = "{0:0b}".format(int(clave_del_texto_recuperado))
	arreglo_bytes = leer_bytes(name)
	inicio = datetime.datetime.now()
	bytes_por_checar = posiciones_recuperar(int(clave_del_texto_recuperado), numero_de_bits, mensaje_texto)
	print
	for i in xrange(len(bytes_por_checar)):
		if i % 10000 == 0:
			print "\t\t{} de {}, por favor espera un poco\n".format(i, len(bytes_por_checar))
		byte = bytes_por_checar[i]
		byte_caracter  = ord(arreglo_bytes[byte])
		bits_caracter = numero_a_bits(byte_caracter, 8) #de 0 a 255
		bits_recuperados.append(bits_caracter[len(bits_caracter) - 1])
		caracteres_recuperados = []
		contador = 0
		for i in xrange(len(bits_recuperados)/ numero_de_bits):
			temporal = []
			for j in xrange(contador, ((i + 1) * numero_de_bits)):
				temporal.append(bits_recuperados[j])
				contador = j
			contador += 1
			bits_caracter = "".join(temporal)
			numero = bits_a_numero(bits_caracter)
			caracter = abecedario[numero]
			caracteres_recuperados.append(caracter)
	if mensaje_texto:
		mensaje_oculto = "".join(caracteres_recuperados)
		mensaje_secreto = cifrado(mensaje_oculto, abecedario, numero_de_bits, clave_del_texto_recuperado_binaria)
		mensaje_final = []
		temporal = []
		contador = 0
		while contador < len(mensaje_secreto):
			if mensaje_secreto[contador] == chr(92) and mensaje_secreto[(contador + 1) % len(mensaje_secreto)] == chr(92):
				contador += 1
				mensaje_final.append("".join(temporal))
				temporal = []
			else:
				temporal.append(mensaje_secreto[contador])
			contador += 1
			if contador == len(mensaje_secreto):
				mensaje_final.append("".join(temporal))
		
		print "\n\tMensaje oculto"
		print "\t\t", mensaje_oculto
		print "\n\tMensaje recuperado"
		print "\t\t", " ".join(mensaje_final)
		fin = datetime.datetime.now()
		tiempo_ejecucion = fin - inicio
		print "\n\tTiempo para recuperar un mensaje de texto: {} segundos".format(tiempo_ejecucion)
	else:
		print "\tRecuperando archivo binario...\n"
		ext = "." + "".join(caracteres_recuperados[1:4])
		crear_nuevo_archivo(caracteres_recuperados, ext, "recuperar")
		fin = datetime.datetime.now()
		tiempo_ejecucion = fin - inicio
		print "\n\tTiempo para recuperar un archivo binario: {} segundos".format(tiempo_ejecucion)
		
	
def ayuda():
	print
	print "Para ejecutar el programa sigue el siguiente formato"
	print
	print "\t-e archivo_contenedor archivo_texto - > Guardar mensaje"
	print "\t-d archivo_contenedor clave clave - > Recuperar mensaje"
	
	print
	print "NOTA: solo copia la clave desde la terminal"

	
def bits_a_numero(cadena_binaria):
	return int(cadena_binaria, 2)
	
def leer_bytes(nombre):
	inicio = datetime.datetime.now()
	arreglo_bytes = []
	with open(nombre, "rb") as nombre:
		byte = nombre.read(1)
		while byte != "":
			arreglo_bytes.append(byte)
			byte = nombre.read(1)
	fin = datetime.datetime.now()
	tiempo_ejecucion = fin - inicio
	print "\tTiempo para leer el archivo : {} segundos".format(tiempo_ejecucion)
	return arreglo_bytes

if len(sys.argv) == 4 or len(sys.argv) == 5:
	op = sys.argv[1]
	name = sys.argv[2]
	
	if op == "-e" and len(sys.argv) == 4:
		nombre_archivo_texto = sys.argv[3]
		print "\nModo seleccionado: Guardar mensaje\n"
		if os.path.isfile(name):
			if os.path.isfile(nombre_archivo_texto):
				ocultar(name, nombre_archivo_texto)
			else:
				print "No existe el archivo de texto"
		else:
			print "No existe el archivo de audio"
	elif op == "-d" and len(sys.argv) == 5:
		clave_principal = sys.argv[3]
		clave_secreta = sys.argv[4]
		if not clave_secreta.isdigit() and clave_secreta[len(clave_secreta) - 1] == "b":
			clave_temporal = clave_secreta[0:len(clave_secreta) - 1]
			if clave_temporal.isdigit() and clave_principal.isdigit():
				clave = int(clave_temporal)
				print "\n*Modo seleccionado: Recuperar mensaje\n"
				if os.path.isfile(name):
					recuperar(name, clave_principal, clave, False)
				else:
					print "No existe archivo"
			else:
				print "Se esperaba digitos, caracter al final"
		elif clave_secreta.isdigit():
			clave = int(clave_secreta)
			print "\n*Modo seleccionado: Recuperar mensaje\n"
			if os.path.isfile(name):
				recuperar(name, clave_principal, clave, True)
			else:
				print "No existe archivo"
		else:
			print "Algo rarocon tu clave"
	else:
		ayuda()
else:
	ayuda()
