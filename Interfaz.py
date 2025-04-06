import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RaizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de raíces")
        self.crear_interfaz()

    def crear_interfaz(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Entrada de función
        ttk.Label(frame, text="f(x):").grid(row=0, column=0, sticky=tk.W)
        self.funcion_entry = ttk.Entry(frame, width=40)
        self.funcion_entry.grid(row=0, column=1)

        # Selección de método
        ttk.Label(frame, text="Método:").grid(row=1, column=0, sticky=tk.W)
        self.metodo_var = tk.StringVar(value="newton")
        metodo_menu = ttk.OptionMenu(frame, self.metodo_var, "newton", "newton", "secante", command=self.actualizar_campos)
        metodo_menu.grid(row=1, column=1)

        # Valores iniciales
        self.x0_label = ttk.Label(frame, text="x0:")
        self.x0_label.grid(row=2, column=0, sticky=tk.W)
        self.x0_entry = ttk.Entry(frame)
        self.x0_entry.grid(row=2, column=1)

        #Grafica
        self.x1_label = ttk.Label(frame, text="x1:")
        self.x1_entry = ttk.Entry(frame)

        self.boton = ttk.Button(frame, text="Calcular raíz", command=self.calcular)
        self.boton.grid(row=4, column=0, columnspan=2, pady=10)

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.grid(row=1, column=0)

        self.actualizar_campos()

    def actualizar_campos(self, *args):
        metodo = self.metodo_var.get()
        if metodo == "secante":
            self.x1_label.grid(row=3, column=0, sticky=tk.W)
            self.x1_entry.grid(row=3, column=1)
        else:
            self.x1_label.grid_remove()
            self.x1_entry.grid_remove()

    def calcular(self):
        x = sp.Symbol('x')
        funcion_str = self.funcion_entry.get()
        metodo = self.metodo_var.get()

        try:
            f_expr = sp.sympify(funcion_str)
            f = sp.lambdify(x, f_expr, 'numpy')
        except:
            messagebox.showerror("Error", "La función ingresada no es válida.")
            return

        try:
            x0 = float(self.x0_entry.get())
        except:
            messagebox.showerror("Error", "x0 debe ser un número.")
            return

        try:
            if metodo == "newton":
                df_expr = sp.diff(f_expr, x)
                df = sp.lambdify(x, df_expr, 'numpy')
                if df(x0) == 0:
                    raise ValueError("La derivada en x0 es cero. Elige otro valor inicial.")
                raiz = self.newton_raphson(f, df, x0)
            elif metodo == "secante":
                try:
                    x1 = float(self.x1_entry.get())
                except:
                    messagebox.showerror("Error", "x1 debe ser un número.")
                    return

                if x0 == x1:
                    raise ValueError("x0 y x1 deben ser distintos.")
                raiz = self.secante(f, x0, x1)
            else:
                return

            messagebox.showinfo("Resultado", f"Raíz aproximada encontrada: {raiz:.6f}")
            self.graficar(f, raiz)
        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))
        except Exception as e:
            print("Error inesperado:", e)
            messagebox.showerror("Error", str(e))

    def newton_raphson(self, f, df, x0, tol=1e-6, max_iter=100):
        for _ in range(max_iter):
            fx = f(x0)
            dfx = df(x0)
            if dfx == 0:
                raise ValueError("Derivada cero durante la iteración.")
            x1 = x0 - fx / dfx
            if abs(x1 - x0) < tol:
                return x1
            x0 = x1
        raise ValueError("No se encontró convergencia.")

    def secante(self, f, x0, x1, tol=1e-6, max_iter=100):
        for _ in range(max_iter):
            fx0 = f(x0)
            fx1 = f(x1)
            if fx1 - fx0 == 0:
                raise ValueError("Diferencia cero en el denominador.")
            x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            if abs(x2 - x1) < tol:
                return x2
            x0, x1 = x1, x2
        raise ValueError("No se encontró convergencia.")

    def graficar(self, f, raiz):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        x_vals = np.linspace(raiz - 10, raiz + 10, 400)
        y_vals = f(x_vals)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_vals, y_vals, label='f(x)')
        ax.axhline(0, color='black', linewidth=0.8)
        ax.axvline(raiz, color='red', linestyle='--', label=f'Raíz ≈ {raiz:.4f}')
        ax.plot(raiz, f(raiz), 'ro')
        ax.set_title('Gráfica de la función')
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Ventana aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = RaizApp(root)
    root.mainloop()
