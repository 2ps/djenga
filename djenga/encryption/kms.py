from djenga.encryption.helpers import _as_bytes
from djenga.encryption.helpers import b64_str
from djenga.encryption.helpers import from_b64_str
from djenga.encryption.helpers import _get_client
from djenga.encryption.helpers import _prefix_alias


def encrypt_bytes(
        plain_text: bytes
        , alias: str
        , region: str=None
        , profile: str=None) -> bytes:
    client = _get_client(region, profile)
    alias = _prefix_alias(alias)
    data = client.encrypt(KeyId=alias, Plaintext=plain_text)
    return data['CiphertextBlob']


def decrypt_bytes(
        cipher_text: bytes
        , region: str=None
        , profile: str=None) -> bytes:
    client = _get_client(region, profile)
    data = client.decrypt(CiphertextBlob=cipher_text)
    return data['Plaintext']


def encrypt(plain_text, alias, region: str=None, profile: str=None) -> str:
    plain_text = _as_bytes(plain_text)
    data = encrypt_bytes(plain_text, alias, region, profile)
    return b64_str(data)


def decrypt(cipher_text: str, region: str=None, profile: str=None):
    cipher_text = from_b64_str(cipher_text)
    data = decrypt_bytes(cipher_text, region, profile)
    return data.decode('utf-8')
