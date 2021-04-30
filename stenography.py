from PIL import Image, ImageDraw 
from random import randint	
from re import findall
	
ALPHABET = ('abcdefghijklmnopqrstuvwxyz')

def encryption_caesar(msg, offset):
    encrypted_alphabet = ALPHABET[offset:] + ALPHABET[:offset]
    encrypted = []
    for char in msg:
        index = get_char_index(char, ALPHABET)
        encrypted_char = encrypted_alphabet[index] if index >= 0 else char
        encrypted.append(encrypted_char)
    return ''.join(encrypted)

def get_char_index(char, alphabet):
    char_index = alphabet.find(char)
    return char_index

def decryption_caesar(msg, offset=3):
    encrypted_alphabet = ALPHABET[offset:] + ALPHABET[:offset]
    decrypted = []
    if offset:
        # Если известно смещение, просто дешифруем сообщение по обратно
        for char in msg:
            index = get_char_index(char, encrypted_alphabet)
            encrypted_char = encrypted_alphabet[index - offset] \
                if index >= 0 else char
            decrypted.append(encrypted_char)
        return ''.join(decrypted)
    return 'Не удалось расшифровать сообщение %s' % msg

def stega_encrypt():
	keys = [] 					#сюда будут помещены ключи
	img = Image.open(input("path to image: ")) 	#создаём объект изображения
	draw = ImageDraw.Draw(img)	   		#объект рисования
	width = img.size[0]  		   		#ширина
	height = img.size[1]		   		#высота	
	pix = img.load()				#все пиксели тут
	f = open('keys.txt','w')			#текстовый файл для ключей

	for elem in ([ord(elem) for elem in encryption_caesar(str(input("text here: ")),3)]):
		key = (randint(1,width-10),randint(1,height-10))		
		g, b = pix[key][1:3]
		draw.point(key, (elem,g , b))														
		f.write(str(key)+'\n')		
						
	print('keys were written to the keys.txt file')
	img.save("newimage.png", "PNG")
	f.close()

def stega_decrypt():
	a = []						    
	keys = []
	img = Image.open(input("path to image: "))				
	pix = img.load()
	f = open(input('path to keys: '),'r')
	y = str([line.strip() for line in f])				
															
	for i in range(len(findall(r'\((\d+)\,',y))):
		keys.append((int(findall(r'\((\d+)\,',y)[i]),int(findall(r'\,\s(\d+)\)',y)[i]))) 	
	for key in keys:
		a.append(pix[tuple(key)][0])							
	return ''.join([chr(elem) for elem in a])


a = input("path to: 1-encrypt, 2-decrypte\n")
if(a=="1"):
    stega_encrypt()
if(a=="2"):
    print("you message: ",decryption_caesar(stega_decrypt()))
if(a=="3"):
    message = str(input("text here: "))
    shift = int(input("Сдвиг: "))  # Смещение алфавита
    encrypted_message = encryption_caesar(message, shift)
    print('Сообщение: %s' % message)
    print('Зашифрованное сообщение: %s' % encrypted_message)
    print('Расшифрованное сообщение: %s' % decryption_caesar(encrypted_message,shift))
 