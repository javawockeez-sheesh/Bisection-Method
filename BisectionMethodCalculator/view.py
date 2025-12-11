import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class MainView:  
    def __init__(self, root):
        self.root = root
        self.root.title("BisectionMethodCalculator")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        self.input_view = InputView(self.main_frame)
        self.results_view = ResultsView(self.main_frame)
        self.plot_view = PlotView(self.main_frame)
        
        self.create_buttons()
        
        self.layout_views()
        
    def create_buttons(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        self.calculate_btn = ttk.Button(button_frame, text="Calculate Root")
        self.calculate_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="Clear Results")
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.plot_btn = ttk.Button(button_frame, text="Plot Function")
        self.plot_btn.pack(side=tk.LEFT, padx=5)
        
    def layout_views(self):
        self.input_view.frame.grid(row=1, column=0, columnspan=3, 
        sticky=(tk.W, tk.E), pady=(0, 10))
    
        self.results_view.frame.grid(row=6, column=0, columnspan=3, 
        sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.plot_view.frame.grid(row=8, column=0, columnspan=3, 
        sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.main_frame.rowconfigure(6, weight=1)
        self.main_frame.rowconfigure(8, weight=1)


class InputView:
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.LabelFrame(parent, text="Input Parameters", padding="10")
        
        self.function_var = tk.StringVar(value="x**3 - x - 2")
        self.a_var = tk.StringVar(value="1")
        self.b_var = tk.StringVar(value="2")
        self.tolerance_var = tk.StringVar(value="0.0001")
        self.max_iter_var = tk.StringVar(value="100")
        
        self.create_widgets()
        
    def create_widgets(self):
        ttk.Label(self.frame, text="Function f(x):", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.function_entry = ttk.Entry(self.frame, textvariable=self.function_var, width=40, font=("Arial", 10))
        self.function_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        ttk.Label(self.frame, text="Interval [a, b]:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        interval_frame = ttk.Frame(self.frame)
        interval_frame.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Label(interval_frame, text="a =", font=("Arial", 10)).pack(side=tk.LEFT)
        self.a_entry = ttk.Entry(interval_frame, textvariable=self.a_var, width=10, font=("Arial", 10))
        self.a_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        ttk.Label(interval_frame, text="b =", font=("Arial", 10)).pack(side=tk.LEFT)
        self.b_entry = ttk.Entry(interval_frame, textvariable=self.b_var, width=10, font=("Arial", 10))
        self.b_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        ttk.Label(self.frame, text="Tolerance:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.tolerance_entry = ttk.Entry(self.frame, textvariable=self.tolerance_var, width=20, font=("Arial", 10))
        self.tolerance_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Label(self.frame, text="Max Iterations:", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.max_iter_entry = ttk.Entry(self.frame, textvariable=self.max_iter_var, width=20, font=("Arial", 10))
        self.max_iter_entry.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        self.frame.columnconfigure(1, weight=1)
    
    def get_parameters(self):
        return {
            'function': self.function_var.get(),
            'a': self.a_var.get(),
            'b': self.b_var.get(),
            'tolerance': self.tolerance_var.get(),
            'max_iterations': self.max_iter_var.get()
        }


class ResultsView:
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.LabelFrame(parent, text="Results", padding="10")
        
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        self.create_widgets()
        
    def create_widgets(self):
        text_frame = ttk.Frame(self.frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.results_text = tk.Text(text_frame, height=10, width=80, font=("Courier", 9))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.summary_label = ttk.Label(self.frame, text="Enter parameters and click 'Calculate Root'", 
                                      font=("Arial", 10))
        self.summary_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
    
    def clear_results(self):
        self.results_text.delete(1.0, tk.END)
        self.summary_label.config(text="Results cleared")
    
    def display_results(self, results, summary):
        self.clear_results()

        header = f"{'Iter':^6} {'a':^12} {'b':^12} {'c':^12} {'f(c)':^12} {'Error':^12}\n"
        separator = "-" * 70 + "\n"
        self.results_text.insert(tk.END, header)
        self.results_text.insert(tk.END, separator)

        for result in results:
            line = f"{result['iter']:^6} {result['a']:^12.6f} {result['b']:^12.6f} "
            line += f"{result['c']:^12.6f} {result['f_c']:^12.6f} {result['error']:^12.6f}\n"
            self.results_text.insert(tk.END, line)
        
        self.summary_label.config(text=summary)


class PlotView:
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.LabelFrame(parent, text="Function Plot", padding="10")
        
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.initialize_plot()
    
    def initialize_plot(self):
        self.ax.clear()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('f(x)')
        self.ax.set_title('Function Graph')
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
    
    def plot_function(self, x_values, y_values, root=None, a=None, b=None):
        self.ax.clear()
        
        self.ax.plot(x_values, y_values, 'b-', linewidth=2, label='f(x)')

        self.ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)

        if root is not None:
            self.ax.axvline(x=root, color='r', linestyle='--', alpha=0.7, label=f'Root ≈ {root:.4f}')
        if a is not None:
            self.ax.axvline(x=a, color='g', linestyle=':', alpha=0.5, label=f'a = {a:.2f}')
        if b is not None:
            self.ax.axvline(x=b, color='g', linestyle=':', alpha=0.5, label=f'b = {b:.2f}')
        
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('f(x)')
        self.ax.set_title('Function Graph with Bisection Method')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        
        self.fig.tight_layout()
        self.canvas.draw()