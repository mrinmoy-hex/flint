import os
import sys


class GenerateAst:
    @staticmethod
    def main(args):
        if len(args) != 1:
            print("Usage: generate_ast <output directory>", file=sys.stderr)
            sys.exit(64)

        output_dir = args[0]
        GenerateAst.define_ast(output_dir, "Expr", [
            "Binary   : Expr left, Token operator, Expr right",
            "Grouping : Expr expression",
            "Literal  : Object value",
            "Unary    : Token operator, Expr right"
        ])

    @staticmethod
    def define_ast(output_dir, base_name, types):
        """Generate the AST classes"""
        try:
            path = os.path.join(output_dir, f"{base_name}.py")
            with open(path, "w") as file:
                file.write(f"class {base_name}:\n")
                file.write("    pass\n\n")  # Base class

                # Generate AST classes
                for type_definition in types:
                    class_name, fields = map(str.strip, type_definition.split(":"))
                    GenerateAst.define_type(file, base_name, class_name, fields)
                print(f"AST classes generated in {path}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def define_type(file, base_name, class_name, field_list):
        """Generate code for a specific type of AST node"""
        file.write(f"class {class_name}({base_name}):\n")
        fields = [f.strip() for f in field_list.split(",")]
        # print(fields)
        # Constructor
        file.write(f"    def __init__(self, {', '.join([field.split()[1] for field in fields])}):\n")
        for field in fields:
            field_type, field_name = field.split()
            file.write(f"        self.{field_name} = {field_name}\n")
        file.write("\n")


if __name__ == "__main__":
    GenerateAst.main(sys.argv[1:])
