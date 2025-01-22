"""Objetivo
El objetivo de esta actividad es que los estudiantes analicen la instrucción de imprimir una 
cadena en diferentes lenguajes de programación y desarrollen un algoritmo que permita validarla 
según las reglas de un lenguaje en especifico. Finalmente, 
se deberá generar un documento en formato PDF que contenga la descripción del 
proceso de análisis y el código fuente correspondiente en cada lenguaje.

Instrucciones

-   Selecciona un lenguaje de programación en el que la instrucción print("lo que sea") sea válida. 
        Ejemplos de lenguajes pueden incluir sintaxis de C. Python, JavaScript, Ruby, etc.
-   Analiza instrucción print(" cadena ") en el contexto del lenguaje seleccionado. 
        Considera aspectos como la función print, el manejo de cadenas de texto y la estructura general de la instrucción.


Desarrolla un algoritmo que valide si una instrucción sigue la sintaxis correcta del lenguaje seleccionado. 
El algoritmo debe:
-   Comprobar que la instrucción comience con la palabra reservada para imprimir según el lenguaje seleccionado.
-   Verificar que los paréntesis y las comillas estén correctamente balanceados.
-   Asegurarse de que el texto dentro de las comillas sea una cadena válida.
-   Escribe el algoritmo en el lenguaje de programación correspondiente.


Implementa el algoritmo en el lenguaje de programación que hayas elegido y asegúrate de probar 
el código para verificar que la validación funcione correctamente con diferentes entradas.


Redacta un documento que incluya:
-  Una breve introducción sobre el propósito de la actividad.
-  La descripción detallada del análisis de la instrucción print("Hola mundo") en el lenguaje seleccionado.
-  El algoritmo desarrollado para la validación.
-  El código fuente implementado
-  Resultados de pruebas realizadas con diferentes entradas.

Criterios de Evaluación
Grado de detalle y precisión en el análisis de la instrucción.
Correctitud y eficiencia del algoritmo desarrollado.
Funcionalidad y calidad del código implementado.
Claridad, organización y presentación del documento."""


repetir = 1
print("---Analizandor de Texto---")
while repetir == 1:
    print("Vamos a analizar una instruccion de codigo en python\n")
    CadenaUsuario = input("Dame la cadena que quieras analizar de python: ")

    if CadenaUsuario == 'print("Hola Mundo")':
        print("Tu cadena es:    ")
        print("---------------------------------")
        print(CadenaUsuario)
        print("---------------------------------")
        print(f"""Analicemos paso por paso lo que estas haciendo en esta Cadena:
              
              {CadenaUsuario}

            en la primer parte estas usando la palabra reservada ------> {CadenaUsuario[0:5]}

            Esta palabra esta enfocada en la salida de informacion a la pantalla, 
            pues imprime en pantalla lo que deseas


            Despues se encuentra con los simbolos especiales que siguien a la palabra reservada:
            
            {CadenaUsuario[5:7]}
            
            Estos simbolos nos declaran que despues de la palabra reservada tenemos el contenido de nuestra cadena
            En otras palabras es lo que queremos imprimir en pantalla.
            Con el inicio del parentesis le indicamos a python que dentro del parentesis esta contenida la cadena
            Y con las comillas indicamos que dentro de ellas esta nuestra cadena de texto

            Que en tu caso tu Cadena a Imprimir es: 

                    {CadenaUsuario[7:17]}
            Esto es el contenido de tu cadena.
            

            {CadenaUsuario[17:]}
            Y finalmente encontramos nuevamente los simbolos de cierre de comillas dobles y cierre de parentesis
            lo que nos indica que cierras tu cadena y cierras las instruccion PRINT

            """)
    else:
        print("Tu instruccion de python es incorrecta, revisa tu ORTOGRAFIA y SINTAXIS\n\n\n\n")
        repetir = 2
    

