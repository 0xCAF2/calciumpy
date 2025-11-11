# calciumpy

A Calcium language interpreter on Python

[Docs](https://0xcaf2.app/calciumpy/)

## What is Calcium language?

Calcium is a programming language that takes a JSON array as input.
It is interoperable with the Python language,
allowing you to utilize Python's standard libraries and more.
Calcium is primarily designed as a subset of Python.

## How to create the interpreter and run code

```python
from calciumpy import Runtime

# Calcium code is given as JSON arrays.
calcium_code = [
  [1, [], "#", "0.4.3"],
  [1, [], "expr", ["call", ["var", "print"], ["Hello, World."]]],
  [1, [], "end"],
]

# The Runtime executes Calcium code.
r = Runtime(calcium_code)
r.run()  # outputs 'Hello, World.'
```

The code above corresponds to the following Python code:

```python
print("Hello, World.")
```

## Applications of calciumpy

### [Calcium Editor](https://caed.app/)
is a web application that allows you to
create code using visual programming with
[Blockly](https://developers.google.com/blockly) and execute it with calciumpy
and [Pyodide](https://pyodide.org/en/stable/).
