from Crypto.Cipher import AES
import string, base64


class AESCipher(object):
    
    def __init__(self, key=b'BLhgpCL81fdLBk23HkZp8BgbT913cqt0',iv=b'OWFJATh1Zowac2xr'):
        self.key = key
        self.iv = iv

    def encrypt(self, raw):
        if isinstance(raw, str): # convert string to bytes
            raw = raw.encode('utf-8') 
        self.cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        ciphertext = self.cipher.encrypt(raw)
        
        encoded = base64.b64encode(ciphertext)
        return encoded.decode('utf-8')

    def decrypt(self, raw):
        decoded = base64.b64decode(raw)
        self.cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        decrypted = self.cipher.decrypt(decoded)
        
        return str(decrypted, 'utf-8')
