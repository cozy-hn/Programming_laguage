from token import TokenType
from ctl_error import Error_controller
class Lexical_Analyzer:	
	def __init__(self,text) -> None: 
		self.next_token = None# 다음 토큰
		self.token_string = None # 토큰 문자열
		self.full_txt = text
		self.textlength = len(text) - 1 #'\0' 제거
		self.idx = 0 #텍스트 인덱스
		self.error = Error_controller()

	
	def is_whitespace(self) -> bool:
		return ord(self.full_txt[self.idx]) <= 32

	def is_unused_char(self) -> bool:
		rtn=ord(self.full_txt[self.idx+1])
		return (33<=rtn<=39 or 44<=rtn<=46 or rtn==60 or 62<=rtn<=64 or 91<=rtn<=94 or rtn==96 or 123<=rtn<=126)

	def lexical(self) -> None:
		while self.is_whitespace() and self.idx < self.textlength:
			self.idx += 1
		now = self.full_txt[self.idx]
		self.token_string = now
		if now == '+' or now == '-':
			self.next_token = TokenType.ADD_OP
		elif now == '*' or now == '/':
			self.next_token = TokenType.MULT_OP
		elif now == '(':
			self.next_token = TokenType.LEFT_PAREN
		elif now == ')':
			self.next_token = TokenType.RIGHT_PAREN
		elif now == ';':
			self.next_token = TokenType.SEMI_COLON
		elif now == ':':
			self.erase_unused_char()
			self.token_string += '='
			self.next_token = TokenType.ASSIGNMENT_OP
			if self.full_txt[self.idx+1] == '=':
				self.idx += 1
			else:
				self.error.add_warning(f"오타 수정 : ':'가 ':='로 변경되었습니다.")

		elif now == '=':
			self.erase_unused_char()
			if self.full_txt[self.idx+1] == ':':
				self.error.add_warning(f"오타 수정 : '=:'가 ':='로 변경되었습니다.")
				self.token_string = ':='
				self.idx += 1
				self.next_token = TokenType.ASSIGNMENT_OP
			else:
				self.next_token = TokenType.UNDEFINED
       
		elif now == '\0':
			self.next_token = TokenType.EOF
		elif now.isdigit():
			while self.full_txt[self.idx+1].isdigit() or self.is_unused_char():
				self.erase_unused_char()
				self.token_string += self.full_txt[self.idx+1]
				self.idx += 1
			self.next_token = TokenType.CONST
		elif now.isalpha() or now == '_':
			while self.full_txt[self.idx+1].isalnum() or self.full_txt[self.idx+1] == '_' or self.is_unused_char():
				self.erase_unused_char()
				self.token_string += self.full_txt[self.idx+1]
				self.idx += 1
			self.next_token = TokenType.IDENT
		else:
			self.next_token = TokenType.UNDEFINED
		self.idx += 1
		if self.next_token == TokenType.UNDEFINED:
			self.error.add_warning(f"Undefined token: '{self.full_txt[self.idx-1]}'가 제거되었습니다.")
			self.lexical()
   
	def erase_unused_char(self) -> None:
		while self.is_unused_char():
			self.error.add_warning(f"Undefined token: '{self.full_txt[self.idx+1]}'가 제거되었습니다.")
			self.idx += 1
      
			