**Required:**
- [X] Arithmetic expressions
- [X] Boolean expressions
- [X] Assignment
- [] Goto statements / return statement
- [] If/else control flow: One-line loops/conditionals aren't currently supported:
```
if (X && Y) { Z }
```
turns into
```
if (X):
    if (Y):
        Z
    else:
else:
```
---
```
if (X || Y) { A }
```
turns into
```
if (X):
    A
else:
    if (Y):
        A
    else:
```
```
if (!(X)) { A }
```
turns into
```
if (!X):
    A
else:
```
---
```
if (X) { A }
else if (Y) { B }
else { C }
```
turns into
```
if (X):
    A
else:
    if (Y):
        B
    else:
        C
```
---
```
if(X || Y)
```
is equivalent to
```
if (X): else if (Y)
```

- [] Unary operators (unary minus (`-`), NOT (`!`), `sizeof()`)
- [] Return statements
- [] Break statements: Break can currently be placed outside of loops and switches
- [] While/do-while loops: One-line loops/conditionals aren't currently supported

# Identifiers

# Variables
