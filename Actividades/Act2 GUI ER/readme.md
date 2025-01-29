# Formulario de Validación de Datos Personales

## Descripción
Una aplicación GUI desarrollada en Python con Tkinter que valida datos personales incluyendo números telefónicos, correos electrónicos, CURP, RFC, direcciones IPv4 y fechas de nacimiento. La aplicación proporciona validación en tiempo real utilizando expresiones regulares y muestra mensajes de error para entradas inválidas.

## Características
- Valida los siguientes datos:
  - Números telefónicos (10 dígitos)
  - Direcciones de correo electrónico
  - CURP (Clave Única de Registro de Población)
  - RFC (Registro Federal de Contribuyentes)
  - Direcciones IPv4
  - Fechas de nacimiento (formato DD/MM/AA)

## Requisitos
- Python 3.x
- Tkinter (generalmente viene con la instalación de Python)
- Re (biblioteca de Expresiones Regulares, parte de la biblioteca estándar de Python)

## Clonar el Repositorio
Para obtener una copia local del proyecto, ejecuta el siguiente comando:
```bash
git clone https://github.com/tu-usuario/nombre-del-repo.git
cd nombre-del-repo
```

## Instalación
No se requiere instalación adicional si ya tienes Python 3.x instalado, ya que tanto Tkinter como Re son parte de la biblioteca estándar.

## Uso
1. Ejecuta el script:
```bash
python GUI-ER.py
```
2. Se abrirá una ventana con campos para:
   - Número telefónico
   - Correo electrónico
   - CURP
   - RFC
   - Dirección IPv4
   - Fecha de nacimiento

3. Ingresa la información requerida en cada campo
4. Haz clic en "Validar y Enviar" para verificar las entradas
5. La aplicación mostrará:
   - Un mensaje de error listando las entradas inválidas
   - Un mensaje de éxito si todas las entradas son válidas

## Requisitos de Formato de Entrada
- Teléfono: solo 10 dígitos
- Correo: formato estándar de correo (ejemplo@dominio.com)
- CURP: formato estándar mexicano ([A-Z]{4}\d{6}[HM][A-Z]{5}\d{2})
- RFC: formato estándar mexicano ([A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3})
- IPv4: formato estándar IPv4 (xxx.xxx.xxx.xxx)
- Fecha de nacimiento: formato DD/MM/AA

## Manejo de Errores
- La aplicación valida cada campo usando expresiones regulares
- Las entradas inválidas se reportan en un mensaje emergente de error
- Se pueden mostrar múltiples errores simultáneamente
- El mensaje de éxito aparece cuando todas las entradas son válidas

## Detalles Técnicos
- Construido usando Tkinter para la interfaz gráfica
- Usa expresiones regulares (biblioteca re) para validación de entradas
- Implementa diseño de cuadrícula para elementos del formulario
- Incluye manejo de mensajes de error a través de messagebox

## Estructura de Archivos
- `GUI-ER.py`: Archivo principal de la aplicación que contiene todo el código

## Contribuir
1. Haz un Fork del proyecto
2. Crea una rama para tu función (`git checkout -b feature/NuevaFuncion`)
3. Haz commit de tus cambios (`git commit -m 'Añadir nueva función'`)
4. Haz Push a la rama (`git push origin feature/NuevaFuncion`)
5. Abre un Pull Request

## Idioma
- Interfaz en español
- Mensajes de error en español
