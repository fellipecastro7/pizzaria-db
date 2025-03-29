def validar_preco(preco):
    try:
        preco = float(preco)
        if preco <= 0:
            return "O preço deve ser um valor positivo."
    except ValueError:
        return "O preço deve ser um número válido."
    return None


def validar_nome(nome):
    if not nome.strip():
        return "O nome do item não pode ser vazio."
    return None


def validar_categoria(categoria):
    if categoria not in ["pizza", "bebida"]:
        return "Categoria inválida. Escolha 'pizza' ou 'bebida'."
    return None
