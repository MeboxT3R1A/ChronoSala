import os

# Ignorar pastas/arquivos indesejados
EXCLUDE = {"venv", ".venv", "__pycache__", ".git", ".DS_Store"}
EXCLUDE_EXT = {".pyc", ".pyo", ".log", ".txt"}

# Define o que não deve aparecer
def should_exclude(entry):
    if entry in EXCLUDE:
        return True
    if os.path.splitext(entry)[1] in EXCLUDE_EXT:
        return True
    return False

# Adiciona comentários automáticos (personalize por nome se quiser)
def annotate(rel_path, filename):
    norm_path = rel_path.replace("\\", "/").lower()

    if filename == "gerar_estrutura.py":
        return "← Gera estrutura de diretórios (essa aqui)"
    elif filename == "":
        return "← "
    return ""

# Monta a árvore com indentação e comentários
def build_tree(dir_path, prefix='', rel_path=''):
    entries = sorted([e for e in os.listdir(dir_path) if not should_exclude(e)])
    lines = []
    for i, entry in enumerate(entries):
        path = os.path.join(dir_path, entry)
        rel_entry_path = os.path.join(rel_path, entry)  # ← caminho relativo
        connector = '└── ' if i == len(entries) - 1 else '├── '
        
        comment = annotate(rel_entry_path, entry)  # ← CORREÇÃO AQUI
        
        line = f"{prefix}{connector}{entry}/" if os.path.isdir(path) else f"{prefix}{connector}{entry}"
        if comment:
            line += f" {comment}"
        lines.append(line)
        if os.path.isdir(path):
            extension = '    ' if i == len(entries) - 1 else '│   '
            lines.extend(build_tree(path, prefix + extension, rel_entry_path))
    return lines

# Pasta onde o script está
root_dir = os.path.abspath(os.path.dirname(__file__))
root_name = os.path.basename(root_dir)

# Gera a estrutura
estrutura = [f"{root_name}/"] + build_tree(root_dir)

# Salva no arquivo estrutura.txt
output_path = os.path.join(root_dir, "estrutura.txt")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(estrutura))

print(f"Arquivo '{output_path}' gerado com sucesso.")
