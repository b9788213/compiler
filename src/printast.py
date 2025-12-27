from node import *

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
        if isinstance(n, Program): return "Program"
        if isinstance(n, Func): return f"Func(name='{n.name}', args={n.args})"
        if isinstance(n, BinOp): return f"BinOp(op='{n.op}')"
        if isinstance(n, Comp): return f"Comp(op='{n.op}')"
        if isinstance(n, Assign): return f"Assign(name='{n.name}')"
        if isinstance(n, Call): return f"Call(name='{n.name}')"
        if isinstance(n, Neg): return "Neg(-)"
        if isinstance(n, Ret): return "Ret"
        if isinstance(n, (Int, Float, String, Id)):
            val = getattr(n, 'value', getattr(n, 'name', ''))
            return f"{type(n).__name__}({val})"
        return f"Unknown({type(n).__name__})"

    lines.append(f"{prefix}{get_node_info(node)}")

    # Alt düğümleri (children) topla
    children = []
    if isinstance(node, Program):
        children.extend(node.funcs)
        children.extend(node.statics)
    elif isinstance(node, Func):
        children.extend(node.body)
    elif isinstance(node, (BinOp, Comp)):
        children.append(node.left)
        children.append(node.right)
    elif isinstance(node, Assign):
        children.append(node.value)
    elif isinstance(node, Call):
        children.extend(node.args)
    elif isinstance(node, (Neg, Ret)):
        children.append(node.value)

    # Çocukları recursive olarak işle
    for i, child in enumerate(children):
        is_last = (i == len(children) - 1)
        # Alt dallara markers bilgisini aktar (son dal mı değil mi)
        lines.append(get_ast(child, indent + 1, markers + [not is_last]))

    return "\n".join(lines)