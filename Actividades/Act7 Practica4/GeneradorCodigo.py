import ply.lex as lex
import ply.yacc as yacc
import sys

# Tabla de símbolos para almacenar variables y sus tipos
tabla_simbolos = {}

# Contador para variables temporales
temp_counter = 0
label_counter = 0

# Lista para almacenar código intermedio
codigo_intermedio = []

def new_temp():
    global temp_counter
    temp = f"t{temp_counter}"
    temp_counter += 1
    return temp

def new_label():
    global label_counter
    label = f"L{label_counter}"
    label_counter += 1
    return label

# Tabla de símbolos para almacenar variables y sus tipos
tabla_simbolos = {}

def generar_codigo_intermedio(nodo):
    global temp_counter
    
    if isinstance(nodo, (int, float)):
        return str(nodo)
    
    if isinstance(nodo, str) and not nodo.startswith('t'):
        return nodo
        
    if isinstance(nodo, tuple):
        if len(nodo) == 3:  # Operación binaria
            op = nodo[1]
            izq = generar_codigo_intermedio(nodo[0])
            der = generar_codigo_intermedio(nodo[2])
            
            temp = f"t{temp_counter}"
            temp_counter += 1
            
            if op == '=':  # Asignación
                codigo_intermedio.append(f"ASSIGN {izq} = {der}")
                return izq
            else:  # Otras operaciones
                codigo_intermedio.append(f"{temp} = {izq} {op} {der}")
                return temp
                
        elif len(nodo) == 2:  # Declaración
            tipo, var = nodo
            codigo_intermedio.append(f"DECLARE {tipo} {var}")
            return var
    
    return str(nodo)

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
    if p[2] in tabla_simbolos:
        print(f"Error semántico: Variable '{p[2]}' ya declarada previamente.")
        p[0] = None
        return
    
    tipo = 'int' if p[1] == 'int' else 'float'
    tabla_simbolos[p[2]] = {'tipo': tipo, 'valor': None}
    codigo_intermedio.append(f"DECLARE {tipo} {p[2]}")
    print(f"Variable '{p[2]}' declarada como {tipo}")
    p[0] = None

def p_asignacion(p):
    '''asignacion : ID IGUAL expresion PUNTOCOMA'''
    if p[1] not in tabla_simbolos:
        print(f"Error semántico: Variable '{p[1]}' no declarada.")
        p[0] = None
        return
    
    valor = p[3]
    tipo_var = tabla_simbolos[p[1]]['tipo']
    
    if tipo_var == 'int' and isinstance(valor, float):
        print(f"Advertencia: Asignando valor flotante a variable entera '{p[1]}'. Se truncará el valor.")
        valor = int(valor)
    
    tabla_simbolos[p[1]]['valor'] = valor
    codigo_intermedio.append(f"ASSIGN {p[1]} = {valor}")
    print(f"Asignación: {p[1]} = {valor}")
    p[0] = valor

def p_expresion_binaria(p):
    '''expresion : expresion SUMA expresion
                | expresion RESTA expresion
                | expresion MULT expresion
                | expresion DIV expresion'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
        temp = new_temp()
        codigo_intermedio.append(f"{temp} = {p[1]} + {p[3]}")
        p[0] = temp
    elif p[2] == '-':
        p[0] = p[1] - p[3]
        temp = new_temp()
        codigo_intermedio.append(f"{temp} = {p[1]} - {p[3]}")
        p[0] = temp
    elif p[2] == '*':
        p[0] = p[1] * p[3]
        temp = new_temp()
        codigo_intermedio.append(f"{temp} = {p[1]} * {p[3]}")
        p[0] = temp
    elif p[2] == '/':
        if p[3] == 0:
            print("Error: División por cero")
            p[0] = None
            return
        p[0] = p[1] / p[3]
        temp = new_temp()
        codigo_intermedio.append(f"{temp} = {p[1]} / {p[3]}")
        p[0] = temp

def p_expresion_numero(p):
    'expresion : NUMERO'
    p[0] = p[1]

def p_expresion_id(p):
    'expresion : ID'
    if p[1] not in tabla_simbolos:
        print(f"Error semántico: Variable '{p[1]}' no declarada.")
        p[0] = 0
        return
    
    if tabla_simbolos[p[1]]['valor'] is None:
        print(f"Error semántico: Variable '{p[1]}' no inicializada.")
        p[0] = 0
    else:
        p[0] = tabla_simbolos[p[1]]['valor']

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
    global codigo_intermedio
    codigo_intermedio = []  # Limpiar código intermedio anterior
    
    try:
        result = parser.parse(expresion)
        
        print("\n=== CÓDIGO INTERMEDIO ===")
        for i, instr in enumerate(codigo_intermedio):
            print(f"{i}: {instr}")
        
        print("\n=== CÓDIGO ENSAMBLADOR ===")
        print(generar_asm())
        
        print("\nValidación semántica completada exitosamente.")
        mostrar_tabla_simbolos()
        return result
    except Exception as e:
        print(f"Error durante el análisis: {e}")
        return None


# Función para generar código ensamblador
def generar_asm():
    asm_code = [
        "section .data",
        "; Variables declaradas"
    ]
    
    # Declarar variables
    for var, info in tabla_simbolos.items():
        if info['tipo'] == 'int':
            asm_code.append(f"{var} dd 0")
        else:
            asm_code.append(f"{var} dq 0.0")
    
    asm_code.extend([
        "\nsection .text",
        "global _start",
        "_start:"
    ])
    
    # Traducir código intermedio a ensamblador
    for instr in codigo_intermedio:
        if instr.startswith("DECLARE"):
            continue  # Las declaraciones ya se manejaron en .data
        elif "=" in instr:
            partes = instr.split("=")
            destino = partes[0].strip()
            expresion = partes[1].strip()
            
            if "+" in expresion:
                op1, op2 = expresion.split("+")
                asm_code.extend([
                    f"    mov eax, [{op1.strip()}]",
                    f"    add eax, [{op2.strip()}]",
                    f"    mov [{destino}], eax"
                ])
            elif "-" in expresion:
                op1, op2 = expresion.split("-")
                asm_code.extend([
                    f"    mov eax, [{op1.strip()}]",
                    f"    sub eax, [{op2.strip()}]",
                    f"    mov [{destino}], eax"
                ])
    
    # Agregar código de salida
    asm_code.extend([
        "\n    ; Salir del programa",
        "    mov eax, 1",
        "    xor ebx, ebx",
        "    int 0x80"
    ])
    
    return "\n".join(asm_code)

def evaluar_ast(expresion):
    """Evalúa una expresión y muestra los resultados"""
    global codigo_intermedio
    codigo_intermedio = []  # Limpiar código intermedio anterior
    
    try:
        result = parser.parse(expresion)
        if result is not None:
            print(f"\nResultado de evaluación: {result}")
        
        print("\n=== CÓDIGO INTERMEDIO ===")
        for i, instr in enumerate(codigo_intermedio):
            print(f"{i}: {instr}")
        
        print("\n=== CÓDIGO ENSAMBLADOR ===")
        print(generar_asm())
        
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