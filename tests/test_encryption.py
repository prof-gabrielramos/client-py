import pytest

from android_sms_gateway.encryption import Encryptor


def test_decrypt():
    passphrase = "passphrase"
    cleartext = "hello"
    encrypted = "$aes-256-cbc/pbkdf2-sha1$i=75000$obSTW6ittQvTtdAxonQKIw==$g3QFAC9CtBcPxoKlouqsyQ=="
    # A função Encryptor usa 'passphrase' como primeiro argumento.
    # Iterations são lidas do payload para decrypt, mas o encryptor precisa ser inicializado.
    # Para o decrypt funcionar com o payload dado, o encryptor precisa ser inicializado com as iterações do payload.
    # No entanto, a função Encryptor tem um default, então apenas passphrase é necessário para instanciar.
    # O método decrypt da classe AESEncryptor usa as iterações do payload.
    encryptor = Encryptor(passphrase=passphrase) # Passando passphrase

    decrypted = encryptor.decrypt(encrypted)

    assert cleartext == decrypted


def test_encrypt_decrypt():
    passphrase = "correcthorsebatterystaple"
    encryptor = Encryptor(passphrase=passphrase, iterations=1000) # Passando passphrase
    cleartext = "The quick brown fox jumps over the lazy dog"
    encrypted = encryptor.encrypt(cleartext)
    decrypted = encryptor.decrypt(encrypted)
    assert cleartext == decrypted


def test_invalid_format_error():
    passphrase = "correcthorsebatterystaple"
    encryptor = Encryptor(passphrase=passphrase, iterations=1000) # Passando passphrase
    with pytest.raises(ValueError, match="Invalid encryption format"):
        encryptor.decrypt("invalid$format$string")


def test_unsupported_algorithm_error():
    passphrase = "correcthorsebatterystaple"
    encryptor = Encryptor(passphrase=passphrase, iterations=1000) # Passando passphrase
    with pytest.raises(ValueError, match="Unsupported algorithm"):
        encryptor.decrypt("$unsupported-algorithm$i=0$salt$data")


def test_missing_iteration_count_error():
    passphrase = "correcthorsebatterystaple"
    encryptor = Encryptor(passphrase=passphrase, iterations=1000) # Passando passphrase
    with pytest.raises(ValueError, match="Missing iteration count"):
        encryptor.decrypt("$aes-256-cbc/pbkdf2-sha1$x=0$salt$data")
