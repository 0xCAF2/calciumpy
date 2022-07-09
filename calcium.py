# Used for python2calcium.py
class Engine:
    def __init__(self, code_list):
        self.env = Environment(code_list)
        self.breakpoints = []
        self.parser = Parser()

    def run(self):
        while True:
            result = self.step()
            if result == RESULT_EXECUTED:
                continue
            elif result == RESULT_BREAKPOINT:
                return False
            elif result == RESULT_TERMINATED:
                return True

    def step(self):
        last_index = len(self.env.code)
        last_index -= 1
        if self.env.address.indent == 0:
            end_of_code = self.parser.parse(self.env.code[last_index])
            is_end_of_code = isinstance(end_of_code, EndOfCode)
            if not is_end_of_code:
                raise InvalidEndOfCodeError()
            end_of_code.execute(self.env)
            return RESULT_TERMINATED
        else:
            if self.env.address.line == last_index:
                return RESULT_TERMINATED
            line = self.env.code[self.env.address.line]
            command = self.parser.parse(line)
            command.execute(self.env)

            is_end_of_code = isinstance(command, EndOfCode)
            if is_end_of_code:
                return RESULT_TERMINATED

            self.env.skip_to_next_line()
            next_line = self.env.code[self.env.address.line]
            keyword = next_line[INDEX_KEYWORD]
            while keyword == KEYWORD_COMMENT or keyword == KEYWORD_IFS:
                command = self.parser.parse(next_line)
                command.execute(self.env)
                self.env.skip_to_next_line()
                next_line = self.env.code[self.env.address.line]
                keyword = next_line[INDEX_KEYWORD]

            if self.env.address.line in self.breakpoints:
                return RESULT_BREAKPOINT
            else:
                return RESULT_EXECUTED


# Keyword
KEYWORD_ASSIGNMENT = "="
KEYWORD_ADDITION = "+"
KEYWORD_SUBTRACTION = "-"
KEYWORD_MULTIPLICATION = "*"
KEYWORD_EXPONENTIATION = "**"
KEYWORD_DIVISION = "/"
KEYWORD_FLOOR_DIVISION = "//"
KEYWORD_REMAINDER = "%"

KEYWORD_COMPOUND_ADDITION = "+="
KEYWORD_COMPOUND_SUBTRACTION = "-="
KEYWORD_COMPOUND_MULTIPLICATION = "*="

KEYWORD_EQUAL = "=="
KEYWORD_NOT_EQUAL = "!="
KEYWORD_LESS_THAN = "<"
KEYWORD_LESS_THAN_OR_EQUAL = "<="
KEYWORD_GREATER_THAN = ">"
KEYWORD_GREATER_THAN_OR_EQUAL = ">="
KEYWORD_AND = "and"
KEYWORD_OR = "or"
KEYWORD_IS = "is"
KEYWORD_IS_NOT = "is not"
KEYWORD_IN = "in"
KEYWORD_NOT_IN = "not in"

KEYWORD_BIT_AND = "&"
KEYWORD_BIT_OR = "|"
KEYWORD_BIT_XOR = "^"
KEYWORD_LEFT_SHIFT = "<<"
KEYWORD_RIGHT_SHIFT = ">>"

KEYWORD_NOT = "not"
KEYWORD_NEGATIVE = "-_"
KEYWORD_BIT_NOT = "~"

KEYWORD_IFS = "ifs"
KEYWORD_IF = "if"
KEYWORD_ELIF = "elif"
KEYWORD_ELSE = "else"

KEYWORD_FOR_RANGE = "for range"
KEYWORD_FOR_EACH = "for each"
KEYWORD_WHILE = "while"
KEYWORD_BREAK = "break"
KEYWORD_CONTINUE = "continue"

KEYWORD_FUNC_DEF = "def"
KEYWORD_CALL = "call"
KEYWORD_RETURN = "return"

KEYWORD_CLASS_DEF = "class"

KEYWORD_TRY = "try"
KEYWORD_EXCEPT = "except"
KEYWORD_RAISE = "raise"

KEYWORD_VARIABLE = "var"
KEYWORD_ATTRIBUTE = "attr"
KEYWORD_SUBSCRIPT = "sub"

KEYWORD_COMMENT = "#"
KEYWORD_PASS = "pass"
KEYWORD_END_OF_CODE = "end"

# Index
INDEX_INDENT = 0
INDEX_OPTIONS = 1
INDEX_KEYWORD = 2

INDEX_ASSIGNMENT_LHS = 3  # Left Hand Side
INDEX_ASSIGNMENT_RHS = 4  # Right Hand Side

INDEX_CONDITION = 3

INDEX_FOR_RANGE_VARIABLE_NAME = 3
INDEX_FOR_RANGE_VALUES = 4

INDEX_FOR_EACH_ELEMENT_NAME = 3
INDEX_FOR_EACH_ITERABLE_NAME = 4

INDEX_FUNC_DEF_FUNC_NAME = 3
INDEX_FUNC_DEF_PARAMETERS = 4

INDEX_CALL_LHS = 3
INDEX_CALL_REFERENCE = 4
INDEX_CALL_ARGS = 5  # Arguments

INDEX_RETURN_VALUE = 3

INDEX_CLASS_DEF_CLASS_NAME = 3
INDEX_CLASS_DEF_SUPERCLASS_NAME = 4

INDEX_EXCEPT_TYPE_NAME = 3
INDEX_EXCEPT_OBJ_NAME = 4

INDEX_RAISE_EXCEPTION = 3
INDEX_RAISE_ARGS = 4

INDEX_EXPRESSION_KEYWORD = 0

INDEX_VARIABLE_NAME = 1

INDEX_ATTRIBUTE_OBJECT_NAME = 1
INDEX_ATTRIBUTE_PROPERTY_NAMES = 2

INDEX_SUBSCRIPT_REFERENCED_OBJECT = 1
INDEX_SUBSCRIPT_INDEX_EXPR = 2

INDEX_LEFT_OPERAND = 1
INDEX_RIGHT_OPERAND = 2

INDEX_UNARY_OPERAND = 1

# Result
RESULT_TERMINATED = 0
RESULT_EXECUTED = 1
RESULT_BREAKPOINT = 2


class Address:
    def __init__(self, indent, line):
        self.indent = indent
        self.line = line


def _copy_address(point):
    address = Address(point.indent, point.line)
    return address


# BlockKind
BLOCK_KIND_IFS = 0
BLOCK_KIND_IF_ELIF_ELSE = 1
BLOCK_KIND_FOR_RANGE = 2
BLOCK_KIND_FOR_EACH = 3
BLOCK_KIND_WHILE = 4
BLOCK_KIND_FUNC_CALL = 5
BLOCK_KIND_CLASS_DEF = 6
BLOCK_KIND_TRY = 7
BLOCK_KIND_EXCEPT = 8


class Block:
    def __init__(self, kind, address, begin, end):
        self.kind = kind
        self.address = _copy_address(address)
        self.begin = begin
        self.end = end


class Namespace:
    def __init__(self, nesting_scope, dictobj):
        self.nesting_scope = nesting_scope  # None is allowed
        self.dictobj = dictobj

    def register(self, name, obj):
        self.dictobj[name] = obj

    def lookup(self, name):
        if name in self.dictobj:
            return self.dictobj[name]
        else:
            raise NameNotFoundError(name)


class GlobalScope(Namespace):
    pass


class FuncScope(Namespace):
    pass


class ClassScope(Namespace):
    def get_attr(self):
        return self.dictobj


class Inaccessible:
    def evaluate(self, env):
        return self


class BuiltinFuncObj(Inaccessible):
    def __init__(self, name, body):
        self.name = name
        self.body = body
        self.selfclass = builtin_type.builtin_function_or_method


class Accessible:
    def evaluate(self, env):
        return self


class FuncObj(Accessible):
    def __init__(self, name, params, nesting_scope, address):
        self.name = name
        self.params = params
        self.nesting_scope = nesting_scope
        self.address = _copy_address(address)
        self.attributes = {}
        self.selfclass = builtin_type.function

    def get_attr(self, name):
        return self.attributes[name]

    def set_attr(self, name, value):
        self.attributes[name] = value
        return True


class MethodObj(Inaccessible):
    def __init__(self, instance, funcobj):
        self.instance = instance
        self.funcobj = funcobj
        self.selfclass = builtin_type.instance_method


class ClassObj(Accessible):
    def __init__(self, name, superclass, attributes):
        self.name = name
        self.superclass = superclass
        self.attributes = attributes

    def get_attr(self, name):
        if name in self.attributes:
            return self.attributes[name]
        else:
            attr = self.superclass.get_attr(name)
            return attr

    def set_attr(self, name, value):
        if self.attributes != None:
            self.attributes[name] = value
            return True
        else:
            return False

    def get_description(self):
        return "<class " + self.name + ">"


class Instance(Accessible):
    def __init__(self, selfclass):
        self.selfclass = selfclass
        self.attributes = {}

    def get_attr(self, name):
        try:
            attr = self.attributes[name]
            return attr
        except:
            classattr = self.selfclass.get_attr(name)
            is_funcobj = isinstance(classattr, FuncObj)
            if is_funcobj:
                methodobj = MethodObj(self, classattr)
                return methodobj
            else:
                return classattr

    def set_attr(self, name, value):
        self.attributes[name] = value
        return True


class Super(Accessible):
    def __init__(self, classobj, instance):
        self.classobj = classobj
        self.instance = instance
        self.selfclass = builtin_type.super

    def get_attr(self, name):
        currentclass = self.instance.selfclass
        while True:
            if currentclass == None:
                raise SuperCallFailedError()
            if self.classobj.name != currentclass.name:
                currentclass = currentclass.superclass
                continue
            else:
                superclass = currentclass.superclass
                if superclass == None:
                    raise SuperCallFailedError()

                funcobj = superclass.get_attr(name)
                is_funcobj = isinstance(funcobj, FuncObj)
                if funcobj == None or not is_funcobj:
                    raise SuperCallFailedError()

                methodobj = MethodObj(self.instance, funcobj)
                return methodobj

    def set_attr(self, name, value):
        return False


class Variable:
    def __init__(self, name):
        self.name = name

    def assign(self, obj, env):
        env.register(self.name, obj)

    def evaluate(self, env):
        value = env.lookup(self.name)
        return value


class Attribute:
    def __init__(self, objname, propertynames):
        self.objname = objname
        self.propertynames = propertynames

    def assign(self, value, env):
        instance = env.lookup(self.objname)
        target = instance
        length = len(self.propertynames)
        for i in range(length - 1):
            target = _get_attribute(target, self.propertynames[i])
        target.set_attr(self.propertynames[length - 1], value)

    def evaluate(self, env):
        instance = env.lookup(self.objname)
        try:
            target = instance
            for prop in self.propertynames:
                target = _get_attribute(target, prop)
            return target
        except:
            raise AttributeNotExistError(prop)


class Subscript:
    def __init__(self, objref, indexexpr):
        self.objref = objref
        self.indexexpr = indexexpr

    def assign(self, value, env):
        obj = self.lookup(env)
        is_str = isinstance(obj, str)
        if is_str:
            raise SubscriptNotAllowedError()

        index = env.evaluate(self.indexexpr)
        obj[index] = value

    def evaluate(self, env):
        obj = self.lookup(env)
        index = env.evaluate(self.indexexpr)
        try:
            value = obj[index]
            return value
        except:
            raise ValueNotFoundError()

    def lookup(self, env):
        obj = env.evaluate(self.objref)
        is_list = isinstance(obj, list)
        is_str = isinstance(obj, str)
        is_dict = isinstance(obj, dict)
        if is_list or is_str or is_dict:
            return obj
        else:
            raise SubscriptNotAllowedError()


class BuiltinType:
    def __init__(self):
        self.object = ClassObj("object", None, None)
        self.function = ClassObj("function", self.object, None)
        self.instance_method = ClassObj("instancemethod", self.object, None)
        self.super = ClassObj("super", self.object, None)
        self.builtin_function_or_method = ClassObj(
            "builtin_function_or_method", self.object, None
        )


builtin_type = BuiltinType()


class BinaryOperation:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def operate(self, env):
        l = env.evaluate(self.left)
        r = env.evaluate(self.right)
        op = self.operator
        try:
            if op == KEYWORD_ADDITION:
                return l + r
            elif op == KEYWORD_SUBTRACTION:
                return l - r
            elif op == KEYWORD_MULTIPLICATION:
                return l * r
            elif op == KEYWORD_EXPONENTIATION:
                return l**r
            elif op == KEYWORD_DIVISION:
                return l / r
            elif op == KEYWORD_FLOOR_DIVISION:
                return l // r
            elif op == KEYWORD_REMAINDER:
                return l % r
            elif op == KEYWORD_EQUAL:
                return l == r
            elif op == KEYWORD_NOT_EQUAL:
                return l != r
            elif op == KEYWORD_LESS_THAN:
                return l < r
            elif op == KEYWORD_LESS_THAN_OR_EQUAL:
                return l <= r
            elif op == KEYWORD_GREATER_THAN:
                return l > r
            elif op == KEYWORD_GREATER_THAN_OR_EQUAL:
                return l >= r
            elif op == KEYWORD_AND:
                return l and r
            elif op == KEYWORD_OR:
                return l or r
            elif op == KEYWORD_IS:
                return l is r
            elif op == KEYWORD_IS_NOT:
                return l is not r
            elif op == KEYWORD_IN:
                return l in r
            elif op == KEYWORD_NOT_IN:
                return l not in r
            elif op == KEYWORD_BIT_AND:
                return l & r
            elif op == KEYWORD_BIT_OR:
                return l | r
            elif op == KEYWORD_BIT_XOR:
                return l ^ r
            elif op == KEYWORD_LEFT_SHIFT:
                return l << r
            elif op == KEYWORD_RIGHT_SHIFT:
                return l >> r
            else:
                raise Exception()
        except:
            raise InvalidOperationError()


class UnaryOperation:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def operate(self, env):
        v = env.evaluate(self.operator)
        op = self.operator
        try:
            if op == KEYWORD_NOT:
                return not v
            elif op == KEYWORD_NEGATIVE:
                return -v
            elif op == KEYWORD_BIT_NOT:
                return ~v
            else:
                raise Exception()
        except:
            raise InvalidOperationError()


method_names = {
    "append": {},
    "pop": {},
    "insert": {},
    "find": {},
    "replace": {},
    "keys": {},
}


def _get_attribute(obj, name):
    is_list = isinstance(obj, list)
    if is_list:
        if name == "append" or name in method_names["append"]:

            def append(args, env):
                elem = env.evaluate(args[0])
                obj.append(elem)

            builtin_append = BuiltinFuncObj(name, append)
            return builtin_append
        elif name == "pop" or name in method_names["pop"]:

            def pop(args, env):
                length = len(args)
                try:
                    if length == 0:
                        value = obj.pop()
                    else:
                        index = env.evaluate(args[0])
                        value = obj.pop(index)
                    return value
                except:
                    raise CannotPopFromListError()

            builtin_pop = BuiltinFuncObj(name, pop)
            return builtin_pop
        elif name == "insert" or name in method_names["insert"]:

            def insert(args, env):
                index = env.evaluate(args[0])
                elem = env.evaluate(args[1])
                obj.insert(index, elem)

            builtin_insert = BuiltinFuncObj(name, insert)
            return builtin_insert
        else:
            raise MethodNotFoundError(name)

    is_str = isinstance(obj, str)
    if is_str:
        if name == "find" or name in method_names["find"]:

            def find(args, env):
                substr = env.evaluate(args[0])
                result = obj.find(substr)
                return result

            builtin_find = BuiltinFuncObj(name, find)
            return builtin_find
        elif name == "replace" or name in method_names["replace"]:

            def replace(args, env):
                from_str = env.evaluate(args[0])
                to_str = env.evaluate(args[1])
                new_str = obj.replace(from_str, to_str)
                return new_str

            builtin_replace = BuiltinFuncObj(name, replace)
            return builtin_replace
        else:
            raise MethodNotFoundError(name)

    is_dict = isinstance(obj, dict)
    if is_dict:
        if name == "keys" or name in method_names["keys"]:

            def keys(args, env):
                keys_list = obj.keys()
                return keys_list

            builtin_keys = BuiltinFuncObj(name, keys)
            return builtin_keys
        else:
            raise MethodNotFoundError(name)

    # ClassObj or Instance object
    attr = obj.get_attr(name)
    return attr


# Built-in function's name
BUILTIN_FUNC_NAME_PRINT = "print"
BUILTIN_FUNC_NAME_DICT = "dict"
BUILTIN_FUNC_NAME_INT = "int"
BUILTIN_FUNC_NAME_LEN = "len"
BUILTIN_FUNC_NAME_LIST = "list"
BUILTIN_FUNC_NAME_STR = "str"
BUILTIN_FUNC_NAME_SUPER = "super"
BUILTIN_FUNC_NAME_HASATTR = "hasattr"
BUILTIN_FUNC_NAME_ISINSTANCE = "isinstance"
BUILTIN_FUNC_NAME_ISSUBCLASS = "issubclass"


class Environment:
    def __init__(self, codelist):
        self.code = codelist
        self.global_context = GlobalScope(None, {})
        self.context = self.global_context
        self.address = Address(1, 0)  # (indent, line)
        self.callstack = []
        self.returned_value = None
        self.blocks = []
        self.exception = None
        self.parser = Parser()

        self.builtin_print = print

        def _dict(args, env):
            return {}

        builtin_dict = BuiltinFuncObj(BUILTIN_FUNC_NAME_DICT, _dict)
        self.global_context.register(BUILTIN_FUNC_NAME_DICT, builtin_dict)

        def _hasattr(args, env):
            obj = env.evaluate(args[0])
            attr_name = env.evaluate(args[1])
            has_attr = hasattr(obj, attr_name)
            return has_attr

        builtin_hasattr = BuiltinFuncObj(BUILTIN_FUNC_NAME_HASATTR, _hasattr)
        self.global_context.register(BUILTIN_FUNC_NAME_HASATTR, builtin_hasattr)

        def _int(args, env):
            value = env.evaluate(args[0])
            try:
                num = int(value)
                return num
            except:
                raise CannotParseInt()

        builtin_int = BuiltinFuncObj(BUILTIN_FUNC_NAME_INT, _int)
        self.global_context.register(BUILTIN_FUNC_NAME_INT, builtin_int)

        def _isinstance(args, env):
            instance = env.evaluate(args[0])
            classobj = env.evaluate(args[1])
            is_instance = isinstance(instance, Instance)
            is_classobj = isinstance(classobj, ClassObj)
            if is_classobj and is_instance:
                currentclass = instance.selfclass
                while True:
                    if currentclass == None:
                        return False
                    elif currentclass is classobj:
                        return True
                    else:
                        currentclass = currentclass.superclass
            else:
                is_builtin = isinstance(classobj, BuiltinFuncObj)
                if is_builtin:
                    builtin_funcobj = classobj
                    if builtin_funcobj.name == BUILTIN_FUNC_NAME_LIST:
                        is_list = isinstance(instance, list)
                        return is_list
                    elif builtin_funcobj.name == BUILTIN_FUNC_NAME_STR:
                        is_str = isinstance(instance, str)
                        return is_str
                    elif builtin_funcobj.name == BUILTIN_FUNC_NAME_DICT:
                        is_dict = isinstance(instance, dict)
                        return is_dict
                    else:
                        return False
                else:
                    return False

        builtin_isinstance = BuiltinFuncObj(BUILTIN_FUNC_NAME_ISINSTANCE, _isinstance)
        self.global_context.register(BUILTIN_FUNC_NAME_ISINSTANCE, builtin_isinstance)

        def _issubclass(args, env):
            classtype = env.evaluate(args[0])
            superclass = env.evaluate(args[1])
            is_subclass = issubclass(classtype, superclass)
            return is_subclass

        builtin_issubclass = BuiltinFuncObj(BUILTIN_FUNC_NAME_ISSUBCLASS, _issubclass)
        self.global_context.register(BUILTIN_FUNC_NAME_ISSUBCLASS, builtin_issubclass)

        def _len(args, env):
            value = env.evaluate(args[0])
            try:
                length = len(value)
                return length
            except:
                raise NotIterableError()

        builtin_len = BuiltinFuncObj(BUILTIN_FUNC_NAME_LEN, _len)
        self.global_context.register(BUILTIN_FUNC_NAME_LEN, builtin_len)

        def _list(args, env):
            iterable = env.evaluate(args[0])
            try:
                new_list = list(iterable)
                return new_list
            except:
                raise NotIterableError()

        builtin_list = BuiltinFuncObj(BUILTIN_FUNC_NAME_LIST, _list)
        self.global_context.register(BUILTIN_FUNC_NAME_LIST, builtin_list)

        def _print(args, env):
            description = ""
            length = len(args)
            count = 0
            for arg in args:
                value = env.evaluate(arg)
                desc = _get_description(value)
                description += desc
                if count < length - 1:
                    description += " "
            self.builtin_print(description)
            return None

        builtin_print = BuiltinFuncObj(BUILTIN_FUNC_NAME_PRINT, _print)
        self.global_context.register(BUILTIN_FUNC_NAME_PRINT, builtin_print)

        def _str(args, env):
            value = env.evaluate(args[0])
            new_str = str(value)
            return new_str

        builtin_str = BuiltinFuncObj(BUILTIN_FUNC_NAME_STR, _str)
        self.global_context.register(BUILTIN_FUNC_NAME_STR, builtin_str)

        def _super(args, env):
            try:
                classtype = env.evaluate(args[0])
                obj = env.evaluate(args[1])
                is_classtype = isinstance(classtype, ClassObj)
                is_instance = isinstance(obj, Instance)
                if is_classtype and is_instance:
                    s = Super(classtype, obj)
                    return s
                else:
                    # Caught by except below
                    raise Exception()
            except:
                raise InvalidArgumentsForSuperError()

        builtin_super = BuiltinFuncObj(BUILTIN_FUNC_NAME_SUPER, _super)
        self.global_context.register(BUILTIN_FUNC_NAME_SUPER, builtin_super)

    def begin_block(self, block):
        self.address = _copy_address(block.address)
        should_begin = block.begin(self)
        if should_begin:
            self.shift_indent(1)
            self.blocks.append(block)

    def end_block(self):
        block = self.pop_block()
        block.end(self)

        if (
            block.kind == BLOCK_KIND_IFS
            or block.kind == BLOCK_KIND_CLASS_DEF
            or block.kind == BLOCK_KIND_TRY
            or block.kind == BLOCK_KIND_EXCEPT
        ):
            return False
        elif (
            block.kind == BLOCK_KIND_IF_ELIF_ELSE or block.kind == BLOCK_KIND_FUNC_CALL
        ):
            return True
        else:
            self.begin_block(block)
            return True

    def evaluate(self, expr):
        is_variable = isinstance(expr, Variable)
        is_attribute = isinstance(expr, Attribute)
        is_subscript = isinstance(expr, Subscript)
        if is_variable or is_attribute or is_subscript:
            evaluated_value = expr.evaluate(self)
            return evaluated_value

        is_binop = isinstance(expr, BinaryOperation)
        is_unaryop = isinstance(expr, UnaryOperation)
        if is_binop or is_unaryop:
            evaluated_value = expr.operate(self)
            return evaluated_value

        is_list = isinstance(expr, list)
        if is_list:
            evaluated_list = []
            for elem in expr:
                value = self.evaluate(elem)
                evaluated_list.append(value)
            return evaluated_list

        is_accessible = isinstance(expr, Accessible)
        if is_accessible:
            return expr

        is_dict = isinstance(expr, dict)
        if is_dict:
            evaluated_dict = {}
            for key in expr:
                evaluated_dict[key] = self.evaluate(expr[key])
            return evaluated_dict

        return expr

    def jump_to(self, address):
        self.address = _copy_address(address)

    def lookup(self, name):
        current_scope = self.context
        while True:
            try:
                value = current_scope.lookup(name)
                return value
            except:
                current_scope = current_scope.nesting_scope
                if current_scope == None:
                    raise NameNotFoundError(name)
                else:
                    continue

    def pop_block(self):
        b = self.blocks.pop()
        return b

    def pop_stack(self):
        previous_context = self.callstack.pop()
        self.context = previous_context

    def push_stack(self, new_context):
        self.callstack.append(self.context)
        self.context = new_context

    def register(self, name, obj):
        self.context.register(name, obj)

    def retrieve_nesting_scope(self):
        current_scope = self.context
        while True:
            is_classscope = isinstance(current_scope, ClassScope)
            if is_classscope:
                current_scope = current_scope.nesting_scope
                continue
            else:
                return current_scope

    def shift_indent(self, delta):
        self.address.indent += delta

    def skip_to_next_line(self):
        next_line_index = self.address.line + 1
        while True:
            next_line = self.code[next_line_index]
            next_indent = next_line[INDEX_INDENT]
            delta = next_indent - self.address.indent
            if delta <= 0:
                for _ in range(0, delta, -1):
                    is_address_jumped = self.end_block()
                    if is_address_jumped:
                        self.skip_to_next_line()
                        return
                break
            next_line_index += 1
        self.address.line = next_line_index

    def step_line(self, delta):
        self.address.line += delta

    def switch_context(self, next_context):
        self.context = next_context


def _get_description(value):
    desc = str(value)
    return desc


# Commands
class Assignment:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def execute(self, env):
        value = env.evaluate(self.rhs)
        self.lhs.assign(value, env)


class Ifs:
    def execute(self, env):
        def begin(env):
            return True

        def end(env):
            env.shift_indent(-1)

        block = Block(BLOCK_KIND_IFS, env.address, begin, end)
        env.begin_block(block)


def _execute_conditional_block(env):
    def begin(env):
        return True

    def end(env):
        env.shift_indent(-2)
        env.pop_block()

    block = Block(BLOCK_KIND_IF_ELIF_ELSE, env.address, begin, end)
    env.begin_block(block)


class If:
    def __init__(self, condition):
        self.condition = condition

    def execute(self, env):
        is_satisfied = env.evaluate(self.condition)
        if is_satisfied:
            _execute_conditional_block(env)


class Elif:
    def __init__(self, condition):
        self.condition = condition

    def execute(self, env):
        is_satisfied = env.evaluate(self.condition)
        if is_satisfied:
            _execute_conditional_block(env)


class Else:
    def execute(self, env):
        _execute_conditional_block(env)


class LoopCounter:
    def __init__(self, start, stop, step):
        self.start = start
        self.stop = stop
        self.step = step
        self.now = None

    def next(self):
        if (
            self.step > 0
            and self.start >= self.stop
            or self.step < 0
            and self.start <= self.stop
        ):
            return None
        elif self.now == None:
            self.now = self.start
            return self.start
        else:
            self.now += self.step
            if self.step > 0:
                if self.now >= self.stop:
                    return None
                else:
                    return self.now
            elif self.step < 0:
                if self.now <= self.stop:
                    return None
                else:
                    return self.now
            else:
                return None


class ForRange:
    def __init__(self, varname, start, stop, step):
        self.varname = varname
        self.start = start
        self.stop = stop
        self.step = step

    def execute(self, env):
        stop_value = env.evaluate(self.stop)
        if self.start == None and self.step == None:
            # eg. for i in range(n):
            loopcounter = LoopCounter(0, stop_value, 1)
        elif self.start != None and self.step == None:
            # eg. for i in range(m, n):
            start_value = env.evaluate(self.start)
            loopcounter = LoopCounter(start_value, stop_value, 1)
        else:
            # eg. for i in range(a, b, c):
            start_value = env.evaluate(self.start)
            step_value = env.evaluate(self.step)
            loopcounter = LoopCounter(start_value, stop_value, step_value)

        def begin(env):
            next_value = loopcounter.next()
            if next_value != None:
                env.register(self.varname, next_value)
                return True
            else:
                return False

        def end(env):
            pass

        block = Block(BLOCK_KIND_FOR_RANGE, env.address, begin, end)
        env.begin_block(block)


class ForEach:
    def __init__(self, elemname, iterable):
        self.elemname = elemname
        self.iterable = iterable

    def execute(self, env):
        iterableobj = env.evaluate(self.iterable)
        is_list = isinstance(iterableobj, list)
        is_str = isinstance(iterableobj, str)
        is_dict = isinstance(iterableobj, dict)
        if not (is_list or is_str or is_dict):
            raise NotIterableError()

        if not is_dict:
            length = len(iterableobj)
            loopcounter = LoopCounter(0, length, 1)

            def begin(env):
                next_index = loopcounter.next()
                if next_index != None:
                    env.register(self.elemname, iterableobj[next_index])
                    return True
                else:
                    return False

        else:
            keys = iterableobj.keys()
            length = len(keys)
            loopcounter = LoopCounter(0, length, 1)

            def begin(env):
                next_index = loopcounter.next()
                if next_index != None:
                    env.register(self.elemname, iterableobj[keys[next_index]])
                    return True
                else:
                    return False

        def end(env):
            pass

        block = Block(BLOCK_KIND_FOR_EACH, env.address, begin, end)
        env.begin_block(block)


class While:
    def __init__(self, condition):
        self.condition = condition

    def execute(self, env):
        def begin(env):
            condition_value = env.evaluate(self.condition)
            if condition_value:
                return True
            else:
                return False

        def end(env):
            pass

        block = Block(BLOCK_KIND_WHILE, env.address, begin, end)
        env.begin_block(block)


class Break:
    def execute(self, env):
        while True:
            block = env.pop_block()
            if (
                block.kind == BLOCK_KIND_IFS
                or block.kind == BLOCK_KIND_IF_ELIF_ELSE
                or block.kind == BLOCK_KIND_TRY
                or block.kind == BLOCK_KIND_EXCEPT
            ):
                env.shift_indent(-1)
                continue
            elif (
                block.kind == BLOCK_KIND_WHILE
                or block.kind == BLOCK_KIND_FOR_RANGE
                or block.kind == BLOCK_KIND_FOR_EACH
            ):
                env.shift_indent(-1)
                break
            else:
                raise InvalidBreakError()


class Continue:
    def execute(self, env):
        while True:
            block = env.pop_block()
            if (
                block.kind == BLOCK_KIND_IFS
                or block.kind == BLOCK_KIND_IF_ELIF_ELSE
                or block.kind == BLOCK_KIND_TRY
                or block.kind == BLOCK_KIND_EXCEPT
            ):
                env.shift_indent(-1)
                continue
            elif (
                block.kind == BLOCK_KIND_WHILE
                or block.kind == BLOCK_KIND_FOR_RANGE
                or block.kind == BLOCK_KIND_FOR_EACH
            ):
                env.begin_block(block)
                break
            else:
                raise InvalidContinueError()


class FuncDef:
    def __init__(self, name, params):
        self.name = name
        self.params = params

    def execute(self, env):
        defined_address = env.address
        nesting_scope = env.retrieve_nesting_scope()
        funcobj = FuncObj(self.name, self.params, nesting_scope, defined_address)
        env.register(self.name, funcobj)


def _invoke(calledobj, args, lhs, env):
    funcobj = calledobj

    def get_returned_value(env):
        return env.returned_value

    is_methodobj = isinstance(calledobj, MethodObj)
    if is_methodobj:
        funcobj = calledobj.funcobj
        if funcobj.name == "__init__":

            def _get_returned_value(env):
                return calledobj.instance

            get_returned_value = _get_returned_value
        args.insert(0, calledobj.instance)  # insert self

    caller_address = _copy_address(env.address)
    args_dict = {}
    length = len(args)
    for i in range(length):
        paramname = funcobj.params[i]
        argvalue = env.evaluate(args[i])
        args_dict[paramname] = argvalue
    new_context = FuncScope(funcobj.nesting_scope, args_dict)
    env.push_stack(new_context)

    def begin(env):
        return True

    def end(env):
        env.pop_stack()
        if lhs != None:
            returned_value = get_returned_value(env)
            lhs.assign(returned_value, env)
        env.returned_value = None
        env.jump_to(caller_address)

    block = Block(BLOCK_KIND_FUNC_CALL, funcobj.address, begin, end)
    env.begin_block(block)


class Call:
    def __init__(self, lhs, funcref, args):
        self.lhs = lhs
        self.funcref = funcref
        self.args = args

    def execute(self, env):
        calledobj = env.evaluate(self.funcref)
        is_funcobj = isinstance(calledobj, FuncObj)
        is_methodobj = isinstance(calledobj, MethodObj)
        is_builtin = isinstance(calledobj, BuiltinFuncObj)
        is_classtype = isinstance(calledobj, ClassObj)
        if is_funcobj or is_methodobj:
            _invoke(calledobj, self.args, self.lhs, env)
        elif is_builtin:
            returned_value = calledobj.body(self.args, env)
            if self.lhs != None:
                self.lhs.assign(returned_value, env)
        elif is_classtype:
            instance = Instance(calledobj)
            try:
                init = instance.get_attr("__init__")
                _invoke(init, self.args, self.lhs, env)
            except:
                self.lhs.assign(instance, env)
                return  # Successful
        else:
            raise CannotInvokeFunctionError()


class Return:
    def __init__(self, expression):
        self.expression = expression

    def execute(self, env):
        env.returned_value = env.evaluate(self.expression)
        while True:
            try:
                block = env.pop_block()
                if block.kind == BLOCK_KIND_FUNC_CALL:
                    block.end(env)
                    return
                elif (
                    block.kind == BLOCK_KIND_IFS
                    or block.kind == BLOCK_KIND_IF_ELIF_ELSE
                    or block.kind == BLOCK_KIND_TRY
                    or block.kind == BLOCK_KIND_EXCEPT
                    or block.kind == BLOCK_KIND_WHILE
                    or block.kind == BLOCK_KIND_FOR_RANGE
                    or block.kind == BLOCK_KIND_FOR_EACH
                ):
                    continue
                else:
                    raise Exception()
            except:
                raise InvalidReturnError()


class ClassDef:
    def __init__(self, classname, superclassname):
        self.classname = classname
        self.superclassname = superclassname

    def execute(self, env):
        if (
            self.superclassname == None
            or self.superclassname == builtin_type.object.name
        ):
            superclass = builtin_type.object
        else:
            superclass = env.lookup(self.superclassname)
            is_classtype = isinstance(superclass, ClassObj)
            if not is_classtype:
                raise InvalidSuperclassError()

        def begin(env):
            nesting_scope = env.retrieve_nesting_scope()
            new_context = ClassScope(nesting_scope, {})
            env.switch_context(new_context)
            return True

        current_context = env.context

        def end(env):
            attributes = env.context.dictobj
            env.switch_context(current_context)
            classtype = ClassObj(self.classname, superclass, attributes)
            env.register(self.classname, classtype)
            env.shift_indent(-1)

        block = Block(BLOCK_KIND_CLASS_DEF, env.address, begin, end)
        env.begin_block(block)


class Comment:
    def __init__(self, options):
        self.options = options

    def execute(self, env):
        pass  # Do nothing


class Pass:
    def execute(self, env):
        pass  # Do nothing


class EndOfCode:
    def execute(self, env):
        pass  # Do nothing


class Parser:
    def __init__(self):
        t = {}

        def _assignment(line):
            lhs = self.parse_ref(line[INDEX_ASSIGNMENT_LHS])
            rhs = self.parse_expr(line[INDEX_ASSIGNMENT_RHS])
            cmd = Assignment(lhs, rhs)
            return cmd

        t[KEYWORD_ASSIGNMENT] = _assignment

        def _make_compound_assignment(keyword, line):
            lhs = self.parse_ref(line[INDEX_ASSIGNMENT_LHS])
            rhs = self.parse_expr(line[INDEX_ASSIGNMENT_RHS])
            op = BinaryOperation(keyword, lhs, rhs)
            cmd = Assignment(lhs, op)
            return cmd

        def _compound_addition(line):
            cmd = _make_compound_assignment(KEYWORD_ADDITION, line)
            return cmd

        t[KEYWORD_COMPOUND_ADDITION] = _compound_addition

        def _compound_subtraction(line):
            cmd = _make_compound_assignment(KEYWORD_SUBTRACTION, line)
            return cmd

        t[KEYWORD_COMPOUND_SUBTRACTION] = _compound_subtraction

        def _compound_multiplication(line):
            cmd = _make_compound_assignment(KEYWORD_MULTIPLICATION, line)
            return cmd

        t[KEYWORD_MULTIPLICATION] = _compound_multiplication

        def _ifs(line):
            cmd = Ifs()
            return cmd

        t[KEYWORD_IFS] = _ifs

        def _if(line):
            condition = self.parse_expr(line[INDEX_CONDITION])
            cmd = If(condition)
            return cmd

        t[KEYWORD_IF] = _if

        def _elif(line):
            condition = self.parse_expr(line[INDEX_CONDITION])
            cmd = Elif(condition)
            return cmd

        t[KEYWORD_ELIF] = _elif

        def _else(line):
            cmd = Else()
            return cmd

        t[KEYWORD_ELSE] = _else

        def _while(line):
            condition = self.parse_expr(line[INDEX_CONDITION])
            cmd = While(condition)
            return cmd

        t[KEYWORD_WHILE] = _while

        def _for_range(line):
            varname = line[INDEX_FOR_RANGE_VARIABLE_NAME]
            values = line[INDEX_FOR_RANGE_VALUES]
            length = len(values)
            if length == 1:
                stop = self.parse_expr(values[0])
                cmd = ForRange(varname, None, stop, None)
                return cmd
            elif length >= 2:
                start = self.parse_expr(values[0])
                stop = self.parse_expr(values[1])
                if length == 2:
                    cmd = ForRange(varname, start, stop, None)
                    return cmd
                else:
                    step = self.parse_expr(values[2])
                    cmd = ForRange(varname, start, stop, step)
                    return cmd

        t[KEYWORD_FOR_RANGE] = _for_range

        def _for_each(line):
            elemname = line[INDEX_FOR_EACH_ELEMENT_NAME]
            iterable = self.parse_expr(line[INDEX_FOR_EACH_ITERABLE_NAME])
            cmd = ForEach(elemname, iterable)
            return cmd

        t[KEYWORD_FOR_EACH] = _for_each

        def _break(line):
            cmd = Break()
            return cmd

        t[KEYWORD_BREAK] = _break

        def _continue(line):
            cmd = Continue()
            return cmd

        t[KEYWORD_CONTINUE] = _continue

        def _func_def(line):
            funcname = line[INDEX_FUNC_DEF_FUNC_NAME]
            params = line[INDEX_FUNC_DEF_PARAMETERS]
            cmd = FuncDef(funcname, params)
            return cmd

        t[KEYWORD_FUNC_DEF] = _func_def

        def _call(line):
            lhs = line[INDEX_CALL_LHS]
            if lhs != None:
                lhs = self.parse_ref(lhs)
            calledref = self.parse_ref(line[INDEX_CALL_REFERENCE])
            args = self.parse_args(line, INDEX_CALL_ARGS)
            cmd = Call(lhs, calledref, args)
            return cmd

        t[KEYWORD_CALL] = _call

        def _return(line):
            length = len(line)
            if length - 1 < INDEX_RETURN_VALUE:
                cmd = Return(None)
                return cmd
            else:
                expr = self.parse_expr(line[INDEX_RETURN_VALUE])
                cmd = Return(expr)
                return cmd

        t[KEYWORD_RETURN] = _return

        def _class_def(line):
            classname = line[INDEX_CLASS_DEF_CLASS_NAME]
            superclassname = line[INDEX_CLASS_DEF_SUPERCLASS_NAME]
            cmd = ClassDef(classname, superclassname)
            return cmd

        t[KEYWORD_CLASS_DEF] = _class_def

        def _comment(line):
            options = line[INDEX_OPTIONS]
            cmd = Comment(options)
            return cmd

        t[KEYWORD_COMMENT] = _comment

        def _pass(line):
            cmd = Pass()
            return cmd

        t[KEYWORD_PASS] = _pass

        def _end_of_code(line):
            cmd = EndOfCode()
            return cmd

        t[KEYWORD_END_OF_CODE] = _end_of_code

        self.table = t

    def parse(self, line):
        keyword = line[INDEX_KEYWORD]
        parserfunc = self.table[keyword]
        command = parserfunc(line)
        return command

    def parse_args(self, listobj, index):
        args_list = listobj[index]
        parsed_args = []
        for elem in args_list:
            arg = self.parse_expr(elem)
            parsed_args.append(arg)
        return parsed_args

    def parse_expr(self, obj):
        is_list = isinstance(obj, list)
        if is_list:
            is_nested_list = isinstance(obj[0], list)
            if is_nested_list:
                parsed_list = []
                for elem in obj[0]:
                    value = self.parse_expr(elem)
                    parsed_list.append(value)
                return parsed_list
            keyword = obj[INDEX_EXPRESSION_KEYWORD]
            if (
                keyword == KEYWORD_VARIABLE
                or keyword == KEYWORD_ATTRIBUTE
                or keyword == KEYWORD_SUBSCRIPT
            ):
                ref = self.parse_ref(obj)
                return ref
            elif (
                keyword == KEYWORD_NOT
                or keyword == KEYWORD_NEGATIVE
                or keyword == KEYWORD_BIT_NOT
            ):
                operand = self.parse_expr(obj[INDEX_UNARY_OPERAND])
                unary_op = UnaryOperation(keyword, operand)
                return unary_op
            else:
                left = self.parse_expr(obj[INDEX_LEFT_OPERAND])
                right = self.parse_expr(obj[INDEX_RIGHT_OPERAND])
                bin_op = BinaryOperation(keyword, left, right)
                return bin_op

        is_dict = isinstance(obj, dict)
        if is_dict:
            parsed_dict = {}
            for key in obj:
                parsed_dict[key] = self.parse_expr(obj[key])
            return parsed_dict
        else:
            return obj

    def parse_ref(self, listobj):
        keyword = listobj[INDEX_EXPRESSION_KEYWORD]
        if keyword == KEYWORD_VARIABLE:
            name = listobj[INDEX_VARIABLE_NAME]
            var = Variable(name)
            return var
        elif keyword == KEYWORD_ATTRIBUTE:
            objname = listobj[INDEX_ATTRIBUTE_OBJECT_NAME]
            propertynames = []
            length = len(listobj)
            for i in range(INDEX_ATTRIBUTE_PROPERTY_NAMES, length):
                propertynames.append(listobj[i])
            attr = Attribute(objname, propertynames)
            return attr
        elif keyword == KEYWORD_SUBSCRIPT:
            objref = self.parse_ref(listobj[INDEX_SUBSCRIPT_REFERENCED_OBJECT])
            indexexpr = self.parse_expr(listobj[INDEX_SUBSCRIPT_INDEX_EXPR])
            sub = Subscript(objref, indexexpr)
            return sub


class AttributeNotExistError(Exception):
    def __init__(self, attrname):
        s = super(AttributeNotExistError, self)
        s.__init__()
        self.attrname = attrname


class CannotInvokeFunctionError(Exception):
    pass


class CannotParseInt(Exception):
    pass


class CannotPopFromListError(Exception):
    pass


class InconsistentBlockError(Exception):
    pass


class InvalidArgumentsForSuperError(Exception):
    pass


class InvalidBreakError(Exception):
    pass


class InvalidContinueError(Exception):
    pass


class InvalidEndOfCodeError(Exception):
    pass


class InvalidExceptionError(Exception):
    pass


class InvalidOperationError(Exception):
    pass


class InvalidReturnError(Exception):
    pass


class InvalidSuperclassError(Exception):
    pass


class MethodNotFoundError(Exception):
    def __init__(self, name):
        s = super(MethodNotFoundError, self)
        s.__init__()
        self.name = name


class NameNotFoundError(Exception):
    def __init__(self, name):
        s = super(NameNotFoundError, self)
        s.__init__()
        self.name = name


class NotIterableError(Exception):
    pass


class SubscriptNotAllowedError(Exception):
    pass


class SuperCallFailedError(Exception):
    pass


class UnhandledExceptionError(Exception):
    pass


class ValueNotFoundError(Exception):
    pass
