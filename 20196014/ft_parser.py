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

import sys
from lexical_analyzer import Lexical_Analyzer
from token import TokenType
from ctl_error import Error_controller
from ctl_input import ctl_input

class FT_Parser:
    def __init__(self) -> None:
        self.lexer = None
        self.ident_table, self.ident_dict = list(), dict()
        self.info = {"ident_num": 0, "const_num": 0, "operator_num": 0, "left_paren_num": 0, "right_paren_num": 0}
        self.error = Error_controller()
        self.cal_stack = list()

    def start(self):
        content = ctl_input() +"\0"
        self.lexer = Lexical_Analyzer(content)
        self.program()
        if self.lexer.next_token != TokenType.EOF:
            print("Error : EOF가 아닌 토큰이 남아있습니다")
            print("프로그램이 종료됩니다")
            sys.exit(1)
        
    def program(self):
        self.lexer.lexical()
        self.statements()
        self.print_result()
        
    def statements(self):
        self.reset_info()
        self.statement()
        while self.lexer.next_token != TokenType.EOF and self.lexer.next_token != TokenType.SEMI_COLON:
            self.error.add_warning(f"예상 TokenType.SEMI_COLON, TokenType.EOF, 현재 {self.lexer.next_token} => {self.lexer.token_string} 생략")
            self.lexer.lexical()
        self.print_token()
        self.print_info()
        self.error.print_error()
        if self.lexer.next_token == TokenType.SEMI_COLON:
            self.lexer.lexical()
            self.statements()
    
    def statement(self):
        while self.lexer.next_token != TokenType.IDENT and self.lexer.next_token != TokenType.EOF and self.lexer.next_token != TokenType.SEMI_COLON:
            self.error.add_warning(f"예상 TokenType.IDENT, 현재 {self.lexer.next_token} => {self.lexer.token_string} 생략")
            self.lexer.lexical()
        if self.lexer.next_token == TokenType.IDENT:
            LHS = self.lexer.token_string
            self.info["ident_num"] += 1
            self.print_token()
            self.ident_table.append(LHS)
            self.ident_dict[LHS] = "Unknown"
            self.lexer.lexical()
            while self.lexer.next_token != TokenType.ASSIGNMENT_OP and self.lexer.next_token != TokenType.EOF \
                and self.lexer.next_token != TokenType.SEMI_COLON:
                self.error.add_warning(f"예상 TokenType.ASSIGNMENT_OP, 현재 {self.lexer.next_token} => {self.lexer.token_string} 생략")
                self.lexer.lexical()
            if self.lexer.next_token == TokenType.ASSIGNMENT_OP:
                self.print_token()
                self.lexer.lexical()
                while self.lexer.next_token != TokenType.IDENT and self.lexer.next_token != TokenType.CONST \
                    and self.lexer.next_token != TokenType.LEFT_PAREN and self.lexer.next_token != TokenType.EOF and self.lexer.next_token != TokenType.SEMI_COLON:
                    if self.lexer.next_token == TokenType.ASSIGNMENT_OP:
                        self.error.add_warning(f"중복된 ASSIGNMENT_OP => {self.lexer.token_string} 생략")
                    else:
                        self.error.add_warning(f"예상 TokenType.IDENT, TokenType.CONST, TokenType.LEFT_PAREN, 현재 {self.lexer.next_token} => {self.lexer.token_string} 생략")
                    self.lexer.lexical()
                self.expression()
                if self.cal_stack:
                    self.ident_dict[LHS] = self.cal_stack.pop()
            else:
                self.error.add_error("Error : ASSIGNMENT_OP가 없어 문법에 맞지 않습니다")
        else:
            self.error.add_error("Error : IDENT가 없어 문법에 맞지 않습니다")

            
    def expression(self):
        while self.lexer.next_token != TokenType.IDENT and self.lexer.next_token != TokenType.CONST \
            and self.lexer.next_token != TokenType.LEFT_PAREN and self.lexer.next_token != TokenType.EOF and self.lexer.next_token != TokenType.SEMI_COLON:
            self.error.add_warning(f"예상 TokenType.IDENT, TokenType.CONST, TokenType.LEFT_PAREN, 현재 {self.lexer.next_token} => {self.lexer.token_string} 생략")
            self.lexer.lexical()
        self.term()
        self.term_tail()
    
    def term_tail(self):
        if self.lexer.next_token == TokenType.ADD_OP:
            self.info["operator_num"] += 1
            self.print_token()
            now_op = self.lexer.token_string
            self.lexer.lexical()
            while self.lexer.next_token != TokenType.IDENT and self.lexer.next_token != TokenType.CONST \
                and self.lexer.next_token != TokenType.LEFT_PAREN and self.lexer.next_token != TokenType.EOF and self.lexer.next_token != TokenType.SEMI_COLON:
                if self.lexer.next_token == TokenType.ADD_OP:
                    self.error.add_warning(f"중복된 ADD_OP => {self.lexer.token_string} 생략")
                else:
                    self.error.add_warning(f"덧셈 연산자 뒤에 바로 존재해서는 안되는 토큰이 나옴 => {self.lexer.token_string} 생략")
                self.lexer.lexical()
            self.term()
            self.calculate(now_op)
            self.term_tail()
        
    def term(self):
        self.factor()
        self.factor_tail()

    def factor_tail(self):
        while self.lexer.next_token == TokenType.RIGHT_PAREN and self.info["left_paren_num"] <= self.info["right_paren_num"]:
            self.error.add_warning(f" ')'가 불필요하게 나옴 => {self.lexer.token_string} 생략")
            self.lexer.lexical()
        if self.lexer.next_token == TokenType.MULT_OP:
            self.info["operator_num"] += 1
            self.print_token()
            now_op = self.lexer.token_string
            self.lexer.lexical()
            while self.lexer.next_token != TokenType.IDENT and self.lexer.next_token != TokenType.CONST \
                and self.lexer.next_token != TokenType.LEFT_PAREN and self.lexer.next_token != TokenType.EOF and self.lexer.next_token != TokenType.SEMI_COLON:
                if self.lexer.next_token == TokenType.MULT_OP:
                    self.error.add_warning(f"중복된 MULT_OP => {self.lexer.token_string} 생략")
                else:
                    self.error.add_warning(f"곱셈 연산자 뒤에 바로 존재해서는 안되는 토큰이 나옴 => {self.lexer.token_string} 생략")
                self.lexer.lexical()
            self.factor()
            self.calculate(now_op)
            self.factor_tail()
    
    def factor(self):
        while self.lexer.next_token != TokenType.IDENT and self.lexer.next_token != TokenType.CONST \
            and self.lexer.next_token != TokenType.LEFT_PAREN and self.lexer.next_token != TokenType.EOF and self.lexer.next_token != TokenType.SEMI_COLON:
            self.error.add_warning(f"예상 TokenType.IDENT, TokenType.CONST, TokenType.LEFT_PAREN, 현재 {self.lexer.next_token} => {self.lexer.token_string} 생략")
            self.lexer.lexical()
        if self.lexer.next_token == TokenType.LEFT_PAREN:
            self.info["left_paren_num"] += 1
            self.print_token()
            self.lexer.lexical()
            self.expression()
            while self.lexer.next_token != TokenType.RIGHT_PAREN and self.lexer.next_token != TokenType.EOF and self.lexer.next_token != TokenType.SEMI_COLON:
                self.error.add_warning(f"예상 TokenType.RIGHT_PAREN, 현재 {self.lexer.next_token} => {self.lexer.token_string} 생략")
                self.lexer.lexical()
            if self.lexer.next_token == TokenType.RIGHT_PAREN:
                self.info["right_paren_num"] += 1
                self.print_token()
                self.lexer.lexical()
            else:
                while self.info["left_paren_num"] > self.info["right_paren_num"]:
                    self.info["right_paren_num"] += 1
                    self.error.add_warning(f"RIGHT_PAREN이 없어 문법에 맞지 않습니다, RIGHT_PAREN 추가")
                    print(") ", end="")
        elif self.lexer.next_token == TokenType.IDENT:
            self.info["ident_num"] += 1
            self.print_token()
            if self.ident_dict.get(self.lexer.token_string) is None:
                self.ident_table.append(self.lexer.token_string)
                self.ident_dict[self.lexer.token_string] = "Unknown"
                self.error.add_error(f'"정의되지 않은 변수({self.lexer.token_string})가 참조됨"')
            self.cal_stack.append(self.ident_dict[self.lexer.token_string])
            self.lexer.lexical()
        elif self.lexer.next_token == TokenType.CONST:
            self.info["const_num"] += 1
            self.print_token()
            self.cal_stack.append(self.lexer.token_string)
            self.lexer.lexical()
        else:
            self.error.add_error("Error : 연산이 완료되지 않았습니다")
            self.cal_stack.append('Unknown')
            
    
    def print_result(self):
        print("Result ==> ", end="")
        if not self.ident_table:
            print("None")
        self.ident_table.sort()
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
    
    def reset_info(self):
        self.info["ident_num"]=self.info["const_num"]=self.info["operator_num"]=self.info["left_paren_num"]=self.info["right_paren_num"]=0
        self.cal_stack.clear()
    
    def print_info(self):
        print(f"ID: {self.info['ident_num']}; CONST: {self.info['const_num']}; OP: {self.info['operator_num']};")
    
    def calculate(self, now_op):
        a,b=self.cal_stack.pop(),self.cal_stack.pop()
        if a=='Unknown' or b=='Unknown':
            self.cal_stack.append('Unknown')
        else:
            if int(a)==0 and now_op=='/':
                self.error.add_error(f'"0으로 나누기 연산이 있음 결과 => \"Unknown\""')
                self.cal_stack.append('Unknown')
            else:
                self.cal_stack.append(eval(f"{int(b)}{now_op}{int(a)}"))
