import ply.lex as lex
import ply.yacc as yacc
import sys

# Tabla de símbolos para almacenar variables y sus tipos
tabla_simbolos = {}

# Definición del analizador léxico
tokens = (
    'NUMERO',
    'ID',
    'SUMA',
    'RESTA',
    'MULT',
    'DIV',
    'LPAREN',
    'RPAREN',
    'IGUAL',
    'PUNTOCOMA',
    'INT',
    'FLOAT'
)

# Reglas para tokens simples
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_IGUAL = r'='
t_PUNTOCOMA = r';'

# Palabras reservadas
def t_INT(t):
    r'int'
    return t

def t_FLOAT(t):
    r'float'
    return t

# Regla para identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Regla para números (enteros y flotantes)
def t_NUMERO(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Nueva línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()

# Definición de la gramática
def p_programa(p):
    '''programa : declaracion
                | asignacion
                | expresion'''
    p[0] = p[1]

def p_declaracion(p):
    '''declaracion : INT ID PUNTOCOMA
                   | FLOAT ID PUNTOCOMA'''
    if p[1] == 'int':
        tipo = 'int'
    else:
        tipo = 'float'
    
    # Verificar si la variable ya está declarada
    if p[2] in tabla_simbolos:
        print(f"Error semántico: Variable '{p[2]}' ya declarada previamente.")
    else:
        tabla_simbolos[p[2]] = {'tipo': tipo, 'valor': None}
        print(f"Variable '{p[2]}' declarada como {tipo}")
    
    p[0] = None

def p_asignacion(p):
    '''asignacion : ID IGUAL expresion PUNTOCOMA'''
    # Verificar si la variable está declarada
    if p[1] not in tabla_simbolos:
        print(f"Error semántico: Variable '{p[1]}' no declarada.")
        p[0] = None
        return
    
    # Asignar el valor y verificar compatibilidad de tipos
    valor = p[3]
    tipo_var = tabla_simbolos[p[1]]['tipo']
    
    if tipo_var == 'int' and isinstance(valor, float):
        print(f"Advertencia: Asignando valor flotante a variable entera '{p[1]}'. Se truncará el valor.")
        valor = int(valor)
    
    tabla_simbolos[p[1]]['valor'] = valor
    print(f"Asignación: {p[1]} = {valor}")
    p[0] = valor

def p_expresion_binaria(p):
    '''expresion : expresion SUMA expresion
                 | expresion RESTA expresion
                 | expresion MULT expresion
                 | expresion DIV expresion'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        # Verificar división por cero
        if p[3] == 0:
            print("Error: División por cero")
            p[0] = None
        else:
            p[0] = p[1] / p[3]

def p_expresion_parentesis(p):
    'expresion : LPAREN expresion RPAREN'
    p[0] = p[2]

def p_expresion_numero(p):
    'expresion : NUMERO'
    p[0] = p[1]

def p_expresion_id(p):
    'expresion : ID'
    # Verificar si la variable existe en la tabla de símbolos
    if p[1] not in tabla_simbolos:
        print(f"Error semántico: Variable '{p[1]}' no declarada.")
        p[0] = 0  # Valor por defecto para continuar la evaluación
        return
    
    # Verificar si la variable tiene valor asignado
    if tabla_simbolos[p[1]]['valor'] is None:
        print(f"Error semántico: Variable '{p[1]}' no inicializada.")
        p[0] = 0  # Valor por defecto para continuar la evaluación
    else:
        p[0] = tabla_simbolos[p[1]]['valor']

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}', línea {p.lineno}")
    else:
        print("Error de sintaxis al final de la entrada")

# Construir el parser
parser = yacc.yacc()

def mostrar_tabla_simbolos():
    print("\n=== TABLA DE SÍMBOLOS ===")
    print("Variable\tTipo\tValor")
    print("-" * 30)
    for var, info in tabla_simbolos.items():
        print(f"{var}\t\t{info['tipo']}\t{info['valor']}")
    print("=" * 30)

def evaluar_ast(expresion):
    """Evalúa una expresión y muestra los resultados"""
    try:
        result = parser.parse(expresion)
        if result is not None:
            print(f"Resultado de evaluación: {result}")
        print("\nValidación semántica completada exitosamente.")
        mostrar_tabla_simbolos()
        return result
    except Exception as e:
        print(f"Error durante el análisis: {e}")
        return None

# Función principal para probar el analizador
def main():
    print("Analizador Semántico - Evaluador de Expresiones")
    print("Ingrese 'salir' para terminar")
    
    while True:
        try:
            expresion = input(">> ")
            if expresion.lower() == 'salir':
                break
            evaluar_ast(expresion)
        except EOFError:
            break

if __name__ == "__main__":
    main()