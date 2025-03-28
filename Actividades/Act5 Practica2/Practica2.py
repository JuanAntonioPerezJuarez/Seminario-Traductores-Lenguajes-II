import re
import sys

class SyntaxParser:
    def __init__(self, input_string):
        # Eliminar espacios en blanco
        self.tokens = input_string.replace(' ', '').split(';')
        # Eliminar cadenas vacías
        self.tokens = [token for token in self.tokens if token]
        self.current_token = None
        self.token_index = 0

    def parse(self):
        """
        Método principal para parsear el programa completo
        """
        try:
            while self.token_index < len(self.tokens):
                # Parsear cada instrucción
                current_statement = self.tokens[self.token_index]
                self.token_index += 1
                
                # Reiniciar índices para cada instrucción
                self.current_token = None
                self.pos = 0
                
                # Analizar la instrucción
                print(f"Analizando expresion: {current_statement}")
                
                # Realizar validaciones
                resultado = self.validate_assignment(current_statement)
                
                # Imprimir resultados detallados
                if resultado:
                    print("--- Validacion Completa ---")
                    print(f"Identificador: {resultado['identificador']}")
                    print(f"Expresion: {resultado['expresion']}")
                    print("Estado: Expresion Sintacticamente Correcta")
                
            return True
        except SyntaxError as e:
            print(f"Error de sintaxis: {e}")
            return False

    def validate_assignment(self, statement):
        """
        Validar una sentencia de asignación
        """
        # Dividir la asignación en identificador y expresión
        parts = statement.split('=')
        if len(parts) != 2:
            raise SyntaxError("Formato de asignacion invalido")
        
        identificador = parts[0].strip()
        expresion = parts[1].strip()
        
        # Validar identificador
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', identificador):
            raise SyntaxError(f"Identificador invalido: {identificador}")
        
        # Validar la expresión
        self.validate_expression(expresion)
        
        # Retornar detalles de la validación
        return {
            'identificador': identificador,
            'expresion': expresion
        }

    def validate_expression(self, expresion):
        """
        Validar una expresión
        """
        # Método para dividir la expresión en términos
        def split_by_operator(expr, operators):
            for op in operators:
                if op in expr:
                    parts = expr.split(op, 1)
                    return parts[0].strip(), op, parts[1].strip()
            return expr, None, None

        # Registro de operaciones encontradas
        operaciones_encontradas = []

        # Primero intentar dividir por suma
        term1, op_suma, term2 = split_by_operator(expresion, ['+'])
        
        # Validar el primer término
        self.validate_term(term1)
        
        # Si hay suma, validar el segundo término y registrar
        if op_suma:
            operaciones_encontradas.append('+')
            self.validate_term(term2)

        return operaciones_encontradas

    def validate_term(self, termino):
        """
        Validar un término
        """
        # Método para dividir el término
        def split_by_operator(expr, operators):
            for op in operators:
                if op in expr:
                    parts = expr.split(op, 1)
                    return parts[0].strip(), op, parts[1].strip()
            return expr, None, None

        # Registro de operaciones encontradas
        operaciones_encontradas = []

        # Primero intentar dividir por multiplicación o división
        factor1, op_mult, factor2 = split_by_operator(termino, ['*', '/'])
        
        # Validar el primer factor
        self.validate_factor(factor1)
        
        # Si hay multiplicación o división, validar el segundo factor y registrar
        if op_mult:
            operaciones_encontradas.append(op_mult)
            self.validate_factor(factor2)

        return operaciones_encontradas

    def validate_factor(self, factor):
        """
        Validar un factor 
        """
        # Quitar paréntesis si los hay
        if factor.startswith('(') and factor.endswith(')'):
            factor = factor[1:-1].strip()
            # Recursivamente validar la expresión dentro de los paréntesis
            self.validate_expression(factor)
        else:
            # Verificar si es un identificador o un número
            if re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', factor):
                print(f"    - Factor Identificador: {factor}")
                return "identificador"
            elif re.match(r'^[0-9]+$', factor):
                print(f"    - Factor Numero: {factor}")
                return "numero"
            else:
                raise SyntaxError(f"Factor invalido: {factor}")

def main():
    print("Analizador Sintactico de Expresiones")
    print("Ingrese una expresion de asignacion (ej. x = 10; o result = (a + b) * c;)")
    print("Presione Enter sin escribir nada para salir.")
    
    while True:
        # Solicitar entrada al usuario
        entrada = input("\nIngrese su expresion: ")
        
        # Salir si no hay entrada
        if not entrada:
            print("Saliendo del programa.")
            break
        
        # Crear y ejecutar el parser
        parser = SyntaxParser(entrada)
        parser.parse()

if __name__ == "__main__":
    main()