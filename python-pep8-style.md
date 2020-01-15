[PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

For our project, we'll follow the PEP 8 style guide, which offers conventions that we can follow to the make our code consistent and more readable.

# Overview of the conventions
## Conventions we should follow
- Indentation: 4 spaces per indentation level (see the guide linked above for specific indentation cases such as continutation lines)
- Tabs or spaces: spaces
- Line breaks before or after binary op: before (**I think it's more readable, but we can talk about it.**)
- Blank lines: surround top-level functions and classes with two blank lines on either side, class methods with a single blank line on either side
- Imports: imports should usually be on separate lines, always at the top of the file, just after module comments and docstrings, before globals and constants; prefer absolute imports
- Comments (syntax: ```# This is a comment```):
    - Let's try and make and keep up with comments when the logic gets complicated (e.g. explaining the purpose of loops and conditionals, non-standard function calls, etc.)
    - Prefer block comments to inline comments
- Docstrings (syntax: ```""" This is a docstring """```):
    - Write docstrings for all public modules, functions, classes, and methods
    

## Conventions that we can choose whether or not to follow
- Max line length:
    - They recommend 79 characters for normal lines, 72 characters for comments and docstrings
    - **I would be perfectly happy extending this out to 99 characters for normal lines to minimize the amount of multi-line shenanigans we'll have to partake in. I'm fine with 72 for comments, etc.**
- String quotes: " or '
    - **I'm fine with either. If I had to pick, I guess I'd choose "**
    - When a quote is surrounded with a single or double quote, use the opposite within the string to avoid backslashes in the string
- Pet peeves:
    - Avoid extraneous white space
        1. Immediately inside brackets
        2. Between a trailing comma and a following close parenthesis
        3. Immediately before a comma, semicolon, or colon (except slices)
        4. Immediately before the open parenthesis that starts the argument list of a function call
        5. Immediately before the open parenthesis that starts an indexing or slicing
        6. More than one space around an assignment  (or other) operator to align it with another
