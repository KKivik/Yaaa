import os
import sys
from cryptography.fernet import Fernet
import sqlite3
import os, ipaddress
import socket


class No_Flash_Drive(Exception):
	pass

class No_Key_On_Flash(Exception):
	pass

class Decoder:
	def __init__(self, path_to_decode, bool): # bool если True значит шифруем, если False, то расшифровываем
		self.drive_letter = "F"  # имя буквы внешнего накопителя
		if self.check_drive():
			self.con = sqlite3.connect("F:/db.sqlite")
			self.cur = self.con.cursor()
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.s.connect(("8.8.8.8", 80))  # любой внешний адрес
			self.ip = self.s.getsockname()[0]
			if bool:
				self.encrypted_path = path_to_decode #"C:/Data" #что шифровать?

				# if os.path.isfile(self.drive_letter + ":/db.sqlite") == False:
				# 	self.write_key()

				self.key = self.load_key()
				self.walk(self.encrypted_path)
			else:
				#РАСШИФРОВЫВАЕМ
				self.encrypted_path = path_to_decode  # "C:/Data" #что шифровать?

				if self.load_key_decode() == None:
					raise No_Key_On_Flash

				self.walk_to_decode(self.encrypted_path)
		else:
			raise No_Flash_Drive

	def check_drive(self): #эта функция проверяет вставлен ли вообще флеш-накопитель
		if os.system("cd " + self.drive_letter + ":") == 0: #если там что-то есть
			return True
		else:
			return False

	def write_key(self):
		key = Fernet.generate_key()
		self.cur.execute("""INSERT INTO keys VALUES (?, ?);""", (self.ip, key))

	def load_key(self):
		# self.ip - ipшник
		key = self.cur.execute("""SELECT key from keys where ip = ?""", (self.ip, )).fetchone()
		if key == None:
			self.write_key()
			key = self.cur.execute("""SELECT key from keys where ip = ?""", (self.ip,)).fetchone()
		return key[0]
		# with open(self.drive_letter + ":/key.txt", "r") as file:
		# 	key = file.read()

		# return key

	def load_key_decode(self):
		# self.ip - ipшник
		key = self.cur.execute("""SELECT key from keys where ip = ?""", (self.ip, )).fetchone()
		if key == None:
			return None
		return key[0]
		# with open(self.drive_letter + ":/key.txt", "r") as file:
		# 	key = file.read()

		# return key

	def encrypt(self, filename, key): # Шифрование файла
		fernet = Fernet(key)

		with open(filename, "rb") as file:
			file_data = file.read()

			encrypted_data = fernet.encrypt(file_data)

			with open(filename, "wb") as file:
				file.write(encrypted_data)

	def decrypt(self, filename, key): # Расшифровка файла
		fernet = Fernet(key)

		with open(filename, "rb") as file:
			file_data = file.read()

		decrypted_data = fernet.decrypt(file_data)

		with open(filename, "wb") as file:
			file.write(decrypted_data)


	def walk(self, temp_path): #Бегает по директории и шифрует файлs
		names = os.listdir(temp_path)
		#print(names)

		for name in names:
			path = os.path.join(temp_path, name)
			ext = os.path.splitext(path)

			if os.path.isfile(path):
				self.encrypt(path, self.key)
			else:
				self.walk(path)

	def walk_to_decode(self, temp_path):
		names = os.listdir(temp_path)
		key = self.load_key()

		for name in names:
			path = os.path.join(temp_path, name)
			ext = os.path.splitext(path)

			if os.path.isfile(path):
				self.decrypt(path, key)
			else:
				self.walk_to_decode(path)



