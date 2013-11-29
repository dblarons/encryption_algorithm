## SAGE Encryption Algorithm
---

#### Background

This encryption algorithm, implemented in Python, is maintained by Carl Block and Aaron Smith, two Vanderbilt University undergraduate students. The algorithm and corresponding front-end application were presented at HackNashville in October 2013 and were later submitted as a class project for Math 194 (Linear Algebra) at the end of the fall 2013 semester.

#### Warning

At this point in time, this encryption algorithm is not intended to be used in any serious, real-world applications. There are serious vulnerabilities in the SAGE encryption algorithm (detailed below). These vulnerabilities have been largely ignored because the point of this project is not secure encryption as much as it is a proof of concept using Hill Ciphers and public key encryption.

#### Licensing

This code is open-sourced under the MIT License and can be modified or re-packaged with another application according to the terms of the LICENSE file included in this Github repository.

#### How does it work?

###### Encryption

The SAGE encryption algorithm uses a two-step encryption method. The first step, a padding scheme, is implemented with a simple Hill Cipher. The length of the message determines whether one or two matrices are generated. For example, if there are 41 characters in the message and the chosen matrix size is 5, then one 5x5 matrix and one 6x6 matrix will be generated. The first matrix will be used seven times to encrypt a total of 35 characters of the message. The second matrix (6x6) will be used to encrypt the remaining 6 characters of the message.

Once the message has been encrypted by the Hill Cipher, the public key pair of the person you want to send the message to is used to encrypt both the matrix and the padded message (please note that packaging the key to the padding scheme __with__ the message itself is a __serious__ vulnerability in the SAGE encryption method). The public-key encrypted message can now be sent to its intended recipient.

###### Decryption

When the encrypted message is received by its intended party, the first layer of encryption can be undone by using the correct private key. Once this layer of encryption has been unlocked, both matrices are inverted and used to undo the padding scheme of the message. The message is now human-readable.

### Usage

#### Generating and Retrieving Keys

###### Generate and store a private key

`private_key = PrivateKey()`

`private_key.new_private_key_pair()`

`private_key.store_private_key('mypath/private_key.txt')`


###### Retrieve a stored private key

`private_key = PublicKey()`

`private_key.retrieve_stored_key('mypath/private_key.txt')`


###### Generate and store a public key

`public_key = PublicKey(private_key.p, private_key.q)`

`public_key.new_public_key_pair()`

`public_key.store_public_key('mypath/public_key.txt')`


###### Retrieve a stored public key

`public_key = PublicKey(private_key.p, private_key.q)`

`public_key.retrieve_stored_key('mypath/public_key.txt')`


#### Encrypting Messages

`encrypted_msg = EncryptMessage(public_key.n, public_key.e, 'mypath/input_file.txt')`

`enrypted_msg.write('mypath/output_file.txt')`


#### Decrypting Messages

`decrypted_msg = DecryptMessage(private_key.p, private_key.q, public_key.e, 'mypath/input_file.txt')`

`decrypted_msg.write('mypath/output_file.txt')`