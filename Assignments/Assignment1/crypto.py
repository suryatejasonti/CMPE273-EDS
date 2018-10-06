from Crypto.Cipher import AES

class AESEncrypt(): 

  def __init__(self):
    self.salt = '!%F=-?Pst970'
    self.key = "{: <32}".format(self.salt).encode("utf-8")
    self.cipher=AES.new(self.key)

  def pad(self, s):
    return s+((16-len(s)%16)*'{')

  def encrypt(self, plaintext):
    return self.cipher.encrypt(self.pad(plaintext))


  def decrypt(self, ciphertext):
    dec=self.cipher.decrypt(ciphertext).decode('utf-8')
    l=dec.count("{")
    return dec[:len(dec)-l]

