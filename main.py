import socket

def get_service_name(port):

    try:
        return socket.getservbyport(port)
    except OSError:
        return "desconocido"

def escanear_puertos(ip_destino, rango_puertos):

    print("-" * 50)
    print(f"Escaneando {ip_destino} en el rango de puertos {rango_puertos[0]}-{rango_puertos[1]}...")
    print("-" * 50)
    
    puertos_abiertos = []
    
    for puerto in range(rango_puertos[0], rango_puertos[1] + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            resultado = s.connect_ex((ip_destino, puerto))
            
            if resultado == 0:
                nombre_servicio = get_service_name(puerto)
                print(f"Puerto {puerto} abierto: {nombre_servicio}")
                puertos_abiertos.append(f"{puerto} ({nombre_servicio})")
            
            s.close()

        except Exception as e:
            continue

    print("-" * 50)
    if puertos_abiertos:
        print("\nRESUMEN: Puertos abiertos encontrados:")
        print(", ".join(puertos_abiertos))
    else:
        print("\nRESUMEN: No se encontraron puertos abiertos en el rango especificado.")
    print("-" * 50)

def menu():

    while True:
        print("\n" + "=" * 50)
        print("  HERRAMIENTA DE ESCANEO DE PUERTOS EN PYTHON  ")
        print("=" * 50)

        ip_objetivo = input("Ingrese la dirección IP a escanear (ej. 192.168.1.1): ")


        try:
            inicio_puerto = int(input("Ingrese el puerto de inicio: "))
            fin_puerto = int(input("Ingrese el puerto de fin: "))
            
            if inicio_puerto > fin_puerto or inicio_puerto < 1 or fin_puerto > 65535:
                print("\n[!] Error: El rango de puertos no es válido. Debe ser entre 1 y 65535, y el inicio debe ser menor que el fin.")
                continue
            
            escanear_puertos(ip_objetivo, [inicio_puerto, fin_puerto])

        except ValueError:
            print("\n[!] Error: Los puertos deben ser números. Intente de nuevo.")
            continue
        
        volver_a_escanear = input("\n¿Desea realizar otro escaneo? (s/n): ")
        if volver_a_escanear.lower() != 's':
            print("\n¡Thnx por probar mi programa:3! ")
            break

if __name__ == "__main__":
    menu()
