# encoding: utf-8

from __future__ import unicode_literals
import logging
import random
import six
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from struct import pack
from django.conf import settings


__all__ = [
    u'encrypt',
    u'decrypt',
]


logger = logging.getLogger(__name__)


def encrypt(plain_text, key=None):
    """
    The encrypt function encrypts a unicode string using the
    Blowfish cipher (provided by pycrypto).  The key used is
    the SECRET_KEY specified in the settings file.

    @param plain_text The plaintext unicode string to be encrypted.

    @return The encrypted ciphertext.

    """

    block_size = AES.block_size
    if not isinstance(plain_text, six.string_types):
        plain_text = '%s' % plain_text
    b_plain_text = b64encode(plain_text.encode('utf-8'))
    iv = get_random_bytes(block_size)
    e_cipher = AES.new(
        key or settings.DJENGA_ENCRYPTION_KEY, AES.MODE_CBC, iv=iv)
    padding_len = block_size - len(b_plain_text) % block_size
    padding = [padding_len] * padding_len
    padding = pack('b' * padding_len, *padding)
    cipher_text = e_cipher.iv + e_cipher.encrypt(b_plain_text + padding)
    return cipher_text


def decrypt(cipher_text, key=None):
    """
    The decrypt function decrypts unicode strings that have
    been encrypted by the util.encryption.encrypt() function.
    The cipher used is Blowfish (provided by pcrypto), and the
    key used is the SECRET_KEY specified in the settings file.

    @param cipher_text The encrypted ciphertext.

    @return The decrypted plaintext (unicode) string.

    >>> import os
    >>> os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    >>> from django.conf import settings
    >>> settings.configure()
    >>> settings.DJENGA_ENCRYPTION_KEY = 'sesame'
    >>> st = 'hello'
    >>> decrypt(encrypt(st)) == st
    True
    """

    block_size = AES.block_size
    d_cipher = AES.new(key or settings.DJENGA_ENCRYPTION_KEY, AES.MODE_CBC)
    d_b64text = d_cipher.decrypt(cipher_text)
    plain_text = b64decode(d_b64text[block_size:]).decode('utf-8')
    return plain_text


if __name__ == "__main__":
    plain_text = 'Hello sesame!'
    key = b'0123456789012345'
    print(decrypt(encrypt(plain_text, key), key))


