# -*- coding: utf-8 -*-
import json, io, os

BASE = r"C:\Users\Lenovo\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a87c4afd7307a4423d42f59"
tpl_path = os.path.join(BASE, "template.html")
db_path = os.path.join(BASE, "db.json")
out_path = os.path.join(BASE, "考公学习工作台.html")

tpl = io.open(tpl_path, encoding='utf-8').read()
db = io.open(db_path, encoding='utf-8').read()

# 转义可能破坏 <script> 的序列（安全起见替换 </ -> <\/）
db_safe = db.replace('</', '<\\/')

marker = '/*__DB_JSON__*/null'
assert marker in tpl, "marker not found"
out = tpl.replace(marker, db_safe)

io.open(out_path, 'w', encoding='utf-8').write(out)
print("written:", out_path)
print("size bytes:", os.path.getsize(out_path))
print("db safe len:", len(db_safe))