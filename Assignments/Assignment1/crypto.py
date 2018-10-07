from Crypto.Cipher import AES

class AES_Encrypt(): 

  def __init__(self):
    self.salt = '!%F=-?Pst970'
    self.key = "{: <32}".format(self.salt).encode()
    self.cipher=AES.new(self.key, AES.MODE_ECB)

  def pad(self, text):
    return text+((16-len(text)%16)*'{')

  def encrypt(self, plaintext):
    return self.cipher.encrypt((self.pad(plaintext).encode()))


  def decrypt(self, ciphertext):
    dec=self.cipher.decrypt(ciphertext).decode()
    l=dec.count('{')
    return dec[:len(dec)-l]


'''
if __name__ == '__main__':
  e = AES_Encrypt()
  print(e.decrypt(e.encrypt('Surya')))
'''
