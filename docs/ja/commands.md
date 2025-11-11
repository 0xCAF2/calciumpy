---
outline: [2, 4]
---

## コマンドとは？
Calcium では、各行（文に相当）で何を実行するかを「コマンド」文字列で指定します。
例えば、制御文に対応するコマンドには以下のようなものがあります。

| コマンド名 | 説明                     |
| ---------- | ------------------------ |
| `if`       | 条件分岐を開始します     |
| `elif`     | 条件分岐の中間節を表します |
| `else`     | 条件分岐の終了節を表します |
| `for`      | 繰り返しを開始します     |
| `while`    | 条件付き繰り返しを開始します |
| `break`    | 繰り返しを中断します     |
| `continue` | 繰り返しの次の反復に進みます |

これらは Python の対応する文と同様の動作をします。

### 例： if 文の使用
次の Python コードは、Calcium では以下のように表現されます。

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

第一要素の `1`, `2`, `3` はブロックレベルを表し、Python におけるインデントに対応します。
JSON にはインデントの概念がないため、ブロックレベルで文の入れ子構造等を表現します。

#### ifs とは？
`ifs` コマンドは、`if`, `elif`, `else` の各節をまとめるためのコンテナです。
`ifs` 自体は特別な動作をしませんが、`if`, `elif`, `else` の各節を実行する際に
正しいブロックレベルを認識するために必要です。

## Calcium コマンドを生成する

Calcium コマンドは手動で記述することもできますが、
[カルシウム エディタ](https://caed.app/) のようなビジュアルプログラミング環境を使って
生成できます。

また、`from calciumpy.tool import convert` によって、
Python のソースコード（のサブセット）から Calcium コマンド群を生成することもできます。

```python
from calciumpy.tool import convert
python_code = '''
x = 73
if x % 2 == 0:
    print("x is even.")
else:
    print("x is odd.")
'''
commands = convert(python_code) # commands は文字列
```


::: info
Python の文全てを Calcium コマンドに変換できるわけではありません。
:::


`Runtime` クラスに渡すには、文字列を直接でも問題ないですし、
`json.loads` でデコードしても良いです。

## Calcium コマンドを実行する

Calcium コマンドを実行するには、`calciumpy.Runtime` クラスを使用します。

```python
from calciumpy import Runtime
calcium_code = [ ... ]  # Calcium コマンド群（JSON 配列のリスト）
r = Runtime(calcium_code)
r.run()
```

`run` メソッドは、Calcium コマンド群を実行し、 `input()` が呼び出されるまでか、
あるいはプログラムが終了するまで動作します。

## コマンド一覧

| コマンド名 | 説明                     |
| ---------- | ------------------------ |
| `#`        | コメント行               |
| `=`        | 代入文                   |
| `expr`     | 式文の評価                 |
| `ifs`      | 条件分岐のコンテナ         |
| `if`       | 条件分岐の開始節           |
| `elif`     | 条件分岐の中間節           |
| `else`     | 条件分岐の終了節           |
| `for`      | 繰り返しの開始             |
| `while`    | 条件付き繰り返しの開始       |
| `break`    | 繰り返しの中断             |
| `continue` | 繰り返しの次の反復に進む     |
| `def`     | 関数定義の開始             |
| `return`   | 関数からの戻り値の返却       |
| `import`   | モジュールのインポート       |
| `class`   | クラス定義の開始           |
| `pass`     | 空文                     |
| `end`      | プログラムの終了             |
