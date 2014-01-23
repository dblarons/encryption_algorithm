import numpy, random, json

KEY_STRENGTH = 1000000 # Upper end of range for private keys (don't make more than 10000000000)
MATRIX_SIZE = 15
HILL_STRENGTH = 40
MIN_KEY_STRENGTH = 500 # Number of prime numbers in

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

    def create_private_key(self, n, beginning):
        primes = self.generate_prime_number(n)
        key = primes[random.randint(beginning, (len(primes) - 1))]
        return key

    def new_private_key_pair(self):
        self.p = self.create_private_key(KEY_STRENGTH, MIN_KEY_STRENGTH)
        self.q = self.create_private_key(KEY_STRENGTH, MIN_KEY_STRENGTH)
        print str(self.p)
        while self.q == self.p:
            self.q = self.create_private_key(KEY_STRENGTH, MIN_KEY_STRENGTH)

    def store_private_key(self, filepath):
        if not self.p or not self.q:
            self.new_private_key_pair()
        a = [str(self.p), str(self.q)]
        with open(filepath, 'w+') as f:
            f.write('.'.join(a))

    def retrieve_stored_key(self, filepath):
        with open(filepath, 'r') as f:
            keychain = f.read()
        self.p = int(keychain.partition(".")[0])
        self.q = int(keychain.partition(".")[2])


''' PublicKey 

    PublicKey is initialized with a private key pair and generates a public
    key from that private key pair. It includes methods for storing and 
    retrieving keys. n and e are the public key pair

'''
class PublicKey(object):
    def __init__(self):
        pass

    # n = p * q
    def generate_n(self, p, q):
        self.n = p * q

    def generate_e(self, p, q):
        private_key = PrivateKey()
        e = private_key.create_private_key(100, 3)
        phi_n = generate_phi_n(p, q)
        while phi_n % e == 0:
            e = private_key.create_private_key(100, 3)
        self.e = long(e)

    def new_public_key_pair(self, p, q):
        self.generate_n(p, q)
        self.generate_e(p, q)

    # stores public key in the format n.e
    def store_public_key(self, filepath):
        if not self.n or not self.e:
            raise NameError('Public key pair not generated. Please use new_public_key_pair.')
        a = [str(self.n), str(self.e)]
        with open(filepath, 'w+') as f:
            f.write('.'.join(a))

    def retrieve_stored_key(self, filepath):
        with open(filepath, 'r') as f:
            keychain = f.read()
        self.n = int(keychain.partition(".")[0])
        self.e = int(keychain.partition(".")[2])

class EncryptMessage(object):

    def __init__(self, n, e, filepath, matrix_size=MATRIX_SIZE):
        self.n = n
        self.e = e

        with open(filepath, 'r') as f:
            contents = f.read()
        self.message = contents

        self.matrix_size = matrix_size

        self.main()

    def main(self):
        number_text = self.numbers_for_letters()
        sizes = self.determine_matrix_sizes()
        number_of_matrices = self.number_of_matrices(sizes[0])
        cipher_one = self.generate_hill_cipher_one(sizes[0])
        cipher_two = self.generate_hill_cipher_two(sizes[1])
        encrypted_array = self.encrypt_plain_text(number_text, cipher_one, [], number_of_matrices)
        cipher_text = self.encrypt_plain_text(number_text, cipher_two, encrypted_array, 1)
        encrypted_cipher_one = self.encrypt_cipher_with_public_key(cipher_one, self.n, self.e)
        encrypted_cipher_two = self.encrypt_cipher_with_public_key(cipher_two, self.n, self.e)
        encrypted_message_array = self.encrypt_message_with_public_key(cipher_text, self.n, self.e)
        self.encrypted_message = self.create_encrypted_string(sizes[0], sizes[1], encrypted_cipher_one, encrypted_cipher_two, encrypted_message_array)

    def generate_hill_cipher_one(self, size):
        matrix = numpy.eye(size)
        min_moves = size - 1
        for i in range(min_moves):
            matrix[i + 1] = matrix[i + 1] + matrix[i]
        for i in range(min_moves):
            matrix[min_moves - i - 1] = matrix[min_moves - i] + matrix[min_moves - i - 1]
        for i in range(HILL_STRENGTH):
            a = random.randint(0, size - 1)
            b = random.randint(0, size - 1)
            while b == a:
                b = random.randint(0, size - 1)
            matrix[a] = matrix[a] + matrix[b]
        return matrix

    def generate_hill_cipher_two(self, size):
        if size == 0:
            return [[0]]
        return self.generate_hill_cipher_one(size)

    # returns (first_matrix_size, second_matrix_size)
    def determine_matrix_sizes(self):
        text_length = len(self.message)
        if text_length < self.matrix_size:  # Not enough to make one full-size matrix
            return text_length, 0
        elif text_length % self.matrix_size == 1:
            if text_length / self.matrix_size == 1:  # ex/ size = 10, length = 11, so one 11x11 matrix
                return self.matrix_size + 1, 0
            else:                        # ex/ size = 10, length = 21
                return self.matrix_size, self.matrix_size + 1
        else:
            return self.matrix_size, text_length % self.matrix_size # ex output/ (10, 4)

    def number_of_matrices(self, size):
        text_length = len(self.message)
        if text_length % size == 1:  # ex/ 10 matrices for text_length = 100
            return text_length / size - 1
        else:
            return text_length / size

    # Use 87 character alphabet to convert each letter into a number
    def numbers_for_letters(self):
        alphabet = get_alphabet()
        message_in_numbers = []
        for i in range(len(self.message)):
            if self.message[i] in alphabet:
                number = alphabet.index(self.message[i])
                message_in_numbers.append(number)
            else:
                # Character is unrecognized; assign default
                message_in_numbers.append(86)
        return message_in_numbers

    def encrypt_plain_text(self, number_text, cipher, encrypted_message_array, loops):
        cipher_size = len(cipher[0])
        try:
            for i in range(loops):
                message_chunk = []
                for j in range(cipher_size):
                    message_chunk.append(number_text.pop(0))
                encrypted = numpy.dot(message_chunk, cipher)
                for i in range(len(encrypted)):
                    encrypted_message_array.append(encrypted[i])
        except IndexError:
            pass
        return encrypted_message_array

    def convert_to_95imal(self, number):
        string = ""
        alphabet = get_alphabet()
        if number == 0:
            return alphabet[0]
        while number != 0:
            new_number = number % 95
            number = number / 95
            string = alphabet[new_number] + string
        return string

    def encrypt_cipher_with_public_key(self, cipher, n, e):
        size = len(cipher[0])
        if not cipher[0][0] == 0:
            pk_encrypted_cipher = []
            for i in range(size):
                row = cipher[i] # for each row
                for j in range(size):
                    m = long(row[j]) # for each entry in each row
                    c = pow(m, e, n)
                    c = self.convert_to_95imal(c)
                    pk_encrypted_cipher.append(c)
            return pk_encrypted_cipher
        else:
            return []

    def encrypt_message_with_public_key(self, message, n, e):
        pk_encrypted_message = []
        for i in range(len(message)):
            m = long(message[i])
            c = pow(m, e, n)
            c = self.convert_to_95imal(c)
            pk_encrypted_message.append(c)
        return pk_encrypted_message

    def matrix_to_string(self, send_file, size, cipher):
        for i in range(size):
            send_file = send_file + str(cipher[i]) + " "
        return send_file

    def create_encrypted_string(self, size_one, size_two, cipher_one, cipher_two, message):
        alphabet = get_alphabet()
        send_file = str(alphabet[size_one]) + " " + str(alphabet[size_two]) + " "
        send_file = self.matrix_to_string(send_file, len(cipher_one), cipher_one)
        send_file = self.matrix_to_string(send_file, len(cipher_two), cipher_two)
        for i in range(len(message)):
            send_file += str(message[i]) + " "
        send_file = send_file[:(len(send_file) - 1)]
        return send_file

    def write(self, output_file):
        if not self.encrypted_message:
            raise NameError('encrypted_message not present')
        with open(output_file, 'w') as f:
            f.write(self.encrypted_message)


class DecryptMessage(object):
    def __init__(self, p, q, e, textfile):
        self.p = p
        self.q = q
        self.e = e
        self.n = p * q

        with open(textfile, 'r') as f:
            contents = f.read()
        self.encrypted_message = contents

        self.main()

    def main(self):
        matrices = self.separate_matrix_from_message() # (matrix1, matrix2, message, size1, size2)
        phi_n = generate_phi_n(self.p, self.q)
        d = self.generate_d(phi_n)
        matrix1 = self.decrypt_cipher(d, self.n, matrices[0], matrices[3])
        matrix2 = self.decrypt_cipher(d, self.n, matrices[1], matrices[4])
        imatrix1 = self.invert_cipher(matrix1)
        imatrix2 = self.invert_cipher(matrix2)
        decrypted_message = self.decrypt_pk_message(d, self.n, matrices[2])
        loops = self.loops(decrypted_message, len(imatrix1))
        message = self.decrypt_hill_cipher(imatrix1, decrypted_message, loops, [])
        decrypted_hill_cipher = self.decrypt_hill_cipher(imatrix2, decrypted_message, 1, message)
        self.message_to_plain_text(decrypted_hill_cipher)

    def separate_matrix_from_message(self):
        encrypted_array = self.encrypted_message.split(" ")
        size_one = encrypted_array.pop(0)
        size_one = self.convert_from_95imal(size_one)
        size_two = encrypted_array.pop(0)
        size_two = self.convert_from_95imal(size_two)
        matrix_length_one = size_one ** 2
        matrix_length_two = size_two ** 2
        matrix_one = []
        for i in range(matrix_length_one):
            entry = self.convert_from_95imal(encrypted_array.pop(0))
            matrix_one.append(entry)
        matrix_two = []
        for i in range(matrix_length_two):
            entry = self.convert_from_95imal(encrypted_array.pop(0))
            matrix_two.append(entry)
        message = encrypted_array
        return matrix_one, matrix_two, message, size_one, size_two

    def convert_from_95imal(self, number):
        alphabet = get_alphabet()
        length = len(number)
        new_number = 0
        for i in range(length):
            digit = number[length - i - 1]
            index = alphabet.index(digit)
            new_number += index * 95 ** i
        return new_number

    def generate_d(self, phi_n):
        a = 1
        while (a * phi_n + 1) % self.e != 0:
            a += 1
        d = (a * phi_n + 1) / self.e
        return d

    def decrypt_cipher(self, d, n, encrypted_cipher, size): # Cipher is c in the formula
        unencrypted_cipher = []
        for i in range(len(encrypted_cipher)):
            c = pow(encrypted_cipher[i], d, n)
            unencrypted_cipher.append(c)
        matrix = []
        for i in range(size):
            matrix1 = []
            for j in range(size):
                matrix1.append(unencrypted_cipher.pop(0))
            matrix.append(matrix1)
        return matrix

    def invert_cipher(self, unencrypted_cipher):
        if len(unencrypted_cipher) != 0:
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
            encrypted_number = self.convert_from_95imal(message[i])
            decrypted_message.append(pow(encrypted_number, d, n))
        return decrypted_message

    def loops(self, decrypted_message, size):
        loops = 0
        if len(decrypted_message) % size == 1:
            loops = len(decrypted_message) / size - 1
        else:
            loops = len(decrypted_message) / size
        return loops

    def decrypt_hill_cipher(self, inverted_matrix, decrypted_message, loops, message):
        size = len(inverted_matrix)

        if size == 1: # return now if there is not a second matrix
            return message

        for i in range(loops):
            encrypted = []
            for j in range(size):
                encrypted.append(decrypted_message.pop(0))
            unencrypted = numpy.dot(encrypted, inverted_matrix) # unencrypt this portion of the message
            unencrypted = numpy.array(unencrypted)
            for j in range(size):
                message.append(unencrypted[j])
        return message

    def message_to_plain_text(self, message):
        alphabet = get_alphabet()
        plain_text = ""
        for i in range(len(message)):
            plain_text = plain_text + alphabet[(int(message[i]) % len(get_alphabet()))]
        self.decrypted_message = plain_text

    def write(self, output_file):
        if not self.decrypted_message:
            raise NameError('decrypted_message not present')
        with open(output_file, 'w') as f:
            f.write(self.decrypted_message)

# Helper methods

# phi(n) = (p - 1) * (q - 1)
def generate_phi_n(p, q):
    phi_n = (p - 1) * (q - 1)
    return phi_n

# Get the supported alphabet from its json file and make into array
def get_alphabet():
    with open('alphabet.json', 'r') as f:
        alphabet = json.loads(f.read())
    return alphabet
