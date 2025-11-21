import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext
from concurrent.futures import ThreadPoolExecutor 
import threading
import sys 
import os 

MAX_TRABAJADORES = 100 

def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "desconocido"

def verificar_puerto(ip_destino, puerto, timeout_seg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout_seg)
    
    resultado = s.connect_ex((ip_destino, puerto))
    s.close()

    if resultado == 0:
        return puerto, get_service_name(puerto)
    
    return None

def escanear_puertos(ip_destino, rango_puertos, timeout_seg, output_text_widget, btn_iniciar, btn_salir):
    
    btn_iniciar.config(state=tk.DISABLED)
    btn_salir.config(state=tk.DISABLED)

    output_text_widget.delete(1.0, tk.END)
    output_text_widget.insert(tk.END, "-" * 50 + "\n")
    output_text_widget.insert(tk.END, f"🚀 Escaneo Concurrente: {ip_destino} en el rango {rango_puertos[0]}-{rango_puertos[1]} (Timeout: {timeout_seg}s, Hilos: {MAX_TRABAJADORES})\n")
    output_text_widget.insert(tk.END, "-" * 50 + "\n")
    output_text_widget.update_idletasks()

    puertos_abiertos = []
    
    with ThreadPoolExecutor(max_workers=MAX_TRABAJADORES) as executor:
        future_to_port = [executor.submit(verificar_puerto, ip_destino, puerto, timeout_seg) 
                          for puerto in range(rango_puertos[0], rango_puertos[1] + 1)]

        for future in future_to_port:
            try:
                resultado = future.result()
                if resultado:
                    puerto, nombre_servicio = resultado
                    mensaje = f"Puerto {puerto} abierto: {nombre_servicio}\n"
                    
                    output_text_widget.insert(tk.END, mensaje)
                    output_text_widget.see(tk.END)
                    puertos_abiertos.append(f"{puerto} ({nombre_servicio})")
            except Exception as exc:
                pass
                
    output_text_widget.insert(tk.END, "\n" + "-" * 50 + "\n")
    if puertos_abiertos:
        output_text_widget.insert(tk.END, "\nRESUMEN: Puertos abiertos encontrados:\n")
        output_text_widget.insert(tk.END, ", ".join(puertos_abiertos) + "\n")
    else:
        output_text_widget.insert(tk.END, "\nRESUMEN: No se encontraron puertos abiertos en el rango especificado.\n")
    output_text_widget.insert(tk.END, "-" * 50 + "\n")
    
    btn_iniciar.config(state=tk.NORMAL)
    btn_salir.config(state=tk.NORMAL)

class PortScannerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Araxmap")

        master.configure(bg='#f0f0f0')
        self.font_title = ('Helvetica', 16, 'bold')
        self.font_label = ('Helvetica', 10)
        self.font_button = ('Helvetica', 10, 'bold')

        self.ip_objetivo = tk.StringVar(value="127.0.0.1")
        self.puerto_inicio = tk.StringVar(value="1")
        self.puerto_fin = tk.StringVar(value="1024")
        self.timeout = tk.StringVar(value="0.5")

        main_frame = tk.Frame(master, padx=10, pady=10, bg='#f0f0f0')
        main_frame.pack(padx=10, pady=10)

        title_label = tk.Label(main_frame, text="Araxmap", font=self.font_title, bg='#f0f0f0', fg='#333333')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        tk.Label(main_frame, text="Dirección IP:", font=self.font_label, bg='#f0f0f0', anchor='w').grid(row=1, column=0, sticky='w', pady=5)
        self.ip_entry = tk.Entry(main_frame, textvariable=self.ip_objetivo, width=25, font=self.font_label)
        self.ip_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=5)

        tk.Label(main_frame, text="Puerto de Inicio:", font=self.font_label, bg='#f0f0f0', anchor='w').grid(row=2, column=0, sticky='w', pady=5)
        self.inicio_entry = tk.Entry(main_frame, textvariable=self.puerto_inicio, width=25, font=self.font_label)
        self.inicio_entry.grid(row=2, column=1, sticky='ew', pady=5, padx=5)

        tk.Label(main_frame, text="Puerto de Fin:", font=self.font_label, bg='#f0f0f0', anchor='w').grid(row=3, column=0, sticky='w', pady=5)
        self.fin_entry = tk.Entry(main_frame, textvariable=self.puerto_fin, width=25, font=self.font_label)
        self.fin_entry.grid(row=3, column=1, sticky='ew', pady=5, padx=5)

        tk.Label(main_frame, text="Timeout (seg):", font=self.font_label, bg='#f0f0f0', anchor='w').grid(row=4, column=0, sticky='w', pady=5)
        self.timeout_entry = tk.Entry(main_frame, textvariable=self.timeout, width=25, font=self.font_label)
        self.timeout_entry.grid(row=4, column=1, sticky='ew', pady=5, padx=5)

        tk.Frame(main_frame, height=1, bg='#cccccc').grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)

        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        self.btn_iniciar = tk.Button(button_frame, text="🚀 Iniciar Escaneo", command=self.iniciar_escaneo_thread, font=self.font_button, bg='#4CAF50', fg='white', relief=tk.RAISED, padx=10, pady=5)
        self.btn_iniciar.pack(side=tk.LEFT, padx=10)

        self.btn_salir = tk.Button(button_frame, text="❌ Salir", command=master.quit, font=self.font_button, bg='#f44336', fg='white', relief=tk.RAISED, padx=10, pady=5)
        self.btn_salir.pack(side=tk.LEFT, padx=10)

        tk.Frame(main_frame, height=1, bg='#cccccc').grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)

        tk.Label(main_frame, text="Resultados del Escaneo:", font=self.font_label, bg='#f0f0f0', anchor='w').grid(row=8, column=0, sticky='w', pady=5)
        self.output_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=50, height=15, font=('Consolas', 9), bg='black', fg='lime')
        self.output_text.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

    def validar_y_obtener_datos(self):
        try:
            ip = self.ip_objetivo.get().strip()
            inicio = int(self.puerto_inicio.get())
            fin = int(self.puerto_fin.get())
            timeout_val = float(self.timeout.get())

            if not ip:
                messagebox.showerror("Error de Entrada", "La dirección IP no puede estar vacía.")
                return None
            
            try:
                ip = socket.gethostbyname(ip)
            except socket.gaierror:
                messagebox.showerror("Error de Entrada", f"La dirección IP/Host '{ip}' no es válida o no se pudo resolver.")
                return None

            if inicio < 1 or fin > 65535 or inicio > fin:
                messagebox.showerror("Error de Rango", "El rango de puertos debe ser entre 1 y 65535, y el inicio debe ser menor o igual al fin.")
                return None
            
            if timeout_val <= 0:
                messagebox.showerror("Error de Timeout", "El valor de Timeout debe ser un número positivo.")
                return None

            return ip, [inicio, fin], timeout_val

        except ValueError:
            messagebox.showerror("Error de Entrada", "Los puertos y el timeout deben ser números válidos.")
            return None

    def iniciar_escaneo_thread(self):
        datos = self.validar_y_obtener_datos()
        if datos:
            ip, rango, timeout = datos
            thread = threading.Thread(target=escanear_puertos, args=(ip, rango, timeout, self.output_text, self.btn_iniciar, self.btn_salir))
            thread.daemon = True
            thread.start()

if __name__ == "__main__":
    root = tk.Tk() 
    app = PortScannerGUI(root)
    root.mainloop()