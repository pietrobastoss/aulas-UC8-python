"""A01 — prática 1. Use somente nome e idade fictícios."""

def conferir(nome, idade_texto):
    
    nome_limpo = nome.strip()
    if not nome_limpo:
        return "Erro: Não pode estar vazio ou apenas espaços."
    
    try:
        idade = int(idade_texto)
    except ValueError:
        return "A idade deve ser um número inteiro"
    
    if idade <= 0:
        return "A idade deve ser maior que zero"
    
    return f"\n### Cadastro Válido!### \nNome: {nome_limpo}\nIdade: {idade} anos."



if __name__ == "__main__":
    nome = input("Nome fictício: ")
    idade_texto = input("Idade fictícia: ")
    print(conferir(nome, idade_texto))
