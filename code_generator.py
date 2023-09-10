import code_blocks
import nodes

class CodeGenerator:

    def __init__(self, program):
        self.program = program
        self.symbol_table = {}
        self.output = ""

    def generate(self):
        for statement in self.program:
            self.generate_statement(statement)

        self.generate_data_table()
        return self.output
    
    def generate_statement(self, statement):
        if not hasattr(statement, "child"):
            return
        
        if isinstance(statement, nodes.PrintI):
            self.generate_print_i(statement.child)

        self.generate_statement(statement.child)

    def generate_data_table(self):
        for k in self.symbol_table.keys():
            self.output += code_blocks.data_entry.format(id=k, value=self.symbol_table[k])

    def get_symbol(self, value):
        existing_symbol = self.check_symbol_table(value)
        if existing_symbol:
            return existing_symbol
        
        symbol_key = f'id{len(self.symbol_table)}'
        self.symbol_table[symbol_key] = value
        return symbol_key

    def check_symbol_table(self, value):
        for k in self.symbol_table.keys():
            if self.symbol_table[k] == value:
                return k
        return False

    def generate_print_i(self, statement):
        if not isinstance(statement, nodes.IntCon):
            raise Exception("printi may only accept integers")
        value = statement.child
        symbol = self.get_symbol(value)
        self.output += code_blocks.print_integer.format(id=symbol)