"""Check upstream releases, falling back to stable-form tags on API rate limiting."""
from pathlib import Path
import json, re, subprocess, urllib.request, urllib.error, sys
up=Path(__file__).resolve().parents[1]
config=json.loads((up/"zh-upstream.json").read_text(encoding="utf-8"))
subprocess.run(["git","fetch","upstream","--tags","--prune"],cwd=up,check=True)
request=urllib.request.Request("https://api.github.com/repos/idkhan/Balatro3DS/releases/latest",headers={"User-Agent":"Balatro3DS-zh-maintenance"})
try:
    with urllib.request.urlopen(request,timeout=60) as response:release=json.load(response)
    assert not release["draft"] and not release["prerelease"]
    asset=next(a for a in release["assets"] if a["name"]=="Balatro.cia")
    result={"latest":release["tag_name"],"url":release["html_url"],"source":"github-release",
        "published_at":release["published_at"],"cia_url":asset["browser_download_url"],"cia_digest":asset.get("digest")}
except urllib.error.HTTPError as error:
    if error.code not in (403,429):raise
    tags=subprocess.check_output(["git","tag","--merged","upstream/main","--sort=-version:refname"],cwd=up,text=True).splitlines()
    latest=next(tag for tag in tags if re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+-base",tag))
    result={"latest":latest,"url":config["repository"]+"/releases/tag/"+latest,"source":"git-tags-fallback",
        "note":"GitHub API rate limited; tag verified, release status must be checked before merging a new tag."}
result.update(current=config["upstream_tag"],needs_sync=result["latest"]!=config["upstream_tag"])
print(json.dumps(result,ensure_ascii=False,indent=2))
