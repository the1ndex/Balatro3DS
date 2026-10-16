from pathlib import Path
import subprocess,hashlib,json
root=Path.cwd();up=root/'work/v2.0.3-zh-fixes'
ctr=root/'work/cia-tools/ctrtool/ctrtool.exe';cia=root/'outputs/v2.0.3-zh-fixes/Balatro3DS-2.0.3-zh-fix2.cia'
work=up/'work'/('validation-'+hashlib.sha256(cia.read_bytes()).hexdigest()[:12]);work.mkdir(parents=True,exist_ok=True)
def run(name,*args):
 p=subprocess.run([str(ctr),*map(str,args)],capture_output=True,text=True);s=p.stdout+p.stderr;(work/(name+'.log')).write_text(s,encoding='utf-8');assert p.returncode==0,s[-2000:];return s
s=run('cia','-y','--contents='+str(work/'content'),cia)
assert s.count('DigitalSignature: (GOOD)')==3
assert 'Hash: (GOOD)' in s
ncch=list(work.glob('content.*'));assert len(ncch)==1
s=run('ncch','-y','--exheader='+str(work/'exheader.bin'),'--exefs='+str(work/'exefs.bin'),'--romfsdir='+str(work/'romfs'),ncch[0])
for p in ['ExeFS hash: (GOOD)','RomFS hash: (GOOD)','Exheader hash: (GOOD)','Level 0: (GOOD)','Level 1: (GOOD)','Level 2: (GOOD)']:assert p in s,p
run('exefs','-t','exefs','--decompresscode','--exefsdir='+str(work/'exefs'),work/'exefs.bin')
assert (work/'exefs/code.bin').read_bytes()==(up/'work/release-exefs/code.bin').read_bytes()
assert (work/'exheader.bin').read_bytes()[:0x400]==(up/'work/release.exheader').read_bytes()[:0x400],'runtime process settings changed'
for name in ['icon.bin','banner.bin']:assert (work/'exefs'/name).read_bytes()==(up/'work/release-exefs'/name).read_bytes()
game=work/'romfs/Balatro3DS';staged=up/'work/patched-romfs/Balatro3DS';count=0
for p in staged.rglob('*'):
 if p.is_file():assert p.read_bytes()==(game/p.relative_to(staged)).read_bytes();count+=1
for name in ['fonts.lua','game.lua','main.lua','shop_ui.lua','consumable.lua','main_menu_ui.lua','topUI.lua','milestone_queue.lua','utf8_text.lua']:assert (game/name).read_bytes()==(up/name).read_bytes()
assert b'preview-hook' not in (game/'main.lua').read_bytes()
report={'file':cia.name,'sha256':hashlib.sha256(cia.read_bytes()).hexdigest(),'romfs_files_verified':count,'native_code_unchanged':True,'native_process_settings_unchanged':True,'banner_and_icon_unchanged':True,'data_hashes':'passed','title_id':'000400000BA1A700','hardware_tested':False}
(root/'outputs/v2.0.3-zh-fixes/validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
