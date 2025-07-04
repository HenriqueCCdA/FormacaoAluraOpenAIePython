import hashlib

def gerar_hash(caminho_arquivo):
    sha256_hash = hashlib.sha256()
    try:
        with open(caminho_arquivo, "rb") as arquivo:
            for byte_block in iter(lambda: arquivo.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None
