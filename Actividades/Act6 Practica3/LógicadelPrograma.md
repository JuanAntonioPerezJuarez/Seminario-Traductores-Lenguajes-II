# Documentación Técnica: Analizador Semántico para Expresiones Aritméticas

Este documento explica en detalle la lógica y el funcionamiento interno del analizador semántico implementado en Python con PLY (Python Lex-Yacc).

## Arquitectura General

El analizador se compone de tres componentes principales interconectados:

1. **Analizador Léxico**: Convierte el texto de entrada en tokens
2. **Analizador Sintáctico**: Organiza los tokens en estructuras gramaticales
3. **Analizador Semántico**: Verifica la coherencia y evalúa las expresiones

## Flujo de Procesamiento

```
Texto de entrada → Analizador Léxico → Tokens → Analizador Sintáctico → Árbol Sintáctico → Analizador Semántico → Resultado/Errores
```

## Análisis Detallado del Código

### 1. Inicialización y Estructuras de Datos

```python
import ply.lex as lex
import ply.yacc as yacc
import sys

# Tabla de símbolos para almacenar variables y sus tipos
tabla_simbolos = {}
```

- **Importaciones**: Se importan los módulos necesarios de PLY para análisis léxico y sintáctico.
- **Tabla de símbolos**: Diccionario que almacena las variables declaradas con su tipo y valor. Estructura clave para el análisis semántico.

### 2. Analizador Léxico (Lexer)

```python
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
```

- **Tokens**: Define todos los elementos atómicos del lenguaje que el analizador léxico debe identificar.

```python
# Reglas para tokens simples
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_IGUAL = r'='
t_PUNTOCOMA = r';'
```

- **Definición de tokens simples**: Cada token se define mediante una expresión regular. Los tokens como operadores y símbolos utilizan este formato simple.

```python
# Palabras reservadas
def t_INT(t):
    r'int'
    return t

def t_FLOAT(t):
    r'float'
    return t
```

- **Palabras reservadas**: Se definen como funciones para facilitar su procesamiento específico si es necesario.

```python
# Regla para identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t
```

- **Identificadores**: Reconoce nombres de variables que comienzan con una letra o guión bajo, seguidos por letras, números o guiones bajos.

```python
# Regla para números (enteros y flotantes)
def t_NUMERO(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t
```

- **Números**: Reconoce enteros y flotantes. Además de identificar el token, realiza la conversión al tipo de dato correspondiente.

```python
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
```

- **Caracteres ignorados**: Espacios y tabulaciones no generan tokens.
- **Control de líneas**: Incrementa el contador de líneas para reportar errores con la ubicación correcta.
- **Manejo de errores léxicos**: Identifica caracteres no reconocidos en el flujo de entrada.
- **Inicialización del lexer**: Crea el analizador léxico con las reglas definidas.

### 3. Analizador Sintáctico (Parser)

```python
# Definición de la gramática
def p_programa(p):
    '''programa : declaracion
                | asignacion
                | expresion'''
    p[0] = p[1]
```

- **Punto de entrada**: Define la estructura de alto nivel del programa como declaraciones, asignaciones o expresiones.
- **Asignación p[0] = p[1]**: Transfiere el valor semántico de la producción derecha a la izquierda.

```python
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
```

- **Declaración de variables**: Reconoce patrones como "int x;" o "float y;".
- **Verificación semántica**: Detecta redeclaraciones de variables (error semántico).
- **Actualización de tabla de símbolos**: Registra la variable con su tipo (sin valor inicial).

```python
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
```

- **Asignación de valores**: Reconoce patrones como "x = 5;".
- **Verificación de existencia**: Comprueba que la variable haya sido declarada.
- **Comprobación de tipos**: Verifica la compatibilidad entre el tipo declarado y el valor asignado.
- **Conversión implícita**: Trunca valores flotantes asignados a variables enteras.

```python
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
```

- **Operaciones binarias**: Define las cuatro operaciones aritméticas básicas.
- **Evaluación de expresiones**: Calcula el resultado de cada operación.
- **Detección de división por cero**: Verifica este caso especial y emite un error.

```python
def p_expresion_parentesis(p):
    'expresion : LPAREN expresion RPAREN'
    p[0] = p[2]
```

- **Paréntesis**: Permite agrupar expresiones para alterar la precedencia predeterminada.
- **Preservación del valor**: El valor de la expresión entre paréntesis se preserva.

```python
def p_expresion_numero(p):
    'expresion : NUMERO'
    p[0] = p[1]
```

- **Números como expresiones**: Los literales numéricos son expresiones válidas.
- **Transferencia de valor**: El valor ya convertido por el lexer se transfiere a la expresión.

```python
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
```

- **Variables como expresiones**: Los identificadores son expresiones válidas.
- **Verificación de existencia**: Comprueba que la variable esté declarada.
- **Verificación de inicialización**: Comprueba que la variable tenga un valor asignado.
- **Manejo de errores con recuperación**: Proporciona un valor por defecto para continuar la evaluación.

```python
def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}', línea {p.lineno}")
    else:
        print("Error de sintaxis al final de la entrada")

# Construir el parser
parser = yacc.yacc()
```

- **Manejo de errores sintácticos**: Reporta errores de sintaxis con información contextual.
- **Inicialización del parser**: Crea el analizador sintáctico con las reglas definidas.

### 4. Funciones Auxiliares y Principal

```python
def mostrar_tabla_simbolos():
    print("\n=== TABLA DE SÍMBOLOS ===")
    print("Variable\tTipo\tValor")
    print("-" * 30)
    for var, info in tabla_simbolos.items():
        print(f"{var}\t\t{info['tipo']}\t{info['valor']}")
    print("=" * 30)
```

- **Visualización de la tabla de símbolos**: Muestra el estado actual de las variables.
- **Formato tabular**: Facilita la lectura de la información.

```python
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
```

- **Evaluación de expresiones**: Punto de entrada para evaluar una expresión.
- **Manejo de excepciones**: Captura errores durante el análisis.
- **Visualización de resultados**: Muestra el resultado y la tabla de símbolos.

```python
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
```

- **Interfaz interactiva**: Permite al usuario introducir expresiones una a una.
- **Bucle principal**: Procesa entradas hasta que el usuario escribe 'salir'.
- **Manejo de entrada/salida**: Captura errores de entrada.

## Flujo de Ejecución para un Ejemplo

Para ilustrar el flujo completo, veamos paso a paso cómo se procesa: `x = 5 + y;`

1. **Análisis Léxico**:
   - Se identifican los tokens: `ID(x)`, `IGUAL`, `NUMERO(5)`, `SUMA`, `ID(y)`, `PUNTOCOMA`

2. **Análisis Sintáctico**:
   - Se reconoce el patrón como una asignación: `ID IGUAL expresion PUNTOCOMA`
   - La expresión `5 + y` se identifica como: `expresion SUMA expresion`
   - El primer operando `5` se identifica como `NUMERO`
   - El segundo operando `y` se identifica como `ID`

3. **Análisis Semántico**:
   - Se verifica que `x` esté declarada en la tabla de símbolos
   - Se verifica que `y` esté declarada y tenga un valor
   - Se evalúa `5 + y` obteniendo el resultado
   - Se asigna el resultado a `x` actualizando la tabla de símbolos
   - Se verifica la compatibilidad de tipos entre el resultado y el tipo de `x`

4. **Resultado**:
   - Se muestra el valor asignado a `x`
   - Se actualiza y muestra la tabla de símbolos

## Detección de Errores Semánticos

El analizador detecta los siguientes errores semánticos:

1. **Variable no declarada**:
   ```python
   if p[1] not in tabla_simbolos:
       print(f"Error semántico: Variable '{p[1]}' no declarada.")
   ```

2. **Variable ya declarada**:
   ```python
   if p[2] in tabla_simbolos:
       print(f"Error semántico: Variable '{p[2]}' ya declarada previamente.")
   ```

3. **Variable no inicializada**:
   ```python
   if tabla_simbolos[p[1]]['valor'] is None:
       print(f"Error semántico: Variable '{p[1]}' no inicializada.")
   ```

4. **División por cero**:
   ```python
   if p[3] == 0:
       print("Error: División por cero")
   ```

5. **Incompatibilidad de tipos**:
   ```python
   if tipo_var == 'int' and isinstance(valor, float):
       print(f"Advertencia: Asignando valor flotante a variable entera '{p[1]}'. Se truncará el valor.")
   ```

## Limitaciones y Posibles Mejoras

1. **Precedencia de operadores**: La implementación actual no define explícitamente la precedencia de operadores, confiando en la gramática y el uso de paréntesis.

2. **Tipos de datos limitados**: Solo soporta enteros y flotantes. Podría extenderse a booleanos, cadenas, etc.

3. **Ámbito de variables**: Existe un único ámbito global. Podría implementarse ámbitos anidados para funciones o bloques.

4. **Operaciones soportadas**: Solo las cuatro operaciones aritméticas básicas. Podrían añadirse operaciones de comparación, lógicas, etc.

5. **Estructuras de control**: No implementa estructuras como condicionales o bucles.

6. **Funciones**: No soporta definición ni llamada a funciones.

## Conclusión

El analizador semántico implementa un subconjunto pequeño pero completo de un lenguaje de programación, centrándose en la evaluación de expresiones aritméticas y la gestión de variables con tipos. La estructura modular permite extenderlo para soportar características adicionales del lenguaje.
