# -*- coding: utf-8 -*-
import argparse
import sys

def print_f(message, end="\n"):
    if not args.v:
        print(message, end=end)
    else:
        pass

def print_t(message, end="\n"):
    if args.v:
        print(message, end=end)
    else:
        pass

def ctl_input():
    parser = argparse.ArgumentParser(prog= "LL Parser",
                                     description="Principles of Programming Languages Fall, 2023 Programming Assignment 1 - Python")
    parser.add_argument('-v', action='store_true', help='출력-(b) 옵션으로 “-v”가 주어진 경우,\
            주어진 문법에 따라 입력파일에 저장되어 있는 프로그램을 분석하되 출력-(a)의 파싱되는 과정은 출력하지 않는다.\
            대신, 아래 처리 조건의 next_token 변수가 변경될 때마다 그 값을 출력한다.')
    parser.add_argument('filename', nargs='*', type=str, help='Only txt file')
    global args
    args = parser.parse_args()
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and args.v):
        print("Error : 텍스트 파일이 입력되지 않았습니다")
        print("프로그램이 종료됩니다")
        sys.exit()
    if len(sys.argv) > 3 or (len(sys.argv) == 3 and not args.v):
        print("Waring : 인자가 여러개 입니다. 첫번째 텍스트 파일만 사용됩니다.")
    try:
        with open(args.filename[0], 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error : 파일 {args.filename[0]}이 존재하지 않습니다.")
        sys.exit(1)
    except PermissionError:
        print(f"Error : 파일 {args.filename[0]}에 대한 권한이 없습니다.")
        sys.exit(1)
    print("\n"+" " * 10+"#" * 27)
    print(" " * 10+"#  LL Parser를 실행합니다 #")
    if args.v:
        print(" " * 10+"# option (b)를 실행합니다 #")
    else:
        print(" " * 10+"# option (a)를 실행합니다 #")
    print(" " * 10+"#" * 27+"\n")
    return content