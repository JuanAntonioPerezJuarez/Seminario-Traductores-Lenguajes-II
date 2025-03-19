import re

# Definición de los tokens y sus categorías
tokens = [
    (r'\b(int|float|char|void|string)\b', 0),  # Tipo de dato
    (r'\b(if|while|return|else|for)\b', lambda m: {'if': 9, 'while': 10, 'return': 11, 'else': 12, 'for': 13}[m.group()]),
    (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 1),  # Identificador
    (r'\b\d+(\.\d+)?\b', 2),  # Constante (números enteros y decimales)
    (r';', 3), (r',', 4), (r'\(', 5), (r'\)', 6), (r'\{', 7), (r'\}', 8), (r'=', 9),
    (r'\+|-', 14),  # Operadores de adición
    (r'\*|/|<<|>>', 15),  # Operadores de multiplicación
    (r'&&|\|\|', 16),  # Operadores lógicos
    (r'<|>|>=|<=|==|!=', 17),  # Operadores relacionales
    (r'\$', 18),  # Fin de entrada
    (r'".*?"', 19)  # Cadenas de texto
]

def lexer(input_string):
    token_counts = {i: 0 for i in range(20)}
    token_list = []
    pos = 0
    while pos < len(input_string):
        match = None
        for pattern, category in tokens:
            regex = re.compile(pattern)
            match = regex.match(input_string, pos)
            if match:
                token = match.group(0)
                category = category(match) if callable(category) else category
                token_counts[category] += 1
                token_list.append((token, category))
                pos = match.end()
                break
        if not match:
            print(f"Error léxico en: {input_string[pos]}")
            pos += 1
    
    return token_list, token_counts

if __name__ == "__main__":
    user_input = input("Ingrese el código a analizar: ")
    tokens_encontrados, conteo_tokens = lexer(user_input)
    
    print("\nTokens encontrados:")
    for token, categoria in tokens_encontrados:
        print(f"{token}: {categoria}")
    
    print("\nResumen de categorías:")
    for categoria, cantidad in conteo_tokens.items():
        print(f"Categoría {categoria}: {cantidad}")