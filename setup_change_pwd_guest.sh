#!/bin/bash

# Variables
REPO_URL="https://raw.githubusercontent.com/carlostcba/ChangePassGuestFortigate/main/change_pwd_guest.py"
SCRIPT_PATH="/usr/local/bin/change_pwd_guest.py"
LOG_FILE="/var/log/change_pwd_guest.log"
RETRY_SCRIPT="/usr/local/bin/retry_change_pwd_guest.sh"

# Actualización del sistema e instalación de dependencias
echo "Actualizando el sistema e instalando dependencias..."
sudo apt update && sudo apt install -y python3 python3-pip curl cron

# Instalar la biblioteca paramiko
echo "Instalando las bibliotecas necesarias para el script..."
sudo pip3 install paramiko

# Descargar el script Python
echo "Descargando el script change_pwd_guest.py..."
sudo curl -o "$SCRIPT_PATH" "$REPO_URL"
sudo chmod +x "$SCRIPT_PATH"

# Crear el log file si no existe
if [ ! -f "$LOG_FILE" ]; then
    sudo touch "$LOG_FILE"
    sudo chmod 666 "$LOG_FILE"
fi

# Crear un script de reintento
echo "Creando script de reintento..."
cat <<EOF | sudo tee "$RETRY_SCRIPT"
#!/bin/bash

# Ejecutar el script y registrar el resultado
python3 $SCRIPT_PATH >> $LOG_FILE 2>&1

# Verificar si el script fue exitoso
if [ \$? -ne 0 ]; then
    echo "El script falló. Reintentando en 1 hora..." >> $LOG_FILE
    sleep 3600
    python3 $SCRIPT_PATH >> $LOG_FILE 2>&1
else
    echo "El script se ejecutó con éxito." >> $LOG_FILE
fi
EOF
sudo chmod +x "$RETRY_SCRIPT"

# Agregar la tarea al cron
CRON_JOB="1 0 1 * * $RETRY_SCRIPT"
(crontab -l 2>/dev/null | grep -v "$RETRY_SCRIPT"; echo "$CRON_JOB") | crontab -

# Verificar que el cron está activo
sudo systemctl enable cron
sudo systemctl start cron

echo "Instalación y configuración completadas. El script se ejecutará el primer día del mes a las 00:01 y reintentará en caso de fallo."
