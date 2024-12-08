import pytest

type_definition = "Binary    : Expr left, Token operator, Expr right"


parts = type_definition.split(":")
print(parts)

cleaned_parts = map(str.strip, parts)   # removes trailing white spaces
print(list(cleaned_parts))

# segmenting class_name and fields
# class_name, fields = map(str.strip, type_definition.split(":"))
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