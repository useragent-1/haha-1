#!/usr/bin/env python3
"""Install a matching asset from the latest public GitHub release into /usr/local/bin."""
from __future__ import annotations
import argparse,gzip,json,os,pathlib,re,shutil,stat,subprocess,tarfile,tempfile,urllib.request,zipfile

def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'haha-1-tool-installer/1.0','Accept':'application/vnd.github+json'})
 with urllib.request.urlopen(req,timeout=30) as r:return r.read()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('repo');ap.add_argument('binary');ap.add_argument('--asset-regex',default=r'(?i)linux.*(?:amd64|x86_64).*(?:tar\.gz|tgz|zip)$');ap.add_argument('--rename');ns=ap.parse_args()
 release=json.loads(fetch(f'https://api.github.com/repos/{ns.repo}/releases/latest'));rx=re.compile(ns.asset_regex);assets=[a for a in release.get('assets',[]) if rx.search(a['name'])]
 if not assets:raise SystemExit(f'FAIL no matching release asset for {ns.repo}; assets={[a["name"] for a in release.get("assets",[])]}')
 asset=assets[0];print(f"release={release.get('tag_name')} asset={asset['name']} size={asset.get('size')}")
 with tempfile.TemporaryDirectory() as td:
  t=pathlib.Path(td);archive=t/asset['name'];archive.write_bytes(fetch(asset['browser_download_url']));out=t/'x';out.mkdir()
  if asset['name'].endswith('.deb'):
   subprocess.run(['sudo','apt-get','install','-y',str(archive)],check=True);print(f'installed_deb={archive.name}');return
  if asset['name'].endswith('.zip'):zipfile.ZipFile(archive).extractall(out)
  elif asset['name'].endswith(('.tar.gz','.tgz')):tarfile.open(archive,'r:*').extractall(out,filter='data')
  elif asset['name'].endswith('.gz'):
   raw=out/ns.binary
   with gzip.open(archive,'rb') as src,raw.open('wb') as dst:shutil.copyfileobj(src,dst)
  else:raise SystemExit(f'FAIL unsupported asset format: {asset["name"]}')
  candidates=[p for p in out.rglob('*') if p.is_file() and p.name==ns.binary]
  if not candidates:raise SystemExit(f'FAIL binary {ns.binary} absent; files={[str(p.relative_to(out)) for p in out.rglob("*") if p.is_file()][:80]}')
  src=candidates[0];dest=pathlib.Path('/usr/local/bin')/(ns.rename or ns.binary);subprocess.run(['sudo','install','-m','0755',str(src),str(dest)],check=True);print(f'installed={dest}')
if __name__=='__main__':main()
