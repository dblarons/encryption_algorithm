import numpy, random

class GeneratePrivateKey(object):

    def __init__(self):
        pass

    def generate_prime_number(self, n):
        # http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
        """ Input n>=6, Returns a array of primes, 2 <= p < n """
        sieve = numpy.ones(n/3 + (n%6==2), dtype=numpy.bool)
        sieve[0] = False
        for i in xrange(int(n**0.5)/3+1):
            if sieve[i]:
                k=3*i+1|1
                sieve[      ((k*k)/3)      ::2*k] = False
                sieve[(k*k+4*k-2*k*(i&1))/3::2*k] = False
        return numpy.r_[2,3,((3*numpy.nonzero(sieve)[0]+1)|1)]

    def create_private_key(self):
        prime_to_million = self.generate_prime_number(1000000)
        prime_to_thousand = self.generate_prime_number(1000)
        thousand_length = len(prime_to_thousand)
        private_keys = prime_to_million[thousand_length:] # Removes prime numbers < 1000
        random_int = random.randint(0, len(private_keys))
        key = private_keys[random_int]
        return key

    def get_private_key(self):
        p = self.create_private_key()
        q = self.create_private_key()
        while q == p:
            q = self.create_private_key()
        return long(p), long(q) # Return as long so they can be multiplied

    def store_private_key(self, p, q):
        f = open("private_key.key", "w")
        f.write(', '.join(str(p), str(q)))
        f.close()

class GeneratePublicKey(object):
    def __init__(self, p, q):
        self.p = p
        self.q = q

    # n = p * q
    def generate_n(self):
        n = self.p * self.q
        return n

    def generate_e(self):
        private_key = GeneratePrivateKey()
        prime_generator = private_key.create_private_key()
        e = prime_generator
        phi_n = generate_phi_n(self.p, self.q)
        while phi_n % e == 0:
            e = prime_generator
        return long(e)

    def get_public_key(self):
        return self.generate_n(), self.generate_e()

    def store_public_key(self, n, e):
        f = open("public_key.txt", "w")
        f.write(', '.join(str(n), str(e)))
        f.close()

class EncryptMessage(object):

    def __init__(self, public_key):
        self.public_key = public_key

    def generate_hill_cipher_one(self, size):
        matrix = np.eye(size)
        for i in range(100):
            a = random.randint(0, size)
            b = random.randint(0, size)
            c = random.randint(1, 101)
            while b == a:
                b = random.randint(0, size)
            matrix[a] += c * matrix[b]
        return matrix

    def generate_hill_cipher_two(self, size):
        if size == 0:
            return none
        matrix = np.eye(size)      
        for i in range(100):
            a = random.randint(0, size)
            b = random.randint(0, size)
            c = random.randint(1, 101)
            while b == a:
                b = random.randint(0, size)
            matrix[a] += c * matrix[b]
        return matrix

    def read_plain_text(self, file):
        f = open(file, "r")
        return f.read()
        f.close()

    def determine_matrix_sizes(self, text_length, size):
        pass
        if text_length / size == 0:  # Not enough to make one full-size matrix
            return text_length, 0
        elif text_length % size == 0:  # One matrix fits all
            return size, 0
        elif text_length % size == 1:
            if text_length / size == 1:  # ex/ size = 10, length = 11, so one 11x11 matrix
                return size + 1, 0
            else:                        # ex/ size = 10, length = 21
                return size, size + 1
        else:
            return size, text_length % size # ex output/ (10, 4)

    def number_of_matrices(self, text_length, size):
        if text_length % size == 0 or text_length % size == 1:  # ex/ 10 matrices for text_length = 100
            return text_length / size
        else:
            return text_length / size + 1

    def encrypt_plain_text(self, plain_text, cipher):
        size = len(cipher[0])
        loops = len(plain_text) / size
        encrypted_message = []
        for i in range(loops):
            array = plain_text.pop(0, size)
            encrypted_message.append(dot(array, cipher))
        return encrypted_message

    def encrypt_cipher_with_public_key(self, cipher, n, e):
        pk_encrypted_cipher = []
        for i in len(cipher[0]):
            m = long(cipher[i])
            c = (m ** e) % n
            pk_encrypted_cipher.append(c)
        return pk_encrypted_cipher

    def encrypt_message_with_public_key(self, message, n, e):
        pk_encrypted_message = []
        for i in len(message):
            m = long(message[i])
            c = m ** e % n
            pk_encrypted_message.append(c)
        return pk_encrypted_message

    def matrix_to_string(self, send_file, size, cipher):
        for i in range(size):
            array = cipher[i]
            for j in range(size):
                send_file = send_file + str(array[j]) + "."
        return send_file

    def create_encrypted_string(self, size_one, size_two, cipher_one, cipher_two, message):
        send_file = str(size_one) + str(size_two) + "."
        send_file = self.matrix_to_string(send_file, size_one, cipher_one)
        send_file = self.matrix_to_string(send_file, size_two, cipher_two)
        for i in range(len(message)):
            send_file = send_file + str(message[i]) + "."
        return send_file

    def output_encrypted_message(self, encrypted_string):
        f = open("encrypted_message.txt", "w")
        f.write(encrypted_string)
        f.close()

if __name__ == '__main__':
    b = GeneratePrivateKey()
    p = b.get_private_key()[0]
    q = b.get_private_key()[1]
    a = GeneratePublicKey(p, q)
    c = a.get_public_key()
    print c

class DecryptMessage(object):
    def __init__(self, textfile, private_key):
        self.textfile = textfile
        self.private_key = private_key # this should be an array

    def read_encrypted_text(self, encrypted_text):
        f = open(encrypted_text, "r")
        return f.read()
        f.close()

    def separate_matrix_from_message(self, encrypted_message):
        encrypted_array = encrypted_message.split(".")
        size_one = int(encrypted_array.pop(0))
        size_two = int(encrypted_array.pop(1))
        matrix_length_one = size_one ** 2
        matrix_length_two = size_two ** 2
        matrix_one = []
        for i in range(matrix_length_one):
            matrix_one = encrypted_array.pop(i)
        matrix_two = []
        for i in range(matrix_length_two):
            matrix_two = encrypted_array.pop(i)
        message = encrypted_array
        return matrix_one, matrix_two, message

    def generate_d(self, e, phi_n):
        a = 1
        while (a * phi_n + 1) % e != 0:
            a += 1
        d = (a * phi_n + 1) / e
        return d

    def decrypt_cipher(self, d, n, encrypted_cipher): # Cipher is c in the formula
        unencrypted_cipher = (encrypted_cipher ** d) % n
        return unencrypted_cipher

    def convert_cipher_to_inverted_matrix(self, unencrypted_cipher):
        cipher = unencrypted_cipher
        return matrix(cipher).I

    def decrypt_pk_message(self, d, n, message):
        decrypted_message = []
        for i in range(len(message)):
            decrypted_message.append(message[i] ** d % n)
        return decrypted_message

    def decrypt_hill_cipher(self, inverted_matrix, decrypted_message):
        size = len(inverted_matrix[0])
        message = ""
        loops = len(decrypted_message) / size
        for i in range(loops):
            array = dot(decrypted_message[i], inverted_matrix)
            for j in range(size):
                message = message + str(array[j])
        return message

    def output_plain_text_message(self, message1, message2):
        message = message1 + message2
        f = open("decrypted_message.txt", "w")
        f.write(message)
        f.close()

# Helper methods

# phi(n) = (p - 1) * (q - 1)
def generate_phi_n(p, q):
    phi_n = (p - 1) * (q - 1)
    return phi_n