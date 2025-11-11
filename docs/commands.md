
---

---

## What is a command?
In Calcium, each line (equivalent to a statement) specifies what to execute using a "command" string. Certain commands correspond to control flow statements. Examples include:

| Command | Description |
| ------- | ----------- |
| `if`    | Start a conditional branch |
| `elif`  | Middle branch of a conditional |
| `else`  | Final branch of a conditional |
| `for`   | Start a loop |
| `while` | Start a conditional loop |
| `break` | Break out of a loop |
| `continue` | Continue to the next iteration of a loop |

These behave similarly to their Python counterparts.

### Example: using an if statement
The following Python code can be represented in Calcium as follows:

```python
x = 73
if x % 2 == 0:
		print("x is even")
else:
		print("x is odd")
```

```js
[
  [1, [], "#", "0.4.3"],
  [1, [], "=", ["var", "x"], ["num", "73"]],
  [1, [], "ifs"],
    [2, [], "if", ["==", ["%", ["var", "x"], ["num", "2"]], ["num", "0"]]],
      [3, [], "expr", ["call", ["var", "print"], ["x is even."]]],
    [2, [], "else"],
      [3, [], "expr", ["call", ["var", "print"], ["x is odd."]]],
  [1, [], "end"]
]
```

The leading numbers `1`, `2`, `3` indicate the block level (corresponding to indentation in Python). Since JSON has no indentation concept, nesting is represented with block levels.

#### What is `ifs`?
The `ifs` command is a container for `if`, `elif`, and `else` clauses. `ifs` itself does not perform special runtime behavior, but it is required so the interpreter can recognize the correct block levels for each clause.

## Generating Calcium commands

You can write Calcium commands by hand, or generate them using a visual tool such as the Calcium Editor (https://caed.app/). You can also convert Python source (a supported subset) to Calcium commands with:

```python
from calciumpy.tool import convert
python_code = '''
x = 73
if x % 2 == 0:
		print("x is even.")
else:
		print("x is odd.")
'''
commands = convert(python_code)  # `commands` is a string
```

::: info
Not all Python statements can be converted to Calcium.
:::

To pass commands into `Runtime` you may give the JSON string directly or decode it with `json.loads`.

## Executing Calcium commands

Use `calciumpy.Runtime` to execute Calcium commands:

```python
from calciumpy import Runtime
calcium_code = [ ... ]  # list of Calcium command arrays
r = Runtime(calcium_code)
r.run()
```

`run()` will execute until the program ends or until an `input()` is called.

## Command list

| Command | Description |
| ------- | ----------- |
| `#`     | Comment |
| `=`     | Assignment |
| `expr`  | Evaluate an expression (statement) |
| `ifs`   | Container for conditional branches |
| `if`    | Start of conditional branch |
| `elif`  | Middle conditional branch |
| `else`  | Final conditional branch |
| `for`   | Start a for-loop |
| `while` | Start a while-loop |
| `break` | Break out of a loop |
| `continue` | Continue to the next loop iteration |
| `def`   | Start a function definition |
| `return`| Return a value from a function |
| `import`| Import a module |
| `class` | Start a class definition |
| `pass`  | No-op statement |
| `end`   | End of program / top-level end |
