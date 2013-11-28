from encryption_algorithm import encryption_algorithm as sage

def test_storing_and_retrieving_private_key():
    ''' store key '''
    private_key = sage.PrivateKey()
    private_key.new_private_key_pair()
    private_key.store_private_key('tests/test_private_key.txt')
    stored = [private_key.p, private_key.q]

    ''' retrieve key '''
    alt_private_key = sage.PrivateKey()
    alt_private_key.retrieve_stored_key('tests/test_private_key.txt')
    assert [alt_private_key.p, alt_private_key.q] == stored

def test_storing_and_retrieving_public_key():
    private_key = sage.PrivateKey()
    private_key.retrieve_stored_key('tests/test_private_key.txt')

    ''' store key '''
    public_key = sage.PublicKey(private_key.p, private_key.q)
    public_key.new_public_key_pair()
    public_key.store_public_key('tests/test_public_key.txt')
    stored = [public_key.n, public_key.e]

    ''' retrieve key '''
    alt_public_key = sage.PublicKey(private_key.p, private_key.q)
    alt_public_key.retrieve_stored_key('tests/test_public_key.txt')
    assert [alt_public_key.n, alt_public_key.e] == stored

