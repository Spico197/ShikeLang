from curses.ascii import isdigit
import json


class VTable(object):
    def __init__(self) -> None:
        self.v_table = {}

    def update_v_table(self, name, value):
        self.v_table[name] = value

    @staticmethod
    def is_slice(name):
        return "[SLICE]" == name

    def trans(self, node):
        # Assignment
        if node.getdata() == "[ASSIGNMENT]":
            """assignment : VARIABLE '=' NUMBER
            | VARIABLE '=' VARIABLE
            | VARIABLE '=' operation
            | VARIABLE '=' slice
            | slice '=' slice
            | slice '=' VARIABLE"""
            if not self.is_slice(node.getchild(0).getdata()):
                if node.getchild(2).getdata() == "[OPERATION]" or self.is_slice(
                    node.getchild(2).getdata()
                ):
                    self.trans(node.getchild(2))
                    value = node.getchild(2).getvalue()
                elif node.getchild(2).getdata() in self.v_table:
                    value = self.v_table[node.getchild(2).getdata()]
                else:
                    value = node.getchild(2).getvalue()
                node.getchild(0).setvalue(value)
                self.update_v_table(node.getchild(0).getdata(), value)
            else:
                # slice
                self.trans(node.getchild(0))
                if self.is_slice(node.getchild(2).getdata()):
                    self.trans(node.getchild(2))
                    slice_ = node.getchild(0)
                    i = slice_.slice_index
                    self.v_table[slice_.slice_variable][i] = node.getchild(2).getvalue()
                    node.getchild(0).setvalue(self.v_table[slice_.slice_variable][i])
                else:  # variable
                    slice_ = node.getchild(0)
                    i = slice_.slice_index
                    self.v_table[slice_.slice_variable][i] = self.v_table[
                        node.getchild(2).getdata()
                    ]
                    node.getchild(0).setvalue(self.v_table[slice_.slice_variable][i])

        # declaration
        elif node.getdata() == "[DECLARATION]":
            type_ = node.getchild(0).getdata()
            var_name = node.getchild(1).getchild(0).getdata()
            if var_name in self.v_table:
                raise RuntimeError(f"Variable {var_name} declared again!")
            type_convert_func = {
                "int": int,
                "bool": bool,
            }[type_]
            self.trans(node.getchild(1))
            if self.is_slice(var_name):
                raise NotImplementedError
            else:
                self.v_table[var_name] = type_convert_func(self.v_table[var_name])

        # Operation
        elif node.getdata() == "[OPERATION]":
            """operation : VARIABLE '+' VARIABLE
            | VARIABLE '-' VARIABLE
            | VARIABLE '-' NUMBER
            | VARIABLE '+' NUMBER
            | '[' commaexpression ']'
            | LEN '(' VARIABLE ')'
            | '(' VARIABLE '+' VARIABLE ')' GDIV NUMBER"""
            if len(node._children) == 4:
                node.setvalue(len(self.v_table[node.getchild(2).getdata()]))
            elif node.getchild(1).getdata() == "+":
                arg0 = self.v_table[node.getchild(0).getdata()]
                if node.getchild(2).getdata() in self.v_table:
                    arg1 = self.v_table[node.getchild(2).getdata()]
                else:
                    arg1 = node.getchild(2).getvalue()
                node.setvalue(arg0 + arg1)
            elif node.getchild(1).getdata() == "-":
                arg0 = self.v_table[node.getchild(0).getdata()]
                if node.getchild(2).getdata() in self.v_table:
                    arg1 = self.v_table[node.getchild(2).getdata()]
                else:
                    arg1 = node.getchild(2).getvalue()
                node.setvalue(arg0 - arg1)
            elif len(node._children) == 7:
                var1 = self.v_table[node.getchild(1).getdata()]
                var2 = self.v_table[node.getchild(3).getdata()]
                num = node.getchild(6).getvalue()
                node.setvalue((var1 + var2) // num)
            else:
                # commaexpression
                self.trans(node.getchild(1))
                node.setvalue(eval("[{}]".format(node.getchild(1).getvalue())))

        # Print
        elif node.getdata() == "[SHIT]":
            """shit : SHIT LCLOSE VARIABLE RCLOSE
                    | SHIT LCLOSE STRING RCLOSE """
            arg0 = node.getchild(2).getvalue()
            if arg0 is None and node.getchild(2).getdata() in self.v_table:
                arg0 = self.v_table[node.getchild(2).getdata()]
            print(arg0)

        # If
        elif node.getdata() == "[IF]":
            r"""IF [CONDITION] [STATEMENTS]
            IF [CONDITION] [STATEMENTS] [CONDITION] [STATEMENTS] [STATEMENTS]"""
            children = node.getchildren()
            if len(children) == 5:
                if self.trans(children[0]):
                    v = self.trans(children[1])
                    if v == "[BREAK]":
                        node.setvalue("[BREAK]")
                elif self.trans(children[2]):
                    v = self.trans(children[3])
                    if v == "[BREAK]":
                        node.setvalue("[BREAK]")
                else:
                    v = self.trans(children[4])
                    if v == "[BREAK]":
                        node.setvalue("[BREAK]")

            elif len(children) == 2:
                self.trans(children[0])
                condition = children[0].getvalue()
                if condition:
                    for c in children[1:]:
                        self.trans(c)

        elif node.getdata() == "[FOR]":
            r"""FOR : assignment condition VARIABLE statements"""
            children = node.getchildren()
            self.trans(children[0])
            while self.trans(children[1]):
                for c in children[3:]:
                    self.trans(c)
                self.update_v_table(
                    children[2].getdata(), self.v_table[children[2].getdata()] + 1
                )

        # While
        elif node.getdata() == "[WHILE]":
            r"""while : WHILE '(' condition ')' '{' statements '}'"""
            children = node.getchildren()
            while self.trans(children[0]):
                v = self.trans(children[1])
                if v == "[BREAK]":
                    break

        # do-until
        elif node.getdata() == "[DO_UNTIL]":
            statements, condition = node.getchildren()
            v = self.trans(statements)
            while not self.trans(condition):
                v = self.trans(statements)
                if v == "[BREAK]":
                    break

        # Condition
        elif node.getdata() == "[CONDITION]":
            """condition : VARIABLE '>' VARIABLE
            | VARIABLE '<' VARIABLE
            | VARIABLE LET VARIABLE
            | slice '>' VARIABLE
            | slice '<' VARIABLE"""
            op = node.getchild(1).getdata()
            if self.is_slice(node.getchild(0).getdata()):
                self.trans(node.getchild(0))
                v = node.getchild(0).slice_variable
                i = node.getchild(0).slice_index
                arg0 = self.v_table[v][i]
                if node.getchild(2).getdata() == str(node.getchild(2).getvalue()) and isdigit(node.getchild(2).getvalue()):
                    arg1 = node.getchild(2).getvalue()
                elif node.getchild(2).getdata() in ["true", "false"] and node.getchild(2).getvalue() is None:
                    arg1 = {"true": True, "false": False}[node.getchild(2).getdata()]
                else:
                    arg1 = self.v_table[node.getchild(2).getdata()]
            else:
                arg0 = self.v_table[node.getchild(0).getdata()]
                if node.getchild(2).getdata() == str(node.getchild(2).getvalue()) and isdigit(node.getchild(2).getvalue()):
                    arg1 = node.getchild(2).getvalue()
                elif node.getchild(2).getdata() in ["true", "false"] and node.getchild(2).getvalue() is None:
                    arg1 = {"true": True, "false": False}[node.getchild(2).getdata()]
                else:
                    arg1 = self.v_table[node.getchild(2).getdata()]
            if op == ">":
                node.setvalue(arg0 > arg1)
            elif op == "<":
                node.setvalue(arg0 < arg1)
            elif op == "==":
                node.setvalue(arg0 == arg1)
            elif op == "<=":
                node.setvalue(arg0 <= arg1)
            elif op == ">=":
                node.setvalue(arg0 >= arg1)

        elif node.getdata() == "[SLICE]":
            node.slice_variable = node.getchild(0).getdata()
            v = self.v_table[node.getchild(0).getdata()]
            node.slice_index = int(self.v_table[node.getchild(2).getdata()])
            i = node.slice_index
            node.setvalue(v[i])

        elif node.getdata() == "[COMMAEXPRESSION]":
            """commaexpression : commaexpression ',' NUMBER
            | NUMBER ',' NUMBER
            | NUMBER"""
            if len(node._children) == 1:
                node.setvalue(node.getchild(0).getvalue())
            else:
                if node.getchild(0).getdata() == "[COMMAEXPRESSION]":
                    self.trans(node.getchild(0))
                node.setvalue(
                    "{},{}".format(
                        node.getchild(0).getvalue(), node.getchild(1).getvalue()
                    )
                )

        elif node.getdata() == "[BREAK]":
            node.setvalue("[BREAK]")

        else:
            for c in node.getchildren():
                v = self.trans(c)
                if v == "[BREAK]":
                    node.setvalue("[BREAK]")

        return node.getvalue()

    def __str__(self):
        return json.dumps(self.v_table, indent=2, ensure_ascii=False)

    def __repr__(self) -> str:
        return f"<VTable: #Items: {len(self.v_table)}>"
