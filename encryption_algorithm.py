import numpy

# CARL! Generate p and k randomly between certain vals and let me store them in a .key file
# TODO: Aaron - store the key in a .key file
class GeneratePrivateKey():

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

    # For Carl
    def create_private_key(self):
        pass
        # Up to carl how you want to implement, just make it fairly random
        # return tuple of p, q (so return 2 things)


    # Store key in .key file

if __name__ == '__main__':
    a = GeneratePrivateKey()
    print a.generate_prime_number(1000)

# CARL! Generate the public key from p and k and then generate e
# TODO: Aaron - store the public key in format (n, e)
class GeneratePublicKey():
    def __init__(self, p, q):
        self.p = p
        self.q = q
    # Make text file with key that can be given to message senders

class EncryptMessage():

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

    # For Carl
    # figure out number and sizes of matrices needed
    def determine_matrix_sizes(self, text_length):
        pass
        # return 2 values (tuple) containing first matrix size and second matrix size

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

class DecryptMessage():
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
