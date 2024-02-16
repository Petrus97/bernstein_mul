from enum import Enum


class Lang(Enum):
    PYTHON = 0
    C = 1


class CodeGen:

    def __init__(self, target: int, lang: Lang = Lang.PYTHON):
        self.code: list[str] = []
        self.target = target
        self.lang = lang
        self.temporaries_list: dict[int, str] = {}
        self.counter = 0
        self.input_symbol = "n"
        self.__init_by_lang__()

    def __init_by_lang__(self):
        match self.lang:
            case Lang.PYTHON:
                self.code.append(
                    f"# Multiply by {self.target} using the fewest operations"
                )
                self.code.append(f"def multiply({self.input_symbol}: int):")

            case Lang.C:
                self.code.append(
                    f"// Multiply by {self.target} using the fewest operations"
                )
                self.code.append(f"int multiply(int {self.input_symbol})")
                self.code.append("{")

    def __check_src_target__(self, target: int, source: int) -> (str, str): # type: ignore
        source_sym, target_sym = "", ""
        # Check if source and target are the input symbol
        if source == 1:
            source_sym = self.input_symbol
        else:
            try:
                source_sym = self.temporaries_list[source]
            except KeyError:
                self.counter += 1
                source_sym = f"t{self.counter}"
                self.temporaries_list[source] = source_sym
        if target == 1:
            target_sym = self.input_symbol
        else:
            try:
                target_sym = self.temporaries_list[source]
            except KeyError:
                self.counter += 1
                target_sym = f"t{self.counter}"
                self.temporaries_list[source] = target_sym
        return (source_sym, target_sym)

    def __get_temp__(self, value: int) -> str:
        if value == 1:
            return self.input_symbol
        else:
            try:
                return self.temporaries_list[value]
            except KeyError:
                self.counter += 1
                temp = f"t{self.counter}"
                self.temporaries_list[value] = temp
                return temp

    def gen_shift(self, target: int, source: int, shift: int):
        # source_sym, target_sym = self.__check_src_target__(target, source)
        source_sym = self.__get_temp__(source)
        target_sym = self.__get_temp__(target)
        match self.lang:
            case Lang.PYTHON:
                self.code.append(f"\t{target_sym} = {source_sym} << {shift}")

            case Lang.C:
                self.code.append(f"\t{target_sym} = {source_sym} << {shift};")

    def gen_add(self, res: int, op1: int, op2: int):
        # source_sym, target_sym = self.__check_src_target__(target, source)
        op1_sym = self.__get_temp__(op1)
        op2_sym = self.__get_temp__(op2)
        res_sym = self.__get_temp__(res)
        match self.lang:
            case Lang.PYTHON:
                self.code.append(f"\t{res_sym} = {op1_sym} + {op2_sym}")

            case Lang.C:
                self.code.append(f"\t{res_sym} = {op1_sym} + {op2_sym};")

    def gen_sub(self, res: int, op1: int, op2: int):
        # source_sym, target_sym = self.__check_src_target__(target, source)
        op1_sym = self.__get_temp__(op1)
        op2_sym = self.__get_temp__(op2)
        res_sym = self.__get_temp__(res)
        match self.lang:
            case Lang.PYTHON:
                self.code.append(f"\t{res_sym} = {op1_sym} - {op2_sym}")

            case Lang.C:
                self.code.append(f"\t{res_sym} = {op1_sym} - {op2_sym};")

    def gen_negate(self, target: int, source: int):
        source_sym = self.__get_temp__(source)
        target_sym = self.__get_temp__(target)
        match self.lang:
            case Lang.PYTHON:
                self.code.append(f"\t{target_sym} = 0 - {source_sym}")

            case Lang.C:
                self.code.append(f"\t{target_sym} = 0 - {source_sym};")

    def gen_code(self):
        print("GENERATED CODE:")
        print("---------------")
        match self.lang:
            case Lang.PYTHON:
                self.code.append(f"\treturn {self.temporaries_list[self.target]}\n")

            case Lang.C:
                self.code.append(f"\treturn {self.temporaries_list[self.target]};")
                self.code.append("}\n")
        match self.lang:
            case Lang.PYTHON:
                print("\n".join(self.code))
                with open(f"./generated/python/multiply.py", "w") as f:
                    f.write("\n".join(self.code))

            case Lang.C:
                # add the declarations of the temporary variables to the code
                self.code.insert(3, "\tint " + ", ".join(self.temporaries_list.values()) + ";")
                print("\n".join(self.code))
                # write to file
                with open(f"./generated/c/multiply.c", "w") as f:
                    f.write("\n".join(self.code))
        print("---------------")
