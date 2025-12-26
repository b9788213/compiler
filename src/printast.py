from node import *

def print_ast(node, indent=0):
    prefix = "  " * indent

    if isinstance(node, Program):
        print(f"{prefix}Program")
        for func in node.funcs:
            print_ast(func, indent + 1)
        for static in node.statics:
            print(f"{prefix}  Static: {static}")

    elif isinstance(node, Func):
        print(f"{prefix}Func(name='{node.name}', args={node.args})")
        for stmt in node.body:
            print_ast(stmt, indent + 1)

    elif isinstance(node, BinOp):
        print(f"{prefix}BinOp('{node.op}')")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)

    elif isinstance(node, Assign):
        print(f"{prefix}Assign(name='{node.name}')")
        print_ast(node.value, indent + 1)

    elif isinstance(node, Call):
        print(f"{prefix}Call(name='{node.name}')")
        for arg in node.args:
            print_ast(arg, indent + 1)

    elif isinstance(node, (Int, Float, String, Id)):
        # Temel değerleri tek satırda yazdır
        print(f"{prefix}{type(node).__name__}({getattr(node, 'value', getattr(node, 'name', ''))})")

    elif isinstance(node, Neg):
        print(f"{prefix}Neg(-)")
        print_ast(node.value, indent + 1)

    else:
        print(f"{prefix}Unknown Node: {node}")