# encoding: utf-8

from __future__ import unicode_literals
import logging
import random
from base64 import b64decode
from base64 import b64encode
from Crypto.Protocol.KDF import PBKDF2 as derive_key
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from struct import pack
from django.conf import settings
from djenga.encryption.helpers import _as_bytes


__all__ = [
    u'encrypt',
    u'encrypt_bytes',
    u'decrypt',
    u'decrypt_bytes',
]


logger = logging.getLogger(__name__)


def _prep_key(key=None):
    key = key or settings.DJENGA_ENCRYPTION_KEY
    return _as_bytes(key)


def _gcm_pack(header, cipher_text, tag, nonce, kdf_salt):
    values = [ header, cipher_text, tag, nonce, kdf_salt ]
    values = [ b64encode(x).decode('utf-8') for x in values ]
    return '|'.join(values)


def _gcm_unpack(value):
    values = value.split('|')
    if len(values) != 5:
        raise ValueError('Unpacked value did not have exactly four pieces')
    values = [ b64decode(x.encode('utf-8')) for x in values ]
    return values


def encrypt(plain_text, key=None, auth_header='djenga'):
    """
    The encrypt function encrypts a unicode string using the
    Blowfish cipher (provided by pycrypto).  The key used is
    the SECRET_KEY specified in the settings file.

    :param plain_text: The plaintext unicode string to be encrypted.
    :param key: the password to use for encryption
    :param auth_header: str
    :return The encrypted ciphertext.

    """
    plain_text = _as_bytes(plain_text)
    return encrypt_bytes(plain_text, key, auth_header)


def encrypt_bytes(plain_text, key=None, auth_header='djenga'):
    """
    The encrypt function encrypts a unicode string using the
    Blowfish cipher (provided by pycrypto).  The key used is
    the SECRET_KEY specified in the settings file.

    :param plain_text: The plaintext unicode string to be encrypted.
    :param key: the password to use for encryption
    :param auth_header: str
    :return The encrypted ciphertext.

    """
    kdf_salt = get_random_bytes(32)
    key = key or settings.DJENGA_ENCRYPTION_KEY
    derived_key = derive_key(key, kdf_salt, 32)
    cipher = AES.new(derived_key, AES.MODE_GCM)
    auth_header = _as_bytes(auth_header)
    cipher.update(auth_header)
    cipher_text, tag = cipher.encrypt_and_digest(plain_text)
    nonce = cipher.nonce
    return _gcm_pack(auth_header, cipher_text, tag, nonce, kdf_salt)


def decrypt(packed_value, key=None):
    data = decrypt_bytes(packed_value, key)
    return data.decode('utf-8')


def decrypt_bytes(packed_value, key=None):
    """
    The decrypt function decrypts unicode strings that have
    been encrypted by the util.encryption.encrypt() function.
    The cipher used is Blowfish (provided by pcrypto), and the
    key used is the SECRET_KEY specified in the settings file.

    :param packed_value: The encrypted pieces needed for decryption.
    :param key: the password to use when encrypting
    :return The decrypted plaintext (unicode) string.

    >>> import uuid
    >>> key = uuid.uuid4()
    >>> st = 'hello'
    >>> decrypt(encrypt(st, key.bytes), key.bytes) == st
    True
    """
    header, cipher_text, tag, nonce, kdf_salt = _gcm_unpack(packed_value)
    key = key or settings.DJENGA_ENCRYPTION_KEY
    decryption_key = derive_key(key, kdf_salt, 32)
    cipher = AES.new(decryption_key, AES.MODE_GCM, nonce)
    cipher.update(header)
    data = cipher.decrypt_and_verify(cipher_text, tag)
    return data


def _test_me():
    import uuid
    plain_text = 'Hello sesame!'
    key = uuid.uuid4()
    cipher_text = encrypt(plain_text, key.bytes)
    print(f'cipher_text: {cipher_text}')
    value = decrypt(cipher_text, key.bytes)
    print(f'after      : {value}')


if __name__ == "__main__":
    _test_me()


