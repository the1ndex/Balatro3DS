"""Rebuild RomFS around the unmodified official runtime pinned in zh-upstream.json."""
from zh_release_config import *
import shutil, json, hashlib
prepared=json.loads((RELEASE/'prepared.json').read_text(encoding='utf-8'))
assert prepared['tag']==TAG and prepared['cia_sha256']==CONFIG['release_cia_sha256']
OUT.mkdir(parents=True,exist_ok=True)
stage=RELEASE/'patched-romfs';shutil.copytree(RELEASE/'release-romfs',stage,dirs_exist_ok=True)
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
for key,val in {'APP_TITLE':'Balatro','APP_PRODUCT_CODE':'CTR-H-BLTR','APP_UNIQUE_ID':'0xBA1A7','APP_ROMFS':stage.as_posix(),'APP_VERSION_MAJOR':VERSION.split('.')[0]}.items():rsf=rsf.replace('$('+key+')',val)
(WORK/'rebuild.rsf').write_text(rsf,encoding='utf-8')
exefs=RELEASE/'release-exefs';assert hashlib.sha256((exefs/'code.bin').read_bytes()).hexdigest()==prepared['native_code_sha256'];cxi=RELEASE/'patched.cxi';final=OUT/(NAME+'.cia')
print(run(TOOLS/'makerom/makerom.exe','-f','ncch','-target','t','-ignoresign','-exefslogo','-o',cxi,'-rsf',WORK/'rebuild.rsf','-code',exefs/'code.bin','-exheader',RELEASE/'release.exheader','-icon',exefs/'icon.bin','-banner',exefs/'banner.bin'),flush=True)
print(run(TOOLS/'makerom/makerom.exe','-f','cia','-target','p','-ignoresign','-i',str(cxi)+':0:0','-o',final,'-major',VERSION.split('.')[0],'-minor',VERSION.split('.')[1],'-micro',VERSION.split('.')[2]),flush=True)
report={'source_version':TAG,'source_commit':CONFIG['upstream_commit'],'native_code_sha256':hashlib.sha256((exefs/'code.bin').read_bytes()).hexdigest(),'output':final.name,'bytes':final.stat().st_size,'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'title_id':'000400000BA1A700','changed_root_lua':changed,'hardware_tested':False,'save_path':'SD:/3ds/save/Balatro3DS/sdmc/'}
(OUT/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
