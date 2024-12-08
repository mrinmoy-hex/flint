import pytest

TYPE_DEFINITION = "Binary    : Expr left, Token operator, Expr right"


parts = TYPE_DEFINITION.split(":")
print(parts)

cleaned_parts = map(str.strip, parts)   # removes trailing white spaces
print(list(cleaned_parts))

# segmenting class_name and fields
# class_name, fields = map(str.strip, TYPE_DEFINITION.split(":"))
types = [
    "Binary   : Expr left, Token operator, Expr right",
    "Grouping : Expr expression",
    "Literal  : Object value",
    "Unary    : Token operator, Expr right"
]

for typed in types: 
    class_name = typed[0].split(":")
    fields = typed[1].split(":")

    print(class_name)
    # print(fields)