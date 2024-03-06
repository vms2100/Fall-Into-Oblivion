import os
import threading
import time
import hashlib
import shutil
import hmac
import random
import string
import AES
import Salsa20

#variáveis globais
pasta = 'fall-into-oblivion'
iniciado = false
pinset = false
pin = ''
cifra = -1
tamanho = -1

def existe(tipoFile, tipoPasta, nomePasta):
    caminho = os.path.join(Pasta, tipoPasta)
    caminho = os.path.join(caminho, nomePasta + tipoFile)

    if os.path.exists(caminho):
        return caminho
    else:
        print("Ficheiro não existe!")
        return None

def islegit():
    nomef = str(input('Nome do ficheiro a verificar:'))
    filee = existe("", "", nomef)
    if filee:
        caminho2 = os.path.join(Pasta, "Hash")
        caminho2 = os.path.join(caminho2, nomef + str(".hmac"))
        if os.path.exists(caminho2):
            fileh = open(caminho2, "r")
            hmacf = fileh.read()
            fileh.close()
            caminho3 = os.path.join(Pasta, "Cifrado")
            caminho3 = os.path.join(caminho3, nomef + str(".key"))
            chavea = open(caminho3, "r")
            chave = chavea.read()
            chavea.close()
            chavee = chave.encode('utf-8')
            arquivo = open(filee, "r")
            arquivotexto = arquivo.readlines()
            texto = ''
            for linhas in arquivotexto:
                texto = texto + str(linhas)
            texto2 = texto.encode('utf-8')
            hmac1 = hmac.new(chavee, texto2, digestmod="sha1")
            if hmac1.hexdigest() == hmacf:
                print("O ficheiro não foi alterado!")
            else:
                print("O ficheiro foi adulterado!")

        else:
            print("A pasta foi alterada, é impossível dizer se o ficheiro está intacto!")
    else:
        print("Ficheiro não existe!")

def calcularHmac(chave, fic):
    chavee = chave.encode('utf-8')
    caminho = os.path.join(Pasta, fic)
    caminho2 = os.path.join(Pasta, "Hash")
    caminho2 = os.path.join(caminho2, fic + str(".hmac"))
    texto = ''
    arquivo = open(caminho, "r")
    for linha in arquivo:
        texto = texto + str(linha)
    texto2 = texto.encode('utf-8')

    hmac1 = hmac.new(chavee, texto2, digestmod="sha1")
    arquivo2 = open(caminho2, "w")
    arquivo2.write(str(hmac1.hexdigest()))

def guardarChave(chave, nomef):
    caminho = os.path.join(Pasta, "Cifrado")
    caminho = os.path.join(caminho, nomef + str(".key"))
    arquivo = open(caminho, "wb")
    arquivo.write(chave.encode('utf-8'))
    arquivo.close()

def definirCifra():
    global Cifra
    global Tamanho

    while Cifra < 0 or Cifra > 2:
        print("Escolha uma opção:")
        print("1. AES")
        print("2. Salsa20")
        Cifra = int(input())

    while Tamanho < 0:
        print("Escolha o tamanho da chave (em bytes):")
        Tamanho = int(input())

def gerarChave():
    letras = string.ascii_letters + string.digits
    chave = ''.join(random.choice(letras) for i in range(Tamanho))
    return chave

def encriptarAES(nomef):
    global PinSet
    global PIN

    chave = gerarChave()
    guardarChave(chave, nomef)

    caminho1 = existe(".txt", "Texto", nomef)
    caminho2 = existe(".aes", "Cifrado", nomef)
    file1 = open(caminho1, "r")
    texto = file1.read()
    file1.close()

    cipher = AES.new(chave.encode('utf-8'), AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(texto.encode('utf-8'))

    file2 = open(caminho2, "wb")
    file2.write(cipher.nonce)
    file2.write(ciphertext)
    file2.write(tag)
    file2.close()

    if PinSet:
        caminho3 = existe(".key", "Cifrado", nomef)
        cipher2 = AES.new(PIN.encode('utf-8'), AES.MODE_EAX)
        nonce2 = cipher2.nonce
        ciphertext2, tag2 = cipher2.encrypt_and_digest(chave.encode('utf-8'))

        file3 = open(caminho3, "wb")
        file3.write(cipher2.nonce)
        file3.write(ciphertext2)
        file3.write(tag2)
        file3.close()

    calcularHmac(chave, nomef + str(".txt"))

    if os.path.exists(caminho1):
        os.remove(caminho1)

def desencriptarAES(nomef):
    global PinSet
    global PIN

    caminho1 = existe(".aes", "Cifrado", nomef)
    caminho2 = existe(".txt", "Texto", nomef)
    caminho3 = existe(".key", "Cifrado", nomef)

    if PinSet and os.path.exists(caminho3):
        cipher = AES.new(PIN.encode('utf-8'), AES.MODE_EAX)
        file3 = open(caminho3, "rb")
        nonce = file3.read(16)
        ciphertext = file3.read()
        file3.close()

        try:
            chave = cipher.decrypt_and_verify(ciphertext[:-16], ciphertext[-16:])
        except ValueError:
            print("PIN incorreto.")
            return

    else:
        chavea = open(caminho3, "r")
        chave = chavea.read()
        chavea.close()

    cipher = AES.new(chave, AES.MODE_EAX, nonce=nonce)
    file2 = open(caminho1, "rb")
    nonce = file2.read(16)
    ciphertext = file2.read()
    tag = file2.read()
    file2.close()

    try:
        texto = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        print("A chave utilizada é inválida.")
        return

    file1 = open(caminho2, "w")
    file1.write(texto.decode('utf-8'))
    file1.close()

    calcularHmac(chave.decode('utf-8'), nomef + str(".txt"))

    if os.path.exists(caminho1):
        os.remove(caminho1)
    if os.path.exists(caminho3):
        os.remove(caminho3)

def encriptarSalsa20(nomef):
    global PinSet
    global PIN

    chave = gerarChave()
    guardarChave(chave, nomef)

    caminho1 = existe(".txt", "Texto", nomef)
    caminho2 = existe(".salsa", "Cifrado", nomef)
    file1 = open(caminho1, "r")
    texto = file1.read()
    file1.close()

    cipher = Salsa20.new(key=chave.encode('utf-8'))
    ciphertext = cipher.encrypt(texto.encode('utf-8'))

    file2 = open(caminho2, "wb")
    file2.write(ciphertext)
    file2.close()

    if PinSet:
        caminho3 = existe(".key", "Cifrado", nomef)
        cipher2 = Salsa20.new(key=PIN.encode('utf-8'))
        ciphertext2 = cipher2.encrypt(chave.encode('utf-8'))

        file3 = open(caminho3, "wb")
        file3.write(ciphertext2)
        file3.close()

    calcularHmac(chave, nomef + str(".txt"))

    if os.path.exists(caminho1):
        os.remove(caminho1)

def desencriptarSalsa20(nomef):
    global PinSet
    global PIN

    caminho1 = existe(".salsa", "Cifrado", nomef)
    caminho2 = existe(".txt", "Texto", nomef)
    caminho3 = existe(".key", "Cifrado", nomef)

    if PinSet and os.path.exists(caminho3):
        cipher2 = Salsa20.new(key=PIN.encode('utf-8'))
        file3 = open(caminho3, "rb")
        ciphertext2 = file3.read()
        file3.close()

        try:
            chave = cipher2.decrypt(ciphertext2)
        except ValueError:
            print("PIN incorreto.")
            return

    else:
        chavea = open(caminho3, "r")
        chave = chavea.read()
        chavea.close()

    cipher = Salsa20.new(key=chave.encode('utf-8'))
    file2 = open(caminho1, "rb")
    ciphertext = file2.read()
    file2.close()

    texto = cipher.decrypt(ciphertext)

    file1 = open(caminho2, "w")
    file1.write(texto.decode('utf-8'))
    file1.close()

    calcularHmac(chave, nomef + str(".txt"))

    if os.path.exists(caminho1):
        os.remove(caminho1)
    if os.path.exists(caminho3):
        os.remove(caminho3)

def alterarPIN():
    global PinSet
    global PIN

    if PinSet:
        pinatual = str(input('Introduza o PIN atual:'))
        if pinatual == PIN:
            pinnew = str(input('Introduza o novo PIN:'))
            PIN = pinnew
            print("PIN alterado com sucesso!")
        else:
            print("PIN incorreto.")
    else:
        pinnew = str(input('Introduza o novo PIN:'))
        PIN = pinnew
        PinSet = True
        print("PIN definido com sucesso!")

def iniciar():
    global Iniciado
    global PIN

    print("Bem-vindo ao Fall Into Oblivion")
    print("-----------------------------")
    print("Para começar, defina o diretório onde serão guardados os ficheiros.")
    print("Caso não exista, será criado um novo diretório com o nome 'FALL-INTO-OBLIVION'.")
    print("-----------------------------")

    while not Iniciado:
        global Pasta
        Pasta = str(input('Introduza o diretório de destino:'))
        if not os.path.exists(Pasta):
            os.makedirs(Pasta)
            Iniciado = True
            print("Diretório criado com sucesso!")
        else:
            print("Diretório já existe!")

    print("-----------------------------")
    print("Agora, defina o PIN para proteger os ficheiros.")
    print("Este PIN será utilizado para encriptar e desencriptar as chaves das cifras.")
    print("-----------------------------")
    pin = str(input('Introduza o PIN:'))
    PIN = pin
    PinSet = True
    print("PIN definido com sucesso!")
    print("-----------------------------")

def menu():
    print("-----------------------------")
    print("Escolha uma opção:")
    print("1. Encriptar ficheiro")
    print("2. Desencriptar ficheiro")
    print("3. Verificar integridade do ficheiro")
    print("4. Alterar PIN")
    print("5. Sair")
    print("-----------------------------")

def opcao():
    opcao = int(input())
    if opcao == 1:
        encriptar()
    elif opcao == 2:
        desencriptar()
    elif opcao == 3:
        islegit()
    elif opcao == 4:
        alterarPIN()
    elif opcao == 5:
        exit()

def encriptar():
    print("-----------------------------")
    nomef = str(input('Nome do ficheiro a encriptar:'))
    global Cifra
    if Cifra == 1:
        encriptarAES(nomef)
    elif Cifra == 2:
        encriptarSalsa20(nomef)
    else:
        print("Selecione uma cifra válida.")
        return

    print("Ficheiro encriptado com sucesso!")
    print("-----------------------------")

def desencriptar():
    print("-----------------------------")
    nomef = str(input('Nome do ficheiro a desencriptar:'))
    global Cifra
    if Cifra == 1:
        desencriptarAES(nomef)
    elif Cifra == 2:
        desencriptarSalsa20(nomef)
    else:
        print("Selecione uma cifra válida.")
        return

    print("Ficheiro desencriptado com sucesso!")
    print("-----------------------------")

# Função principal
def main():
    iniciar()

    while True:
        menu()
        opcao()

# Executar a função principal
if _name_ == '_main_':
    main()