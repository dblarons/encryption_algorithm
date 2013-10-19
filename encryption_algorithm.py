import numpy, random

# TODO: Aaron - store the key in a .key file
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

    # Aaron - Store key in .key file
    def store_private_key(self):
        pass

# TODO: Aaron - store the public key in format (n, e)
class GeneratePublicKey(object):
    def __init__(self, p, q):
        self.p = p
        self.q = q

    # n = p * q
    def generate_n(self):
        n = self.p * self.q
        return n

    # TODO: make create_private_key method public
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

    # TODO: Make text file with key that can be given to message senders

class EncryptMessage(object):

    def __init__(self, public_key):
        self.public_key = public_key

    # For Aaron
    def generate_hill_cipher(self):
        pass
        # return cipher

    # For Aaron
    def read_plain_text(self):
        pass
        # return plain_text

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

    # For Aaron - plain_text and cipher are matrices
    def encrypt_plain_text(self, plain_text, cipher):
        pass
        # return encrypted_message

    def encrypt_cipher_with_public_key(self, cipher, n, e):
        pk_encrypted_cipher = []
        # TODO: handle for matrix objects
        for i in len(cipher):
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

    # For Aaron - 1011__matrix____message__
    def create_encrypted_string(self, matrix_size, cipher, message):
        pass
        # return send_file (need better name)

    # For Aaron - write it to a file or something
    def output_encrypted_message(self):
        pass
        # Output something

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

    # For Aaron
    def read_encrypted_text(self):
        pass
        # return text

    # For Aaron
    def separate_matrix_from_message(self):
        pass
        # return tuple of matrix and message

    def generate_d(self, e, phi_n):
        a = 1
        while (a * phi_n + 1) % e != 0:
            a += 1
        d = (a * phi_n + 1) / e
        return d

    def decrypt_cipher(self, d, n, encrypted_cipher): # Cipher is c in the formula
        unencrypted_cipher = (encrypted_cipher ** d) % n
        return unencrypted_cipher

    # For Aaron
    def convert_cipher_to_inverted_matrix(self):
        pass
        # return inverted_matrix

    # For Carl
    def decrypt_pk_message(self, d, n, message):
        pass
        # return encrypted_message


    # For Aaron
    def decrypt_hill_cipher(self, inverted_matrix):
        pass
        # return decrypted_message

    # For Aaron
    def output_plain_text_message(self):
        pass
        # Output the plain text message to a file


# Helper methods

# phi(n) = (p - 1) * (q - 1)
def generate_phi_n(p, q):
    phi_n = (p - 1) * (q - 1)
    return phi_n