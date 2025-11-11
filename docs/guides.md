
---

---

## Quick start

```bash
pip install calciumpy
```

::: tip
On some systems you may need `pip3` instead:

```bash
pip3 install calciumpy
```
:::

## Structure of Calcium code
Each line is represented as a JSON array. Elements are:

```js
[
	1,   // number: block level (= indentation in Python)
	[],  // any: an arbitrary field (for extensions)
	"=", // string: command name (type of statement)
	..., // any: command-specific arguments
]
```

For example, the following Calcium code:

```js
[
	[1, [], "#", "0.4.3"],
	[1, [], "=", ["var", "x"], ["num", "42"]],
	[1, [], "expr", ["call", ["var", "print"], [["var", "x"]]]],
	[1, [], "end"],
]
```

corresponds to this Python code:

```python
x = 42
print(x)
```

- [Commands](/commands)
- [Expressions](/expressions)
