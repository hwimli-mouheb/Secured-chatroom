import rsa


class HelperRsa:

    #encryption + decryption
    @staticmethod
    def encrypt(data, key):
        return rsa.encrypt(data.encode('ascii'), key)

    @staticmethod
    def decrypt(data, key):
        try:
            return rsa.decrypt(data, key).decode('ascii')
        except:
            return False

    # Rsa Keys
    @staticmethod
    def get_public_key(key_path):
        try:
            with open(key_path, 'rb') as file:
                pub_key = rsa.PublicKey.load_pkcs1(file.read())
            return pub_key
        except:
            return False

    @staticmethod
    def get_private_key(key_path):
        try:
            with open(key_path, 'rb') as file:
                private_key = rsa.PrivateKey.load_pkcs1(file.read())
            return private_key
        except:
            return False

    @staticmethod
    def generate_keys(public_path='keys/public_key.pem', private_path='keys/private_key.pem'):
        pub_key, private_key = rsa.newkeys(4096)
        with open(public_path, 'wb') as file:
            file.write(pub_key.save_pkcs1('PEM'))

        with open(private_path, 'wb') as file:
            file.write(private_key.save_pkcs1('PEM'))
        print("Generated!")


    @staticmethod
    def sign_sha256(msg, key):
        return rsa.sign(msg.encode('ascii'), key, 'SHA-256')

    @staticmethod
    def verify_sha256(msg: str, signature, key):
        try:
                return rsa.verify(msg.encode('ascii'), signature, key) == 'SHA-256'
        except:
            return False
