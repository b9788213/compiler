from node import (
    Asm,
    BinOp,
    Program,
    Comp,
    Call,
    CondStruct,
    Func,
    Id,
    Int,
    Float,
    String,
    Assign,
    Ret,
    While,
    If,
    Neg,
)


def get_ast(node, indent=0, markers=None):
    if markers is None:
        markers = []

    lines = []

    # Mevcut satırın başındaki bağlantı çizgilerini oluşturur
    if indent > 0:
        prefix = ""
        for i in range(indent - 1):
            if markers[i]:
                prefix += "│   "
            else:
                prefix += "    "
        prefix += "└── " if not markers[indent - 1] else "├── "
    else:
        prefix = ""

    # Düğüm tipine göre içeriği belirle
    def get_node_info(n):
        match n:
            case Asm(): return "Asm"
            case Program(): return "Program"
            case Func(): return f"Func({n.name}, args={n.args})"
            case BinOp(): return f"BinOp({n.op})"
            case Comp(): return f"Comp({n.op})"
            case Assign(): return f"Assign({n.name})"
            case Call(): return f"Call({n.name})"
            case Neg(): return "Neg(-)"
            case Ret(): return "Ret"
            case While(): return "While"
            case CondStruct(): return "CondStruct"
            case If(): return "If"
            case Int(): return f"Int({n.value})"
            case Float(): return f"Float({n.value})"
            case String(): return f"String({repr(n.value)})"
            case Id(): return f"Id({n.name})"
        return f"Unknown({type(n).__name__})"

    lines.append(f"{prefix}{get_node_info(node)}")

    # Alt düğümleri (children) topla
    children = []
    if isinstance(node, Program):
        children.extend(node.funcs)
    elif isinstance(node, Func):
        children.extend(node.body.code)
    elif isinstance(node, (BinOp, Comp)):
        children.append(node.left)
        children.append(node.right)
    elif isinstance(node, Assign):
        children.append(node.value)
    elif isinstance(node, Call):
        children.extend(node.args)
    elif isinstance(node, (Neg, Ret)):
        children.append(node.value)
    elif isinstance(node, While):
        children.append(node.cond)
        children.extend(node.body.code)
    elif isinstance(node, CondStruct):
        children.extend(node.ifs)
        children.extend(node.elsebody.code) if node.elsebody else None
    elif isinstance(node, If):
        children.append(node.cond)
        children.extend(node.body.code)

    # Çocukları recursive olarak işle
    for i, child in enumerate(children):
        is_last = i == len(children) - 1
        # Alt dallara markers bilgisini aktar (son dal mı değil mi)
        lines.append(get_ast(child, indent + 1, markers + [not is_last]))

    return "\n".join(lines)
