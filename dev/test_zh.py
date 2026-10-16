"""Run the maintained branch's localization and affected UI regression checks."""
from pathlib import Path
import os,json
from lupa.luajit21 import LuaRuntime
from zh_release_config import UP,OUT
os.chdir(UP);OUT.mkdir(parents=True,exist_ok=True)
lua=LuaRuntime(unpack_returned_tuples=True)
results=[]
suites=["test_localization","test_fonts","test_input_bindings","test_zh_ui_fixes",
    "test_milestone_queue","test_shop_rendering","test_shop_layering","test_tooltip_wrap",
    "test_accessibility_settings","test_game_over_summary","test_deck_view","test_zh_upstream_sync"]
for name in suites:
    suite=lua.eval("require")("tests."+name)
    for _,test in suite["_order"].items():
        ok,error=lua.eval('function(f) local ok,e=pcall(f);return ok,type(e)=="table" and e.message or tostring(e) end')(suite["_tests"][test])
        results.append({"suite":name,"name":test,"passed":ok,"error":None if ok else error})
        if not ok:print("FAIL",name,test,error)
(OUT/"tests.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
print(sum(r["passed"] for r in results),"/",len(results),"passed")
raise SystemExit(0 if all(r["passed"] for r in results) else 1)
