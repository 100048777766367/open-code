import os, json, re

WORKSPACE = "/tmp/bodhi_dissector"
os.chdir(WORKSPACE)

print("🧬 [OPEN-CODE REAL ENGINE] Đang vi phẫu AST bóc tách Class và Hàm...")
code_result = {"classes": [], "functions": []}

try:
    with open("file_out.json", "r") as f: files = json.load(f)["files"]
    repos = [d for d in os.listdir(".") if os.path.isdir(d) and d not in ["storage"]]
    target_repo = repos[0] if repos else "retina"

    for fitem in files:
        p = fitem["path"]
        if not p.endswith((".py", ".js", ".ts", ".java", ".go", ".rs", ".c", ".cpp")): continue
        full_p = os.path.join(target_repo, p)
        try:
            with open(full_p, "r", errors="ignore") as fr: lines = fr.readlines()
            for lno, line in enumerate(lines, 1):
                cm = re.search(r'^\s*class\s+([A-Za-z0-9_]+)', line)
                if cm: code_result["classes"].append({"file": p, "name": cm.group(1), "line": lno})
                fm = re.search(r'^\s*(?:async\s+)?def\s+([A-Za-z0-9_]+)\s*\((.*?)\)', line)
                if fm:
                    snippet = "".join(lines[lno:lno+15])
                    code_result["functions"].append({"file": p, "name": fm.group(1), "line": lno, "snippet": snippet})
        except: pass

    with open("code_out.json", "w") as f: json.dump(code_result, f)
    print(f"✅ [OPEN-CODE] Vi phẫu xong {len(code_result['classes'])} Class và {len(code_result['functions'])} Hàm vào `code_out.json`.")
except Exception as e:
    print(f"🔴 Lỗi ở open-code: {e}")
