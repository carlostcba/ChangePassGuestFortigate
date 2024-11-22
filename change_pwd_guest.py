import paramiko
import datetime
import time  # Para retrasos entre comandos si es necesario

# Lista de servidores SSH
servers = [
    {"hostname": "10.0.0.1", "username": "usuario", "password": "contraseña"},
]

# Usuarios para los que se desea cambiar la contraseña
usuarios = ["invitados", "invitado"]

# Construir la nueva contraseña basada en el mes actual
mes_actual = datetime.datetime.now().month
nueva_contraseña = f"Lasalle{mes_actual:02d}"  # Formato 'Lasalle01', 'Lasalle12', etc.

# Función para conectarse y ejecutar comandos de forma interactiva
def ssh_interactive_command(server, usuarios, nueva_contraseña):
    try:
        # Crear una instancia del cliente SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server["hostname"], username=server["username"], password=server["password"])

        # Abrir una sesión interactiva
        shell = ssh.invoke_shell()
        time.sleep(1)  # Pequeña pausa para asegurarse de que el shell está listo

        # Procesar cada usuario
        for usuario in usuarios:
            try:
                # Enviar comandos línea por línea
                commands = [
                    "config user local",
                    f"edit {usuario}",
                    f"set passwd {nueva_contraseña}",
                    "end",
                ]
                for command in commands:
                    shell.send(command + "\n")  # Enviar comando con salto de línea
                    time.sleep(0.5)  # Esperar para que el dispositivo procese cada comando
                
                # Leer y procesar la salida
                time.sleep(1)  # Esperar para asegurarse de que toda la salida esté lista
                output = ""
                while shell.recv_ready():
                    output += shell.recv(2048).decode()

                # Verificar éxito o fallo
                if "Command fail" in output or "error" in output.lower():
                    print(f"[ERROR] Falló para el usuario '{usuario}' en {server['hostname']}: {output}")
                else:
                    print(f"[OK] Contraseña cambiada correctamente para '{usuario}' en {server['hostname']}")
            except Exception as e:
                print(f"[EXCEPTION] Error al cambiar la contraseña del usuario '{usuario}' en {server['hostname']}: {str(e)}")

        # Cerrar la conexión
        ssh.close()
    except Exception as e:
        print(f"[CONNECTION ERROR] No se pudo conectar a {server['hostname']}: {str(e)}")

# Iterar sobre cada servidor y ejecutar los comandos
for server in servers:
    ssh_interactive_command(server, usuarios, nueva_contraseña)
