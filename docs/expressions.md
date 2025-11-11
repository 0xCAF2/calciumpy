---

---

## Expression overview

Some expressions are represented as JSON arrays.
The first element is a keyword string that indicates the expression type,
and the remaining elements are arguments specific to that expression.

## Numeric literals

Numeric literals are represented using strings so they can follow JSON's rules
while still allowing Python-style numeric literal forms.

```js
["num", "42"]
["num", "-3.14"]
["num", "1e10"]
["num", "0b1010"]     // binary
["num", "052"]        // octal
["num", "0x2A"]       // hexadecimal
["num", "1_000_000"]  // underscore as digit separator
```

## String literals, booleans and `null`

These use native JSON values. `null` maps to `None` in Calcium.

```js
"Hello, World!"
true  // True
false // False
null  // None
```

## Variable reference
Variable references use the `var` keyword:

```js
["var", "x"]
["var", "my variable"]
```

Variable names may contain any characters valid in JSON strings.

## Attribute access
Object attribute access uses the `attr` keyword:

```js
["attr", ["var", "runtime"], "run"]
```

The second element is the expression that evaluates to the object,
and the third element is the attribute name string.

## Subscript access
Indexing into lists or dictionaries uses the `sub` keyword:

```js
["sub", ["var", "myList"], ["num", "0"]]
["sub", ["var", "myDict"], ["var", "key"]]
```

## Function call
Function calls use the `call` keyword:

```js
["call", ["var", "print"], [["var", "x"], ["var", "y"]]]
```

The second element is the expression for the callable,
and the third element is an array of argument expressions.

## Operators
Operators are represented in prefix form using their corresponding keyword.

```js
["+", ["var", "a"], ["var", "b"]]        // a + b
["-", ["var", "a"], ["var", "b"]]        // a - b
["*", ["var", "a"], ["var", "b"]]        // a * b
```

### Binary operators
The following binary operators are supported.

| Operator | Keyword |
|--------|------------|
| +      | "+"        |
| -      | "-"        |
| *      | "*"        |
| /      | "/"        |
| //     | "//"       |
| %      | "%"        |
| **     | "**"       |
| ==     | "=="       |
| !=     | "!="       |
| <      | "<"        |
| <=     | "<="       |
| >      | ">"        |
| >=     | ">="       |
| and    | "and"      |
| or     | "or"       |

### Unary operators
The following unary operators are supported.

| Operator | Keyword |
|--------|------------|
| not    | "not"      |
| -      | "-_"       |
