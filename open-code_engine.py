import os, json, re
SHARED_DIR = "/tmp/bodhi_workspace"
TARGET_REPO = os.environ.get("TARGET_REPO", "retina")

print(f"🧬 [OPEN-CODE] Bắt đầu vi phẫu AST nội hàm cho {TARGET_REPO}...")
code_data = {"classes": [], "functions": []}

try:
    with open(f"{SHARED_DIR}/file_data.json", "r") as f: files = json.load(f)["files"]
    for fitem in files:
        p = fitem["path"]
        if not p.endswith((".py", ".js", ".ts", ".java", ".go", ".rs", ".c", ".cpp")): continue
        full_p = os.path.join(SHARED_DIR, TARGET_REPO, p)
        try:
            with open(full_p, "r", errors="ignore") as fr: lines = fr.readlines()
            for lno, line in enumerate(lines, 1):
                cm = re.search(r'^\s*class\s+([A-Za-z0-9_]+)', line)
                if cm: code_data["classes"].append({"file": p, "name": cm.group(1), "line": lno})
                fm = re.search(r'^\s*(?:async\s+)?def\s+([A-Za-z0-9_]+)\s*\((.*?)\)', line)
                if fm:
                    snippet = "".join(lines[lno:lno+15])
                    code_data["functions"].append({"file": p, "name": fm.group(1), "line": lno, "snippet": snippet})
        except: pass
    with open(f"{SHARED_DIR}/code_data.json", "w") as f: json.dump(code_data, f)
    print("✅ [OPEN-CODE] Đã bóc tách xong Class và Hàm.")
except Exception as e: print(f"⚠️ Lỗi: {e}")
