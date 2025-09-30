# Questão 1 - Limpeza de Dados de Texto
# Objetivo: limpar a lista de e-mails removendo espaços extras e
#           deixando tudo em letras minúsculas.
# Dica: usar os métodos de string .strip() e .lower()
#       e percorrer a lista com um for (ou list comprehension).

# Lista original (igual à da prova)
emails_clientes = [
    '   joao.silva@gmail.com   ',
    '  MARIA.SANTOS@HOTMAIL.COM  ',
    '     pedro_costa@yahoo.com.br     ',
    '  ANA.OLIVEIRA@OUTLOOK.COM   ',
    '    carlos123@empresa.com.br   '
]

# Minha solução (versão com for):
emails_limpos = []  # lista vazia para guardar os e-mails já limpos
for email in emails_clientes:
    # .strip() tira espaços do começo e do fim
    # .lower() transforma todas as letras em minúsculas
    email_limpo = email.strip().lower()
    emails_limpos.append(email_limpo)

# Se preferir, também dá para fazer com list comprehension (apenas como referência):
# emails_limpos = [e.strip().lower() for e in emails_clientes]

# Mostrando o resultado final
print("E-mails limpos:")
for email in emails_limpos:
    print(email)
