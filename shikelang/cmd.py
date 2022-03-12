import argparse

from shikelang.parser import parser
from shikelang.utils import clear_text
from shikelang.translation import VTable


def main():
    # parse arguments
    arg_parser = argparse.ArgumentParser(description="ShikeLang Interpreter")
    arg_parser.add_argument("-d", "--debug", action="store_true", help="whether to run program in debug mode")
    arg_parser.add_argument("filepath", help="path to code file")
    args = arg_parser.parse_args()

    # read codes
    code_string = clear_text(open(args.filepath, "r").read())

    # syntax parse
    if args.debug:
        from shikelang.tokenizer import lex_obj
        lex_obj.input(code_string)
        for token in lex_obj:
            print(token)
    root = parser.parse(code_string, debug=args.debug)
    if args.debug:
        print(root)
        root.print_node(0)

    # translation
    v_table = VTable()
    v_table.trans(root)
    if args.debug:
        print(v_table)


if __name__ == "__main__":
    main()
