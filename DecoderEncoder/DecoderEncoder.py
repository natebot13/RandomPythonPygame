import time

def isNumber(input):
	try:
		int(input)
		return True
	except:
		return False

class Decode():
	def __init__(self):
		decodeThis = ""
		decodeWith = ""
		decoded = ""
		while True:
			print """
Text to Decode: %s
Decoding type: %s
Decoded text: %s

1. Enter text
2. Enter decoding type
3. Decode!
4. Quit"""%(decodeThis, decodeWith, decoded)
			choice = raw_input(">>> ")
			if isNumber(choice):
				choice = int(choice)
				if choice == 1:
					decodeThis = self.get_decode_text()
				if choice == 2:
					decodeWith = self.get_decode_type()
				if choice == 3:
					if decodeWith == "custom":
						decoded = customCypher(decodeThis)
					else:
						try:
							decoded = decodeThis.decode(decodeWith)
						except:
							decoded =  "The entered decoding type is not valid"
				if choice == 4:
					break
	
	def get_decode_type(self):
		print "What is your decoding type?"
		return raw_input(">>> ")
	
	def get_decode_text(self):
		print "Enter your text to be decoded."
		return raw_input(">>> ")

class Encode():
	def __init__(self):
		encodeThis = ""
		encodeWith = ""
		encoded = ""
		while True:
			print """
Text to Encode: %s
Encoding type: %s
Encoded text: %s

1. Enter text
2. Enter encoding type
3. Encode!
4. Quit"""%(encodeThis, encodeWith, encoded)
			choice = raw_input(">>> ")
			if isNumber(choice):
				choice = int(choice)
				if choice == 1:
					encodeThis = self.get_encode_text()
				if choice == 2:
					encodeWith = self.get_encode_type()
				if choice == 3:
					if encodeWith == "custom":
						encoded = customCypher(encodeThis)
					else:
						try:
							encoded = encodeThis.encode(encodeWith)
						except:
							encoded =  "The entered encoding type is not valid"
				if choice == 4:
					break
	
	def get_encode_type(self):
		print "What is your encoding type?"
		return raw_input(">>> ")
	
	def get_encode_text(self):
		print "Enter your text to be encoded."
		return raw_input(">>> ")

def customCypher(text, encode=True):
	alphabet = list("abcdefghijklmnopqrstuvwxyz")
	entered = raw_input("""
Enter your cipher encryption
ABCDEFGHIJKLMNOPQRSTUVWXYZ
""")

print "Welcome to the Python decoder program\nfor decoding and encoding any text according to certain cypher algorythms."
time.sleep(1)

while True:
	print "What would you like to do?"
	print """
1. Decode
2. Encode
3. Quit"""
	choice = raw_input(">>> ")
	if isNumber(choice):
		choice = int(choice)
		if choice == 3:
			break
		if choice > 3:
			print "That is not an option."
		if choice == 1:
			Decode()
		if choice == 2:
			Encode()
	else:
		print "Please enter a number."
