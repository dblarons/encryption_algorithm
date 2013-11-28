import numpy, random, json

''' PrivateKey
    
    PrivateKey takes no parameters for initialization, but p and q instance 
    variables are created on a PrivateKey object when a key is created or 
    retrieved. p and q are the private key pair and can be stored or 
    regenerated.

'''
class PrivateKey(object):

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

    def create_private_key(self, n):
        primes = self.generate_prime_number(n)
        key = primes[random.randint(0, (len(primes) - 1))]
        return key

    def new_private_key_pair(self):
        self.p = self.create_private_key(1000)
        self.q = self.create_private_key(1000)
        while self.q == self.p:
            self.q = self.create_private_key(1000)

    def store_private_key(self, filepath):
        if not self.p or not self.q:
            self.new_private_key_pair()
        a = [str(self.p), str(self.q)]
        f = open(filepath, "w+") # creates a new file if none is found
        f.write('.'.join(a))
        f.close()

    def retrieve_stored_key(self, filepath):
        f = open(filepath, "r")
        keychain = f.read()
        self.p = int(keychain.partition(".")[0])
        self.q = int(keychain.partition(".")[2])
        f.close()


''' PublicKey 

    PublicKey is initialized with a private key pair and generates a public
    key from that private key pair. It includes methods for storing and 
    retrieving keys. n and e are the public key pair

'''
class PublicKey(object):
    def __init__(self, p, q):
        self.p = p
        self.q = q

    # n = p * q
    def generate_n(self):
        self.n = self.p * self.q

    def generate_e(self):
        private_key = PrivateKey()
        e = private_key.create_private_key(100)
        phi_n = generate_phi_n(self.p, self.q)
        while phi_n % e == 0:
            e = private_key.create_private_key(100)
        self.e = long(e)

    def new_public_key_pair(self):
        self.generate_n()
        self.generate_e()

    # stores public key in the format n.e
    def store_public_key(self, filepath):
        if not self.n:
            self.generate_n()
        if not self.e:
            self.generate_e()

        a = [str(self.n), str(self.e)]
        f = open(filepath, 'w+') # creates a new file if none is found
        f.write('.'.join(a))
        f.close()

    def retrieve_stored_key(self, filepath):
        f = open(filepath, "r")
        keychain = f.read()
        self.n = int(keychain.partition(".")[0])
        self.e = int(keychain.partition(".")[2])
        f.close()

class EncryptMessage(object):

    def __init__(self, n, e):
        self.n = n
        self.e = e

    def generate_hill_cipher_one(self, size):
        matrix = numpy.eye(size)
        matrix[0] = matrix[0] * 2
        while numpy.linalg.det(matrix) != 1 and numpy.linalg.det(matrix) != -1:
            matrix = numpy.eye(size)
            for i in range(20):
                a = random.randint(0, size - 1)
                b = random.randint(0, size - 1)
                while b == a:
                    b = random.randint(0, size - 1)
                matrix[a] = matrix[a] + matrix[b]
            if numpy.linalg.det(matrix) == 1 or numpy.linalg.det(matrix) == -1:
                break
        return matrix

    def generate_hill_cipher_two(self, size):
        if size == 0:
            return [[0]]

        matrix = numpy.eye(size)
        matrix[0] = matrix[0] * 2

        # generate new matrices until one is invertible
        while numpy.linalg.det(matrix) != 1.0 and numpy.linalg.det(matrix) != -1.0:
            matrix = numpy.eye(size)
            for i in range(20):
                a = random.randint(0, size - 1)
                b = random.randint(0, size - 1)
                # don't add multiples of one row to itself
                while b == a:
                    b = random.randint(0, size - 1)
                matrix[a] = matrix[a] + matrix[b]

        return matrix

    def read_plain_text(self, file):
        f = open(file, "r")
        return f.read()
        f.close()

    def determine_matrix_sizes(self, text_length, size):
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
        if text_length % size == 1:  # ex/ 10 matrices for text_length = 100
            return text_length / size - 1
        else:
            return text_length / size

    def plain_text_to_number_text(self, plain_text):
        alphabet = get_alphabet()
        number_text = []
        for i in range(len(plain_text)):
            if plain_text[i] in alphabet:
                number = alphabet.index(plain_text[i])
                number_text.append(number)
            else:
                number_text.append(86)
        return number_text

    def encrypt_plain_text(self, number_text, cipher1, cipher2, loops):
        encrypted_message = []
        for i in range(loops):
            array = []
            for j in range(len(cipher1[0])):
                array.append(number_text.pop(0))
            array2 = numpy.dot(array, cipher1)
            for i in range(len(array2)):
                encrypted_message.append(array2[i])
        try:
            cipher2[0][1] # This is what we're 'trying.' If this doesn't exist, it won't work.
            array3 = []
            for i in range(len(number_text)):
                array3.append(number_text.pop(0))
            array4 = numpy.dot(array3, cipher2)
            for i in range(len(array4)):
                encrypted_message.append(array4[i])
        except IndexError:
            pass
        return encrypted_message

    def encrypt_cipher_with_public_key(self, cipher, n, e):
        if not cipher[0][0] == 0:
            pk_encrypted_cipher = []
            for i in range(len(cipher[0])):
                array = cipher[i]
                for j in range(len(cipher[0])):
                    m = long(array[j])
                    c = (m ** e) % n

                    pk_encrypted_cipher.append(c)
            return pk_encrypted_cipher
        else:
            return []

    def encrypt_message_with_public_key(self, message, n, e):
        pk_encrypted_message = []
        for i in range(len(message)):
            m = long(message[i])
            c = m ** e % n
            pk_encrypted_message.append(c)
        return pk_encrypted_message

    def matrix_to_string(self, send_file, size, cipher):
        for i in range(size):
            send_file = send_file + str(cipher[i]) + "."
        return send_file

    def create_encrypted_string(self, size_one, size_two, cipher_one, cipher_two, message):
        send_file = str(size_one) + "." + str(size_two) + "."
        send_file = self.matrix_to_string(send_file, len(cipher_one), cipher_one)
        send_file = self.matrix_to_string(send_file, len(cipher_two), cipher_two)
        for i in range(len(message)):
            send_file += str(message[i]) + "."
        send_file = send_file[:(len(send_file) - 1)]
        return send_file

    def output_encrypted_message(self, encrypted_string):
        f = open("encrypted_message.txt", "w")
        f.write(encrypted_string)
        f.close()



class DecryptMessage(object):
    def __init__(self, textfile, p, q, e):
        self.textfile = textfile
        self.p = p
        self.q = q
        self.e = e
        self.n = p * q

    def read_encrypted_text(self):
        f = open(self.textfile, "r")
        return f.read()
        f.close()

    def separate_matrix_from_message(self, encrypted_message):
        encrypted_array = encrypted_message.split(".")
        size_one = int(encrypted_array.pop(0))
        size_two = int(encrypted_array.pop(0))
        matrix_length_one = size_one ** 2
        matrix_length_two = size_two ** 2
        matrix_one = []
        for i in range(matrix_length_one):
            matrix_one.append(long(encrypted_array.pop(0)))
        matrix_two = []
        for i in range(matrix_length_two):
            matrix_two.append(long(encrypted_array.pop(0)))
        message = encrypted_array
        return matrix_one, matrix_two, message, size_one, size_two

    def generate_d(self, phi_n):
        a = 1
        while (a * phi_n + 1) % self.e != 0:
            a += 1
        d = (a * phi_n + 1) / self.e
        return d

    def decrypt_cipher(self, d, n, encrypted_cipher, size): # Cipher is c in the formula
        unencrypted_cipher = []
        for i in range(len(encrypted_cipher)):
            unencrypted_cipher.append((encrypted_cipher[i] ** d) % n)
        matrix = []
        for i in range(size):
            matrix1 = []
            for j in range(size):
                matrix1.append(unencrypted_cipher.pop(0))
            matrix.append(matrix1)
        return matrix

    def invert_cipher(self, unencrypted_cipher):
        if len(unencrypted_cipher) != 1:
            matrix = numpy.matrix(unencrypted_cipher).I
            for i in range(len(numpy.array(matrix))):
                matrix = numpy.array(matrix)
                for j in range(len(matrix[i])):
                    matrix[i][j] = round(matrix[i][j])
            return matrix
        else:
            return [0]

    def decrypt_pk_message(self, d, n, message):
        decrypted_message = []
        for i in range(len(message)):
            decrypted_message.append(long(message[i]) ** d % n)
        return decrypted_message

    def decrypt_hill_cipher(self, inverted_matrix1, inverted_matrix2, decrypted_message):
        size = len(inverted_matrix1)
        message = []

        # if the second matrix needs to be used, use the first matrix one less time
        if len(inverted_matrix2) > 1:
            loops = len(decrypted_message) / size - 1
        elif len(inverted_matrix2) == 1:
            loops = len(decrypted_message) / size

        for i in range(loops):
            array = []
            for j in range(len(inverted_matrix1)):
                array.append(decrypted_message.pop(0))
            message0 = numpy.dot(array, inverted_matrix1) # unencrypt this portion of the message
            message0 = numpy.array(message0)
            for j in range(size):
                message.append(message0[j])

        # decrypt the "leftovers"
        size = len(inverted_matrix2)
        array1 = []
        for i in range(size):
            array1.append(decrypted_message.pop(0))
        array2 = numpy.dot(array1, inverted_matrix2)
        array2 = numpy.array(array2)
        for i in range(size):
            message.append(array2[i])
        return message

    def message_to_plain_text(self, message):
        alphabet = get_alphabet()
        plain_text = ""
        for i in range(len(message)):
                plain_text = plain_text + alphabet[(int(message[i]) % 89)]
        return plain_text

    def output_plain_text_message(self, message):
        f = open("decrypted_message.txt", "w")
        f.write(message)
        f.close()

# Helper methods

# phi(n) = (p - 1) * (q - 1)
def generate_phi_n(p, q):
    phi_n = (p - 1) * (q - 1)
    return phi_n

# Get the supported alphabet from its json file and make into array
def get_alphabet():
    return json.loads(open('alphabet.json', 'r').read())

if __name__ == '__main__':
    private_key = PrivateKey()
    private_key.new_private_key_pair()
    private_key.store_private_key('private_key.txt')

    public_key = PublicKey(private_key.p, private_key.q)
    public_key.new_public_key_pair()
    public_key.store_public_key('public_key.txt')

    c = EncryptMessage(public_key.n, public_key.e)
    file1 = c.read_plain_text("test.txt")
    number_text = c.plain_text_to_number_text(file1)
    text_length = len(number_text)
    number_of_matrices = c.number_of_matrices(text_length, 5)
    sizes = c.determine_matrix_sizes(len(file1), 5)
    cipher_one = c.generate_hill_cipher_one(sizes[0])
    cipher_two = c.generate_hill_cipher_two(sizes[1])
    cipher_text = c.encrypt_plain_text(number_text, cipher_one, cipher_two, number_of_matrices)
    encrypted_cipher_one = c.encrypt_cipher_with_public_key(cipher_one, public_key.n, public_key.e)
    encrypted_cipher_two = c.encrypt_cipher_with_public_key(cipher_two, public_key.n, public_key.e)
    encrypted_message = c.encrypt_message_with_public_key(cipher_text, public_key.n, public_key.e)
    string = c.create_encrypted_string(sizes[0], sizes[1], encrypted_cipher_one, encrypted_cipher_two, encrypted_message)
    c.output_encrypted_message(string)

    dm = DecryptMessage("encrypted_message.txt", private_key.p, private_key.q, public_key.e)
    encrypted_message = dm.read_encrypted_text()
    matrices = dm.separate_matrix_from_message(encrypted_message) # (matrix1, matrix2, size1, size2)
    phi_n = generate_phi_n(private_key.p, private_key.q)
    d = dm.generate_d(phi_n)
    matrix1 = dm.decrypt_cipher(d, public_key.n, matrices[0], matrices[3])
    matrix2 = dm.decrypt_cipher(d, public_key.n, matrices[1], matrices[4])
    imatrix1 = dm.invert_cipher(matrix1)
    imatrix2 = dm.invert_cipher(matrix2)
    decrypted_message = dm.decrypt_pk_message(d, public_key.n, matrices[2])
    decrypted_hill_cipher = dm.decrypt_hill_cipher(imatrix1, imatrix2, decrypted_message)
    the_message = dm.message_to_plain_text(decrypted_hill_cipher)
    dm.output_plain_text_message(the_message)
