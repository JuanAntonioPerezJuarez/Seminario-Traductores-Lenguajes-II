# Analizador Sintáctico de Expresiones en Python

## Descripcion del Proyecto

Este proyecto implementa un analizador sintáctico capaz de validar expresiones de asignación y operaciones simples utilizando un enfoque de análisis sintáctico recursivo descendente.

## Caracteristicas Principales

- Validacion de estructuras de asignacion
- Reconocimiento de identificadores y expresiones
- Soporte para operaciones basicas (+, *, /)
- Manejo de expresiones anidadas con parentesis
- Interfaz interactiva de usuario

## Requisitos del Sistema

- Python 3.7 o superior
- No requiere bibliotecas externas adicionales

## Instalacion

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/analizador-sintactico.git
cd analizador-sintactico
```

2. Asegurar version de Python:
```bash
python3 --version
```

## Uso

Ejecutar el script directamente:

```bash
python3 syntax_parser.py
```

### Ejemplos de Uso

- Asignaciones simples: `x = 10;`
- Expresiones con operadores: `result = (a + b) * c;`
- Expresiones anidadas: `z = (x * y) + 3;`

## Modo de Operacion

1. Inicie el programa
2. Ingrese expresiones de asignacion
3. El analizador validara sintacticamente cada expresion
4. Presione Enter sin texto para salir

## Reglas Gramaticales Soportadas

- Identificadores: `[a-zA-Z][a-zA-Z0-9_]*`
- Numeros: `[0-9]+`
- Operadores: `+`, `*`, `/`
- Agrupacion con parentesis

## Limitaciones

- No evalua expresiones, solo valida su estructura
- Soporte limitado de operadores
- Sin manejo de tipos de datos complejos

## Posibles Mejoras

- Implementar generacion de Arbol de Sintaxis Abstracta (AST)
- Agregar soporte para mas operadores
- Implementar validacion semantica
- Manejar tipos de datos complejos

## Contribuciones

Las contribuciones son bienvenidas. Por favor, siga estos pasos:

1. Hacer fork del repositorio
2. Crear rama de caracteristica (`git checkout -b caracteristica/nueva`)
3. Confirmar cambios (`git commit -m 'Descripcion de cambios'`)
4. Empujar a la rama (`git push origin caracteristica/nueva`)
5. Abrir un Pull Request
