import tkinter as tk
from tkinter import messagebox

class BisectionController:
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.setup_event_handlers()
        
    def setup_event_handlers(self):
        self.view.input_view.frame.bind("<Return>", lambda e: self.calculate_root())
        
        self.view.calculate_btn.config(command=self.calculate_root)
        self.view.clear_btn.config(command=self.clear_results)
        self.view.plot_btn.config(command=self.plot_function)
    
    def calculate_root(self):
        try:
            params = self.view.input_view.get_parameters()
            
            self.model.set_parameters(
                params['function'],
                params['a'],
                params['b'],
                params['tolerance'],
                params['max_iterations']
            )
            
            results = self.model.calculate()
            
            summary = self.model.get_summary()
            self.view.results_view.display_results(results, summary)
            
            self.plot_function()
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred: {str(e)}")
    
    def clear_results(self):
        self.view.results_view.clear_results()
        self.view.plot_view.initialize_plot()
        self.model.results = []
        self.model.root = None
    
    def plot_function(self):
        try:
            params = self.view.input_view.get_parameters()
            
            x_min = min(float(params['a']), float(params['b'])) - 1
            x_max = max(float(params['a']), float(params['b'])) + 1
            
            x_values, y_values = self.model.get_function_values(x_min, x_max)
            
            root = self.model.root if self.model.root else None
            a = float(params['a'])
            b = float(params['b'])
            
            self.view.plot_view.plot_function(x_values, y_values, root, a, b)
            
        except Exception as e:
            messagebox.showerror("Plot Error", f"Cannot plot function: {str(e)}")
            self.view.plot_view.initialize_plot()
    
    def run(self):
        self.view.root.mainloop()