import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import random
import json
import time

class GrammarGenerator:
    def __init__(self):
        self.rules = {}
        self.start_symbol = None

    def load_grammar(self, filepath):
        self.rules = {}
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line: continue
                    if "->" in line:
                        lhs, rhs = line.split("->")
                        lhs = lhs.strip()
                        prods = [p.strip().split() for p in rhs.split("|")]
                        if lhs not in self.rules:
                            self.rules[lhs] = []
                        self.rules[lhs].extend(prods)
                        if self.start_symbol is None:
                            self.start_symbol = lhs
            return True, f"Gramática cargada. Símbolo inicial: {self.start_symbol}"
        except Exception as e:
            return False, str(e)

    def generate_valid(self, symbol, current_depth, max_depth):
        # Evitar recursión infinita forzando terminales si excedemos profundidad
        if current_depth > max_depth:
            # Buscar producción simple (terminal o lo más corto posible)
            if symbol not in self.rules: return symbol # Es terminal
            # Intento simple: buscar regla sin el mismo símbolo (para evitar E->E+T)
            candidates = [p for p in self.rules[symbol] if symbol not in p]
            if not candidates: return "1" # Fallback seguro
            choice = random.choice(candidates)
        else:
            if symbol not in self.rules: return symbol
            choice = random.choice(self.rules[symbol])
        
        result = ""
        for s in choice:
            val = self.generate_valid(s, current_depth + 1, max_depth)
            result += val + " "
        return result.strip()

    def generate_extreme(self, symbol, current_depth, max_depth):
        # Fuerza profundidad priorizando reglas recursivas hasta llegar cerca del límite
        if current_depth < max_depth * 0.9:
            if symbol in self.rules:
                # Preferir reglas largas o recursivas
                choice = max(self.rules[symbol], key=len) 
            else:
                return symbol
        else:
            return self.generate_valid(symbol, current_depth, max_depth)

        result = ""
        for s in choice:
            result += self.generate_extreme(s, current_depth + 1, max_depth) + " "
        return result.strip()

    def mutate_string(self, valid_string):
        # Introduce errores sintácticos
        tokens = valid_string.split()
        mutation_type = random.choice(["duplicar_op", "eliminar_par", "insertar_basura"])
        
        if mutation_type == "duplicar_op" and len(tokens) > 2:
            # Busca un operador y lo duplica: "1 + 1" -> "1 ++ 1"
            idx = random.randint(1, len(tokens)-2)
            tokens.insert(idx, tokens[idx])
        
        elif mutation_type == "eliminar_par":
            if "(" in tokens: tokens.remove("(")
            elif ")" in tokens: tokens.remove(")")
            else: tokens.append(")") # Agregar par sin cerrar
            
        elif mutation_type == "insertar_basura":
            idx = random.randint(0, len(tokens))
            tokens.insert(idx, "@") # Simbolo ilegal
            
        return " ".join(tokens)

# --- INTERFAZ GRÁFICA ---
class App:
    def __init__(self, root):
        self.generator = GrammarGenerator()
        root.title("Generador de Casos de Prueba - Grupo 3")
        root.geometry("600x500")

        # Frame superior
        frame_top = tk.Frame(root)
        frame_top.pack(pady=10)
        
        tk.Button(frame_top, text="1. Cargar Gramática (.txt)", command=self.load_file).pack(side=tk.LEFT, padx=5)
        self.lbl_status = tk.Label(frame_top, text="No cargado", fg="red")
        self.lbl_status.pack(side=tk.LEFT, padx=5)

        # Configuración
        frame_config = tk.Frame(root)
        frame_config.pack(pady=5)
        tk.Label(frame_config, text="Cant. Casos:").pack(side=tk.LEFT)
        self.ent_qty = tk.Entry(frame_config, width=5); self.ent_qty.insert(0, "100")
        self.ent_qty.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_config, text="2. Generar Casos", command=self.run_generation, bg="#dddddd").pack(side=tk.LEFT, padx=20)

        # Log Area
        self.txt_log = scrolledtext.ScrolledText(root, width=70, height=20)
        self.txt_log.pack(pady=10)

        # Exportar
        tk.Button(root, text="3. Exportar JSON", command=self.export_json, bg="lightblue").pack(pady=5)
        
        self.results = []

    def load_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filename:
            ok, msg = self.generator.load_grammar(filename)
            self.lbl_status.config(text="Cargado" if ok else "Error", fg="green" if ok else "red")
            messagebox.showinfo("Carga", msg)

    def run_generation(self):
        if not self.generator.start_symbol:
            messagebox.showwarning("Error", "Cargue una gramática primero.")
            return

        try:
            qty = int(self.ent_qty.get())
            self.results = []
            self.txt_log.delete(1.0, tk.END)
            
            start_time = time.time()
            
            # Distribución: 60% validos, 25% invalidos, 15% extremos
            n_valid = int(qty * 0.6)
            n_invalid = int(qty * 0.25)
            n_extreme = qty - n_valid - n_invalid

            # Generar Válidos
            for _ in range(n_valid):
                s = self.generator.generate_valid(self.generator.start_symbol, 0, 10)
                self.results.append({"tipo": "valido", "cadena": s, "longitud": len(s.split())})

            # Generar Inválidos
            for _ in range(n_invalid):
                base = self.generator.generate_valid(self.generator.start_symbol, 0, 5)
                s = self.generator.mutate_string(base)
                self.results.append({"tipo": "invalido", "cadena": s, "error": "sintaxis"})

            # Generar Extremos
            for _ in range(n_extreme):
                s = self.generator.generate_extreme(self.generator.start_symbol, 0, 20)
                self.results.append({"tipo": "extremo", "cadena": s, "longitud": len(s.split()), "profundidad": "alta"})

            elapsed = time.time() - start_time
            
            # Reporte en pantalla
            report = f"Generación completada en {elapsed:.4f} seg.\n"
            report += f"Total: {qty} | Válidos: {n_valid} | Inválidos: {n_invalid} | Extremos: {n_extreme}\n"
            report += "-"*50 + "\n"
            for i, res in enumerate(self.results[:10]): # Mostrar primeros 10
                report += f"{res['tipo'].upper()}: {res['cadena']}\n"
            
            self.txt_log.insert(tk.END, report)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_json(self):
        if not self.results: return
        f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if f:
            with open(f, 'w') as outfile:
                json.dump(self.results, outfile, indent=4)
            messagebox.showinfo("Éxito", "Archivo JSON guardado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()