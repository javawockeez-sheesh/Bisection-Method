import numpy as np

class FunctionEvaluator:   
    @staticmethod
    def safe_eval(expr, x_value):
        safe_dict = {
            'x': x_value,
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'exp': np.exp,
            'log': np.log,
            'log10': np.log10,
            'sqrt': np.sqrt,
            'pi': np.pi,
            'e': np.e,
            'abs': abs,
            'pow': pow,
        }
        
        try:
            result = eval(expr, {"__builtins__": {}}, safe_dict)
            return result
        except Exception as e:
            raise ValueError(f"Error evaluating function: {e}")


class BisectionMethod:   
    def __init__(self):
        self.function_str = ""
        self.a = 0.0
        self.b = 0.0
        self.tolerance = 0.0001
        self.max_iterations = 100
        self.results = []
        self.root = None
        self.final_error = None
        self.iterations = 0
        
    def set_parameters(self, function_str, a, b, tolerance, max_iterations):
        self.function_str = function_str
        self.a = float(a)
        self.b = float(b)
        self.tolerance = float(tolerance)
        self.max_iterations = int(max_iterations)
        self.results = []
        
    def validate_interval(self):
        if self.a >= self.b:
            raise ValueError("Interval a must be less than b")
            
        f_a = FunctionEvaluator.safe_eval(self.function_str, self.a)
        f_b = FunctionEvaluator.safe_eval(self.function_str, self.b)
        
        if f_a * f_b > 0:
            raise ValueError(
                f"f(a) * f(b) = {f_a * f_b:.4f} > 0. "
                f"Bisection method requires f(a) and f(b) to have opposite signs."
            )
        return f_a, f_b
    
    def calculate(self):
        f_a, f_b = self.validate_interval()
        
        a = self.a
        b = self.b
        iteration = 0
        error = abs(b - a)
        
        self.results = []
        
        while error > self.tolerance and iteration < self.max_iterations:
            c = (a + b) / 2
            f_c = FunctionEvaluator.safe_eval(self.function_str, c)
            
            result = {
                'iter': iteration,
                'a': a,
                'b': b,
                'c': c,
                'f_c': f_c,
                'error': error
            }
            self.results.append(result)
            
            if f_a * f_c < 0:
                b = c
                f_b = f_c
            else:
                a = c
                f_a = f_c
            
            error = abs(b - a)
            iteration += 1
        
        self.root = (a + b) / 2
        self.final_error = error
        self.iterations = iteration
        
        return self.results
    
    def get_summary(self):
        if self.root is None:
            return "No calculation performed yet."
        
        f_root = FunctionEvaluator.safe_eval(self.function_str, self.root)
        
        summary = f"Root found at x = {self.root:.4f}\n"
        summary += f"f(root) = {f_root:.4f}\n"
        summary += f"Iterations: {self.iterations}\n"
        summary += f"Final error: {self.final_error:.4f}"
        
        return summary
    
    def get_function_values(self, x_min=None, x_max=None, num_points=200):
        if x_min is None:
            x_min = min(self.a, self.b) - 1
        if x_max is None:
            x_max = max(self.a, self.b) + 1
            
        x_values = np.linspace(x_min, x_max, num_points)
        y_values = []
        
        for x in x_values:
            try:
                y = FunctionEvaluator.safe_eval(self.function_str, x)
                y_values.append(y)
            except:
                y_values.append(np.nan)
        
        return x_values, y_values