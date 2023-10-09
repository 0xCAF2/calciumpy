import typing
from calciumlang.command.command import Command
from calciumlang.environment import Environment


class ExprStmt(Command):
    def __init__(self, expr: typing.Any):
        self.expr = expr

    def execute(self, env: Environment) -> None:
        env.evaluate(self.expr)
