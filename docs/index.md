---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: calciumpy
  text: An interpreter that lets you "run" JSON in Python.
  actions:
    - theme: brand
      text: Get Started
      link: /guides
    - theme: alt
      text: API Reference
      link: /api

features:
  - title: Command based runtime
    details: Each line is a command represented in a JSON array.
  - title: Python interoperability
    details: Python's built-in functions and more can be used.
  - title: Code generation friendly
    details: Integrating with Blockly, commands can be generated.
---

## Applications of calciumpy
[Calcium Editor](https://caed.app/) is a web application that allows you to
create code using visual programming with
[Blockly](https://developers.google.com/blockly) and execute it with calciumpy
and [Pyodide](https://pyodide.org/en/stable/).
