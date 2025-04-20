# Analizador Semántico para Expresiones Aritméticas

Este proyecto implementa un analizador semántico que valida expresiones aritméticas, gestiona tipos de datos, verifica el ámbito de variables y evalúa expresiones matemáticas. Está desarrollado en Python utilizando la biblioteca PLY (Python Lex-Yacc).

## Requisitos Previos

- Python 3.6 o superior
- Biblioteca PLY

## Instalación

1. Asegúrate de tener Python instalado en tu sistema:
   ```
   python --version
   ```

2. Instala la biblioteca PLY usando pip:
   ```
   pip install ply
   ```

3. Descarga el archivo `analizador_semantico.py` de este repositorio.

## Ejecución del Analizador

1. Abre una terminal o línea de comandos.

2. Navega hasta el directorio donde se encuentra el archivo `analizador_semantico.py`.

3. Ejecuta el script:
   ```
   python analizador_semantico.py
   ```

4. Una vez iniciado el programa, verás el prompt `>>` que indica que puedes comenzar a ingresar expresiones para analizar.

## Uso del Analizador

El analizador acepta los siguientes tipos de comandos:

### Declaración de Variables
```
int x;
float y;
```

### Asignación de Valores
```
x = 10;
y = 3.14;
```

### Evaluación de Expresiones
```
x + y
(x * 2) + (y / 2)
```

### Finalizar el Programa
```
salir
```

## Ejemplos de Uso

Aquí hay una sesión de ejemplo mostrando cómo usar el analizador:

```
>> int x;
Variable 'x' declarada como int

>> float y;
Variable 'y' declarada como float

>> x = 5;
Asignación: x = 5

>> y = 3.14;
Asignación: y = 3.14

>> x + y
Resultado de evaluación: 8.14

Validación semántica completada exitosamente.

=== TABLA DE SÍMBOLOS ===
Variable	Tipo	Valor
------------------------------
x		int	5
y		float	3.14
==============================

>> (x * 2) + (y / 2)
Resultado de evaluación: 11.57

Validación semántica completada exitosamente.

=== TABLA DE SÍMBOLOS ===
Variable	Tipo	Valor
------------------------------
x		int	5
y		float	3.14
==============================

>> z = 10;
Error semántico: Variable 'z' no declarada.

>> int z;
Variable 'z' declarada como int

>> z = x / 0;
Error: División por cero
Asignación: z = None

>> salir
```

## Características Implementadas

1. **Análisis Léxico y Sintáctico**:
   - Reconocimiento de tokens (números, operadores, paréntesis, variables)
   - Construcción de estructuras sintácticas correctas

2. **Análisis Semántico**:
   - Verificación de tipos de datos
   - Control de variables no declaradas o no inicializadas
   - Detección de declaraciones duplicadas
   - Manejo de errores semánticos

3. **Evaluación de Expresiones**:
   - Operadores básicos: +, -, *, /
   - Soporte para paréntesis
   - Manejo de tipos numéricos (enteros y flotantes)

4. **Tabla de Símbolos**:
   - Almacenamiento de variables declaradas
   - Control de tipos y valores

## Manejo de Errores

El analizador detecta y reporta varios tipos de errores:

- Uso de variables no declaradas
- Declaraciones duplicadas de variables
- División por cero
- Errores sintácticos
- Variables no inicializadas

## Estructura del Código

- **Analizador Léxico**: Define los tokens del lenguaje
- **Analizador Sintáctico**: Define las reglas gramaticales
- **Analizador Semántico**: Verifica la coherencia de las operaciones
- **Tabla de Símbolos**: Almacena información sobre las variables
- **Evaluador**: Calcula el resultado de las expresiones

## Personalización

Puedes extender este analizador para incluir:
- Más tipos de datos
- Operadores adicionales
- Estructuras de control (if, while, etc.)
- Funciones

Modifica el archivo `analizador_semantico.py` según tus necesidades específicas.
