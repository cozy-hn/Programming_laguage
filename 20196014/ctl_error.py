class Error_controller:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.warnings, self.errors = list(), list()
            self.initialized = True
    
    def print_error(self):
        if self.warnings or self.errors:
            for i in self.warnings:
                print(f"(Warning): {i}")
            for i in self.errors:
                print(f"(Error): {i}")
            self.warnings.clear()
            self.errors.clear()
        else:
            print("(OK)")

    
    def add_error(self, error):
        self.errors.append(error)
    
    def add_warning(self, warning):
        self.warnings.append(warning)