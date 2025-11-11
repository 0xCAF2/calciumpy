---

---

## スタートガイド

```bash
pip install calciumpy
```

::: tip
環境によっては `pip3` を使う必要があるかもしれません。

```bash
pip3 install calciumpy
```
:::

## Calcium コードの構造
1行は JSON 配列で表現されます。各要素は：

```js
[
  1,   // number: ブロックレベル (= Python におけるインデント)
  [],  // any: 任意の要素（拡張用）
  "=", // string: コマンド名。文の種類を表します
  ..., // any: コマンドに応じた引数
]
```

例えば、次の Calcium コードは：

```js
[
  [1, [], "#", "0.4.3"],
  [1, [], "=", ["var", "x"], ["num", "42"]],
  [1, [], "expr", ["call", ["var", "print"], [["var", "x"]]]],
  [1, [], "end"],
]
```

以下の Python コードに相当します：

```python
x = 42
print(x)
```

- [コマンド一覧](/ja/commands)
- [式の表現](/ja/expressions)