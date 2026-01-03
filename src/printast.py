from node import (
    Asm,
    BinOp,
    Program,
    Comp,
    Call,
    ConditionelStruct,
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
        if isinstance(n, Asm):
            return "Asm"
        if isinstance(n, Program):
            return "Program"
        if isinstance(n, Func):
            return f"Func({n.name}, args={n.args})"
        if isinstance(n, BinOp):
            return f"BinOp({n.op})"
        if isinstance(n, Comp):
            return f"Comp({n.op})"
        if isinstance(n, Assign):
            return f"Assign({n.name})"
        if isinstance(n, Call):
            return f"Call({n.name})"
        if isinstance(n, Neg):
            return "Neg(-)"
        if isinstance(n, Ret):
            return "Ret"
        if isinstance(n, While):
            return "While"
        if isinstance(n, ConditionelStruct):
            return "ConditionelStruct"
        if isinstance(n, If):
            return "If"
        if isinstance(n, Int):
            return f"Int({n.value})"
        if isinstance(n, Float):
            return f"Float({n.value})"
        if isinstance(n, String):
            return f"String({repr(n.value)})"
        if isinstance(n, Id):
            return f"Id({n.name})"
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
    elif isinstance(node, ConditionelStruct):
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
