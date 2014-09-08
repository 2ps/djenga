#encoding: utf-8

from __future__ import unicode_literals
import logging
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import Blowfish
from Crypto import Random
from struct import pack
import settings


__all__ = [
    u'encrypt',
    u'decrypt',
]


logger = logging.getLogger(__name__)


def encrypt(s):
    """
    The encrypt function encrypts a unicode string using the
    Blowfish cipher (provided by pycrypto).  The key used is
    the SECRET_KEY specified in the settings file.

    @param s The plaintext unicode string to be encrypted.

    @return The encrypted ciphertext.
    """

    block_size = Blowfish.block_size
    iv = Random.new().read(block_size)
    if not isinstance(s, basestring):
        s = '%s' % s
    b_plaintext = b64encode(s.encode('utf-8'))
    plen = block_size - (len(b_plaintext) % 8)
    padding = [plen] * plen
    padding = pack('b' * plen, *padding)
    e_cipher = Blowfish.new(settings.DJENGA_ENCRYPTION_KEY, Blowfish.MODE_CBC, iv)
    ciphertext = iv + e_cipher.encrypt(b_plaintext + padding)
    return ciphertext


def decrypt(s):
    """
    The decrypt function decrypts unicode strings that have
    been encrypted by the util.encryption.encrypt() function.
    The cipher used is Blowfish (provided by pcrypto), and the
    key used is the SECRET_KEY specified in the settings file.

    @param s The encrypted ciphertext.

    @return The decrypted plaintext (unicode) string.
    """

    block_size = Blowfish.block_size
    d_cipher = Blowfish.new(settings.DJENGA_ENCRYPTION_KEY, Blowfish.MODE_CBC)
    d_b64text = d_cipher.decrypt(s)
    plaintext = b64decode(d_b64text[block_size:]).decode('utf-8')
    return plaintext

