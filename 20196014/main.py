from ctl_input import ctl_input
from ft_parser import FT_Parser

def main():
	content = ctl_input() +"\0"
	FT_Parser(content).start()

if __name__ == "__main__":
	main()
 