import numpy
import random

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
        private_keys = prime_to_million[thousand_length:]
        random_int = random.randint(0, len(private_keys))
        key = private_keys[random_int]
        return key

    def get_private_key(self):
        p = self.create_private_key()
        q = self.create_private_key()
        while q == p:
            q = self.create_private_key()
        p = long(p)
        q = long(q)
        return p, q

    # Aaron - Store key in .key file

# TODO: Aaron - store the public key in format (n, e)
class GeneratePublicKey(object):
    def __init__(self, p, q):
        self.p = p
        self.q = q
    # Make text file with key that can be given to message senders
    def generate_n(self):
        n = self.p * self.q
        return n

    def generate_phi_n(self):
        p_less_one = self.p - 1
        q_less_one = self.q - 1
        phi_n = p_less_one * q_less_one
        return phi_n

    def generate_e(self):
        private_key = GeneratePrivateKey()
        prime_generator = private_key.create_private_key()
        e = prime_generator
        phi_n = self.generate_phi_n()
        while phi_n % e == 0:
            e = prime_generator
        return e

    def get_public_key(self):
        return self.generate_n(), self.generate_e()

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
        # return 2 values (tuple) containing first matrix size and second matrix size
        if text_length / size == 0:
            return text_length % size, 0
        elif text_length % size == 0:
            return size, 0
        elif text_length % size == 1
            if text_length / size == 1:
                return size + 1, 0
            else:
                return size, size + 1
        else:
            return size, text_length % size

    def number_of_matrices(self, text_length, size):
        if text_length % size == 0:
            return text_length / size
        elif: text_length % size == 1 and text_length / size == 1:
            return 1
        else:
            return text_length / size + 1

    # For Aaron - plain_text and cipher are matrices
    def encrypt_plain_text(self, plain_text, cipher):
        pass
        # return encrypted_message

    # For Carl - cipher is an array
    def encrypt_cipher_with_public_key(self, cipher, n, e):
        pass
        # return pk_encrypted_cipher (as a string)

    # For Carl - message is an array
    def encrypt_message_with_public_key(self, message, n, e):
        pass
        # return pk_encrypted_message (as a string)

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

    # For Carl
    def generate_phi(self, p, q):
        pass
        # return phi_n

    # For Carl
    def generate_d(self, e, phi_n):
        pass
        # return d (for pk encryption)

    # For Carl
    def decrypt_cipher(self, d, n, encrypted_cipher): # Cipher is c in the formula
        pass
        # return unencrypted_cipher

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
