import re

def contains_relevant_text(line):
    if len(line.strip()) < 13:
        return False

    if line.strip().startswith("%"):
        return False

    excludeds = "begin, end, label, includegraphics, todo, FloatBarrier".split(",")
    excludeds = [f"\\{ex.strip()}" for ex in excludeds]
    if any([line.strip().startswith(ex) for ex in excludeds]):
        return False
    
    return True

def reduce_tokens(lines):
    # remove any line starting with caption shorter than 60 characters
    lines = [line for line in lines if not line.strip().startswith(r"\caption") or len(line) > 60]
    # remove any line ending on \\ as they are in a table
    lines = [line for line in lines if not line.strip().endswith(r"\\")]
    # replace any (\cref{...}) with '' as they are not semantically needed
    expr = r"\(\\cref\{[^\}]+\}\)"
    lines = [re.sub(expr, "", line) for line in lines]
    # replace all \caption[...] with \caption as they are for the list of X
    expr = r"caption\[[^\]]+\]"
    lines = [re.sub(expr, r"caption", line) for line in lines]
    # replace all \gls{...} with ...
    expr = r"\\gls\{([^\}]+)\}"
    lines = [re.sub(expr, r"\1", line) for line in lines]
    # replace all \qty{x}{unit} with x unit
    units = [r"\\milli\\metre", r"\\centi\\metre", r"\\px", r"\\milli\\metre\\per\\frame\\squared", r"\\percent"]
    unitsto = ["mm", "cm", "px", "mm/frame^2", "\%"]
    for unit, to in zip(units, unitsto):
        expr = r"\\qty\{([^\}]+)\}\{" + unit + r"\}"
        lines = [re.sub(expr, r"\1 " + to, line) for line in lines]
        expr = r"\\qtyrange\{([^\}]+)\}\{([^\}]+)\}\{" + unit + r"\}"
        lines = [re.sub(expr, r"\1 to \2 " + to, line) for line in lines]
    # replace \paragraph{...} with ...
    expr = r"\\paragraph\{([^\}]+)\}"
    lines = [re.sub(expr, r"\1", line) for line in lines]

    return lines

def read_file(path, by_line=True):
    with open(path, "r", encoding="utf-8") as file:
        if by_line:
            return file.readlines()
        else:
            return file.read()
    
def write_file(path, content, by_line=True):
    with open(path, "w", encoding="utf-8") as file:
        if by_line:
            file.writelines(content)
        else:
            file.write(content)

def filter_and_merge_files(paths):
    lines = []
    for path in paths:
        lines.extend(read_file(path))
    lines = [line for line in lines if contains_relevant_text(line)]
    write_file("merged.tex", lines)
