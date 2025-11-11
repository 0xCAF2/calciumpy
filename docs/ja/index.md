---
layout: home

hero:
  name: calciumpy
  text: JSON を「実行」するための Python ライブラリ
  actions:
    - theme: brand
      text: ガイド
      link: /ja/guides
    - theme: alt
      text: API リファレンス
      link: /ja/api

features:
  - title: コマンド指向の実行環境
    details: 各命令は JSON 配列で表現されます。
  - title: Python との相互運用性
    details: Python の組み込み関数などを利用できます。
  - title: コード生成との親和性
    details: Blockly と連携して、各行を生成します (下記を参照)。
---

## Blockly で生成した JSON を calciumpy で実行する
[カルシウム エディタ](https://caed.app/) は、[Blockly](https://developers.google.com/blockly) を使ってビジュアルプログラミングで
コードを作成し、calciumpy で実行する Web アプリケーションです。
[Pyodide](https://pyodide.org/en/stable/) と組み合わせてブラウザ上で動作します。