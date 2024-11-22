
# SSH Password Management Script

Este script Python utiliza la biblioteca `paramiko` para conectarse a servidores SSH, cambiar contraseñas de usuarios de forma interactiva y verificar el resultado de la operación. Es ideal para administrar contraseñas en dispositivos como firewalls o servidores.

## Requisitos

1. **Python 3.x**: El script está diseñado para ejecutarse en Python 3.x.
2. **Biblioteca `paramiko`**: Necesaria para manejar conexiones SSH.

### Instalación de `paramiko`
Ejecuta el siguiente comando para instalar la biblioteca:
```bash
pip install paramiko
```

## Configuración

1. **Editar la lista de servidores**:
   Actualiza la sección `servers` con los detalles de los servidores SSH:
   ```python
   servers = [
       {"hostname": "10.0.0.1", "username": "usuario", "password": "contraseña"},
   ]
   ```

2. **Definir los usuarios a modificar**:
   Modifica la lista `usuarios` con los nombres de los usuarios cuyas contraseñas deseas cambiar:
   ```python
   usuarios = ["invitados", "invitado"]
   ```

3. **Nueva contraseña**:
   La nueva contraseña se genera dinámicamente en función del mes actual en el formato `LasalleMM`, donde `MM` es el mes en formato de dos dígitos (por ejemplo, `Lasalle11` para noviembre).

## Uso

1. **Descarga el script**:
   Guarda el código en un archivo llamado, por ejemplo, `ssh_password_manager.py`.

2. **Ejecuta el script**:
   Abre una terminal en la ubicación del archivo y ejecuta:
   ```bash
   python ssh_password_manager.py
   ```

3. **Resultados**:
   - Si la operación es exitosa, se mostrará:
     ```
     [OK] Contraseña cambiada correctamente para 'invitados' en 10.0.0.1
     ```
   - Si ocurre un error, se mostrará un mensaje similar a:
     ```
     [ERROR] Falló para el usuario 'invitados' en 10.0.0.1: Command fail - User not found
     ```

4. **Logs y manejo de errores**:
   El script captura y muestra errores relacionados con:
   - Conexión SSH fallida.
   - Errores en los comandos enviados.

## Estructura del Código

### 1. **Conexión SSH**
   - El script usa `paramiko.SSHClient` para conectarse al servidor especificado.

### 2. **Sesión interactiva**
   - Usa `invoke_shell` para manejar sesiones CLI que requieren comandos línea por línea.

### 3. **Ejecución de comandos**
   - Envía comandos como:
     - `config user local`
     - `edit <usuario>`
     - `set passwd <nueva_contraseña>`
     - `end`

### 4. **Validación**
   - Verifica si el comando fue exitoso buscando en la salida errores como `Command fail` o `error`.

## Personalización

Puedes modificar:
- **Formato de la contraseña**:
  Cambia la lógica de generación en esta línea:
  ```python
  nueva_contraseña = f"Lasalle{mes_actual:02d}"
  ```
  Por ejemplo, para agregar el año:
  ```python
  nueva_contraseña = f"Lasalle2024{mes_actual:02d}"
  ```

- **Tiempo entre comandos**:
  Ajusta los valores de `time.sleep()` para dispositivos que requieren más o menos tiempo para procesar.

## Notas

- **Seguridad**: Evita almacenar contraseñas en texto plano en el código. Considera usar un gestor de secretos o variables de entorno.
- **Compatibilidad**: Asegúrate de que los comandos enviados son compatibles con el sistema remoto.

## Licencia

Este script se proporciona bajo la [MIT License](LICENSE).
