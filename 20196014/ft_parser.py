# <program> → <statements>
# <statements> → <statement> | <statement><semi_colon><statements>
# <statement> → <ident><assignment_op><expression>
# <expression> →  <term><term_tail>
# <term_tail> → <add_op><term><term_tail> | ε
# <term> → <factor> <factor_tail>
# <factor_tail> → <mult_op><factor><factor_tail> | ε
# <factor> → <left_paren><expression><right_paren> | <ident> | <const>
# <const> → any decimal numbers
# <ident> → any names conforming to C identifier rules
# <assignment_op> → :=
# <semi_colon> → ;
# <add_operator> → + | -
# <mult_operator> → * | /
# <left_paren> → (
# <right_paren> → )

from lexical_analyzer import Lexical_Analyzer
from token import TokenType

class FT_Parser():
    def __init__(self, text) -> None:
        self.lexer = Lexical_Analyzer(text)
        self.ident_table = []
        self.ident_dict = {}
    
    def start(self):
        self.program()
        if self.lexer.next_token != TokenType.EOF:
            print("Error : EOF가 아닌 토큰이 남아있습니다")
            print("프로그램이 종료됩니다")
            exit(1)
        
    def program(self):
        self.lexer.lexical()
        self.statements()
        self.print_result()
        
    def statements(self):
        self.statement()
        self.print_token()
        if self.lexer.next_token == TokenType.SEMI_COLON:
            self.lexer.lexical()
            self.statements()
    
    def statement(self):
        if self.lexer.next_token == TokenType.IDENT:
            self.print_token()
            self.ident_table.append(self.lexer.token_string)
            self.ident_dict[self.lexer.token_string] = "Unknown"
            self.lexer.lexical()
            if self.lexer.next_token == TokenType.ASSIGNMENT_OP:
                self.print_token()
                self.lexer.lexical()
                self.expression()
            
    def expression(self):
        self.term()
        self.term_tail()
    
    def term_tail(self):
        if self.lexer.next_token == TokenType.ADD_OP:
            self.print_token()
            self.lexer.lexical()
            self.term()
            self.term_tail()
        
    def term(self):
        self.factor()
        self.factor_tail()

    def factor_tail(self):
        if self.lexer.next_token == TokenType.MULT_OP:
            self.print_token()
            self.lexer.lexical()
            self.factor()
            self.factor_tail()
    
    def factor(self):
        if self.lexer.next_token == TokenType.LEFT_PAREN:
            self.print_token()
            self.lexer.lexical()
            self.expression()
            if self.lexer.next_token == TokenType.RIGHT_PAREN:
                self.print_token()
                self.lexer.lexical()
        elif self.lexer.next_token == TokenType.IDENT:
            self.print_token()
            self.lexer.lexical()
        elif self.lexer.next_token == TokenType.CONST:
            self.print_token()
            self.lexer.lexical()
        else:
            self.lexer.lexical()
    
    def print_result(self):
        print("Result ==> ", end="")
        for i in self.ident_table[:-1]:
            print(f"{i}: {self.ident_dict[i]}; ", end="")
        if self.ident_table:
            last = self.ident_table[-1]
            print(f"{last}: {self.ident_dict[last]}")
    
    def print_token(self):
        if self.lexer.next_token == TokenType.EOF:
            print()
        elif self.lexer.next_token == TokenType.SEMI_COLON:
            print("\b; ")
        else:
            print(f"{self.lexer.token_string} ", end="")