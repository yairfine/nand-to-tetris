class VMWriter:
    OPERATORS = {
        "+": "add",
        "-": "sub",
        "&": "and",
        "|": "or",
        "<": "lt",
        ">": "gt",
        "=": "eq",
        "add" : "add",
        "sub" : "sub",
        "and" : "and",
        "neg": "neg",
        "not": "not",
        "or" : "or",
        "lt" : "lt",
        "gt" : "gt",
        "eq" : "eq"
    }

    SEGMENT_BY_SYMBOL = {
        "arg": "argument",
        "field": "this",
        "var": "local",
    }

    def __init__(self, output_path):
        self.file = open(output_path, "w")

    def write_push(self, kind, index):
        segment = self.SEGMENT_BY_SYMBOL.get(kind, kind)
        vm_command = f"push {segment} {index}\n"
        self.file.write(vm_command)

    def write_pop(self, kind, index):
        segment = self.SEGMENT_BY_SYMBOL.get(kind, kind)
        vm_command = f"pop {segment} {index}\n"
        self.file.write(vm_command)

    def write_arithmetic(self, command):
        if command == "*":
            self.write_call("Math.multiply", 2)
        elif command == "/":
            self.write_call("Math.divide", 2)
        else:
            operator_name = self.OPERATORS[command]
            self.file.write(operator_name)
            self.file.write("\n")

    def write_label(self, label):
        vm_command = f"label {label}\n"
        self.file.write(vm_command)

    def write_goto(self, label):
        vm_command = f"goto {label}\n"
        self.file.write(vm_command)

    def write_if(self, label):
        vm_command = f"if-goto {label}\n"
        self.file.write(vm_command)

    def write_call(self, name, n_args):
        vm_command = f"call {name} {n_args}\n"
        self.file.write(vm_command)

    def write_function(self, name, n_locals):
        vm_command = f"function {name} {n_locals}\n"
        self.file.write(vm_command)

    def write_return(self):
        self.file.write("return\n")

    def close(self):
        self.file.close()
