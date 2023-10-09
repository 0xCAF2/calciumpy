from calciumlang.command.command import Command
from calciumlang.environment import Environment


class Comment(Command):
    def execute(self, env: Environment) -> None:
        pass  # do nothing


class Pass(Command):
    def execute(self, env: Environment) -> None:
        pass  # do nothing


class End(Command):
    def execute(self, env: Environment) -> None:
        pass  # do nothing
