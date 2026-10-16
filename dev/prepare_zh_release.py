"""Download and verify the exact official CIA pinned in zh-upstream.json."""
from zh_release_config import *
import hashlib, urllib.request
RELEASE.mkdir(parents=True, exist_ok=True)
cia = RELEASE / "upstream.cia"
expected = CONFIG["release_cia_sha256"]
if not cia.is_file() or hashlib.sha256(cia.read_bytes()).hexdigest() != expected:
    request = urllib.request.Request(CONFIG["release_cia_url"], headers={"User-Agent": "Balatro3DS-zh-maintenance"})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != expected:
        raise RuntimeError("Official CIA hash mismatch; no runtime extracted")
    cia.write_bytes(data)
ctr = TOOLS / "ctrtool/ctrtool.exe"
text = run(ctr, "-y", "--contents=" + str(RELEASE / "content"), cia)
assert "Hash: (GOOD)" in text
contents = list(RELEASE.glob("content.*"))
assert len(contents) == 1
text = run(ctr, "-y", "--exheader=" + str(RELEASE / "release.exheader"),
    "--exefs=" + str(RELEASE / "release.exefs"), "--romfsdir=" + str(RELEASE / "release-romfs"), contents[0])
for item in ["ExeFS hash: (GOOD)", "RomFS hash: (GOOD)", "Exheader hash: (GOOD)", "Level 2: (GOOD)"]:
    assert item in text, item
run(ctr, "-t", "exefs", "--decompresscode", "--exefsdir=" + str(RELEASE / "release-exefs"), RELEASE / "release.exefs")
report = {"tag": TAG, "cia_sha256": expected,
    "native_code_sha256": hashlib.sha256((RELEASE / "release-exefs/code.bin").read_bytes()).hexdigest()}
(RELEASE / "prepared.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
