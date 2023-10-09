import typing
from calciumlang.expression.assignable import Assignable
from calciumlang.command.command import Command
from calciumlang.environment import Environment


class Assign(Command):
    def __init__(self, lhs: Assignable, rhs: typing.Any):
        self.lhs = lhs
        self.rhs = rhs

    def execute(self, env: Environment):
        value = env.evaluate(self.rhs)
        if not isinstance(self.lhs, tuple):
            self.lhs.assign(value, env)
            return
        for lhs, val in zip(self.lhs, value):  # type: ignore
            lhs.assign(val, env)
