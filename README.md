# minim
A minimal scripting language with only 6 keywords.

## Usage
```sh
python minim.py file_to_run.py
```

## Concepts
### Ideologies
- Everything can be evaluated as a value.
- Everything should be somewhat readable, at least.
- Control flow should have only one instruction.

### Data Types
- Numbers (Floats)
- Strings

## Syntax
### Keyword Comparison
| minim | Python |
| --- | --- |
| `set V X` | `V = X` |
| `out X` | `print(X)` |
| `in X` | `input(X)` |
| `num X` | `float(X)` |
| `loopif C { ... }` | N/A (closest equivalent is `while C:`) |
| `break X` | N/A (closest equivalent is `break`) |

### Operators
- **Arithmetic:** +, -, *, /, %
- **Bitwise:** &, |, ^, ~
- **Comparison:** ==, >, <
- **Logical:** &&, ||, ^^
