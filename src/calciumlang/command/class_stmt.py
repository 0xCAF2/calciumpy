import typing
from calciumlang.command.command import Command
from calciumlang.block import Block, BlockKind, BlockResult
from calciumlang.environment import Environment
from calciumlang.expression.assignable import Variable, Attribute
from calciumlang.namespace import ClassScope


class Class(Command):
    def __init__(self, name: str, superclass: typing.Union[Variable, Attribute, None]):
        self.name = name
        self.superclass = superclass

    def execute(self, env: Environment) -> None:
        if self.superclass is None:
            superclass = object
        else:
            superclass = self.superclass.evaluate(env)

        def enter(env: Environment) -> bool:
            parent_scope = env.context.find_nesting_scope()
            env.context = ClassScope(parent_scope, {})
            return True

        previous_context = env.context

        def exit(env: Environment) -> BlockResult:
            if not isinstance(env.context, ClassScope):
                raise RuntimeError("context is not ClassScope")
            attributes = env.context.create_attributes()
            env.context = previous_context
            classtype = type(self.name, (superclass,), attributes)
            env.context.register(self.name, classtype)
            env.addr.shift(-1)
            return BlockResult.SHIFT

        block = Block(BlockKind.CLASS, env.addr, enter, exit)
        block.will_enter(env)
