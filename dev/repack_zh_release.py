"""Rebuild RomFS around the unmodified official v2.0.3 native runtime."""
from pathlib import Path
import shutil,subprocess,json,hashlib,re
UP=Path(__file__).resolve().parents[1];ROOT=UP.parents[1]
WORK=UP/'work';TOOLS=ROOT/'work/cia-tools';OUT=ROOT/'outputs/v2.0.3-zh-fixes';OUT.mkdir(parents=True,exist_ok=True)
def run(exe,*args):
 p=subprocess.run([str(exe),*map(str,args)],cwd=UP,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 return p.stdout+p.stderr
stage=WORK/'patched-romfs';shutil.copytree(WORK/'release-romfs',stage,dirs_exist_ok=True)
game=stage/'Balatro3DS'
changed=[]
for path in UP.glob('*.lua'):
 dest=game/path.name
 # Preserve release-only build flags and timestamp, and use stock release conf.lua.
 if path.name in {'build_flags.lua','build_info.lua','conf.lua'}:continue
 if dest.is_file() and dest.read_bytes()!=path.read_bytes():changed.append(path.name)
 shutil.copyfile(path,dest)
shutil.copytree(UP/'locales',game/'locales',dirs_exist_ok=True)
for h in [13,17,21,27,33]:shutil.copyfile(UP/f'resources/fonts/lang/zh_CN_h{h}.bcfnt',game/f'resources/fonts/lang/zh_CN_h{h}.bcfnt')
shutil.copyfile(UP/'resources/fonts/OFL-zh_CN.txt',game/'resources/fonts/OFL-zh_CN.txt')
# Remove unused font faces from this generated staging directory only.
for h in [26,32]:
 p=game/f'resources/fonts/lang/zh_CN_h{h}.bcfnt'
 if p.exists():p.unlink()
rsf=(UP/'dev/cia/balatro.rsf').read_text()
for key,val in {'APP_TITLE':'Balatro','APP_PRODUCT_CODE':'CTR-H-BLTR','APP_UNIQUE_ID':'0xBA1A7','APP_ROMFS':stage.as_posix(),'APP_VERSION_MAJOR':'2'}.items():rsf=rsf.replace('$('+key+')',val)
(WORK/'rebuild.rsf').write_text(rsf,encoding='utf-8')
exefs=WORK/'release-exefs';cxi=WORK/'patched.cxi';final=OUT/'Balatro3DS-2.0.3-zh-fix2.cia'
print(run(TOOLS/'makerom/makerom.exe','-f','ncch','-target','t','-ignoresign','-exefslogo','-o',cxi,'-rsf',WORK/'rebuild.rsf','-code',exefs/'code.bin','-exheader',WORK/'release.exheader','-icon',exefs/'icon.bin','-banner',exefs/'banner.bin'),flush=True)
print(run(TOOLS/'makerom/makerom.exe','-f','cia','-target','p','-ignoresign','-i',str(cxi)+':0:0','-o',final,'-major','2','-minor','0','-micro','3'),flush=True)
report={'source_version':'v2.0.3-base','source_commit':'cd474a4d83aeabf16cb8695e30ef0309f81921f5','native_code_sha256':hashlib.sha256((exefs/'code.bin').read_bytes()).hexdigest(),'output':final.name,'bytes':final.stat().st_size,'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'title_id':'000400000BA1A700','changed_root_lua':changed,'hardware_tested':False,'save_path':'SD:/3ds/save/Balatro3DS/sdmc/'}
(OUT/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
