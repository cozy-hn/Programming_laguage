from token import TokenType
class Lexical_Analyzer:
	def __init__(self,text) -> None: 
		self.next_token = None# 다음 토큰
		self.token_string = None # 토큰 문자열
		self.full_txt = text
		self.textlength = len(text) - 1 #'\0' 제거
		self.idx = 0 #텍스트 인덱스
	
	def whitespace(self) -> bool:
		return ord(self.full_txt[self.idx]) <= 32

	def lexical(self) -> None:
		while self.whitespace() and self.idx < self.textlength:
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
			if self.full_txt[self.idx+1] == '=':
				self.token_string += '='
				self.idx += 1
				self.next_token = TokenType.ASSIGNMENT_OP
		elif now == '\0':
			self.next_token = TokenType.EOF
		elif now.isdigit():
			while self.full_txt[self.idx+1].isdigit():
				self.token_string += self.full_txt[self.idx+1]
				self.idx += 1
			self.next_token = TokenType.CONST
		elif now.isalpha() or now == '_':
			while self.full_txt[self.idx+1].isalnum() or self.full_txt[self.idx+1] == '_':
				self.token_string += self.full_txt[self.idx+1]
				self.idx += 1
			self.next_token = TokenType.IDENT
		else:
			self.next_token = TokenType.UNDEFINED
		self.idx += 1
		if self.next_token == TokenType.UNDEFINED:
			self.lexical()
			