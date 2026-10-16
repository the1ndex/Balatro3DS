"""Check locale coverage, native sheet maps and baseline metrics before packaging."""
from zh_release_config import *
from fontTools.ttLib import TTFont
from bcfnt import inspect
cmap=set(TTFont(UP/"resources/fonts/zh_CN.ttf").getBestCmap())
text="".join(p.read_text(encoding="utf-8") for p in [UP/"locales/zh_CN.lua",*(UP/"locales/content/zh_CN").glob("*.lua")])
missing={ord(c) for c in text if c.isprintable()}-cmap
assert not missing, "Missing glyphs: "+repr("".join(map(chr,sorted(missing))))
results=[]
for h in [13,17,21,27,33]:
    result=inspect(UP/("resources/fonts/lang/zh_CN_h"+str(h)+".bcfnt"))
    assert set(result.pop("mappings"))==cmap
    assert result["cell_height"]==result["finf_height"]==h
    assert result["baseline"]==result["finf_ascent"]
    results.append(result)
OUT.mkdir(parents=True,exist_ok=True)
(OUT/"font-validation.json").write_text(json.dumps(results,indent=2),encoding="utf-8")
print("5 native sheets verified;",len(cmap),"glyphs; no missing Chinese characters")
