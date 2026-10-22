"""抓取 MathorCup 大数据竞赛历年赛题与附件（官方站 + 赛氪 CDN）。

输出：D:\\ModexWork\\MathorCup大数据赛\\raw\\<年份_轮次>\\<原文件名>
清单：manifest.json
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import quote

ROOT = Path(r"D:\ModexWork\MathorCup大数据赛")
RAW = ROOT / "raw"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 官方公告页 → 归属标签
PAGES = {
    "2393": ("历年汇总", "https://mathorcup.org/detail/2393"),
    "2398": ("2022_第三届_初赛", "https://mathorcup.org/detail/2398"),
    "2433": ("2023_第四届_初赛", "https://mathorcup.org/detail/2433"),
    "2448": ("2024_第五届_初赛", "https://mathorcup.org/detail/2448"),
    "2455": ("2024_第五届_复赛", "https://mathorcup.org/detail/2455"),
    "2463": ("2025_第六届_初赛", "https://mathorcup.org/detail/2463"),
    "2467": ("2025_第六届_复赛", "https://mathorcup.org/detail/2467"),
    "2468": ("2025_第六届_复赛验证集A", "https://mathorcup.org/detail/2468"),
}

# 赛氪公告页（2020 年赛题挂在这里）
SAIKR = {
    "7255": ("2020_第一届_赛道A", "https://www.saikr.com/c/nd/7255"),
    "7256": ("2020_第一届_赛道B", "https://www.saikr.com/c/nd/7256"),
    "14811": ("2023_第四届_赛道A", "https://www.saikr.com/c/nd/14811"),
}


def fetch(url: str, timeout=60) -> bytes:
    req = urllib.request.Request(quote(url, safe=":/?&=%#"), headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def safe_name(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]', "_", name)
    return name.strip()[:120] or "file"


def download(url: str, dest: Path, referer: str) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        print("   跳过（已存在）", dest.name)
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        safe_url = quote(url, safe=":/?&=%#")
        req = urllib.request.Request(safe_url, headers={**UA, "Referer": referer})
        with urllib.request.urlopen(req, timeout=300) as r, open(dest, "wb") as f:
            total = 0
            while True:
                chunk = r.read(1 << 16)
                if not chunk:
                    break
                f.write(chunk)
                total += len(chunk)
        print("   ↓ %-52s %6.1f MB" % (dest.name, total / 1048576))
        return True
    except Exception as e:
        print("   ✗ 失败", url, e)
        if dest.exists():
            dest.unlink(missing_ok=True)
        return False


def name_from_url(url: str, fallback: str) -> str:
    m = re.search(r"attname=([^&]+)", url)
    if m:
        from urllib.parse import unquote
        return safe_name(unquote(m.group(1)))
    base = url.split("?")[0].rstrip("/").split("/")[-1]
    return safe_name(base or fallback)


def run():
    manifest = []
    RAW.mkdir(parents=True, exist_ok=True)

    for pid, (label, url) in PAGES.items():
        print("\n== %s (%s)" % (label, url))
        try:
            html = fetch(url).decode("utf-8", "replace")
        except Exception as e:
            print("  页面抓取失败:", e)
            continue
        files = sorted(set(re.findall(r'href="(/uploads/files/[^"]+)"', html)))
        if not files:
            print("  无站内附件")
        cdn = sorted(set(re.findall(r'(https://publicqn\.saikr\.com/[^"\']+?\.(?:zip|rar|7z))(?=["\'])', html)))
        for full in cdn:
            fname = name_from_url(full, "saikr_file")
            ok = download(full, RAW / label / fname, url)
            manifest.append({"year_label": label, "source": url, "url": full,
                             "file": str((RAW / label / fname).relative_to(RAW)), "ok": ok})
        for rel in files:
            full = "https://mathorcup.org" + rel
            fname = name_from_url(full, rel.split("/")[-1])
            dest = RAW / label / fname
            ok = download(full, dest, url)
            manifest.append({"year_label": label, "source": url, "url": full,
                             "file": str(dest.relative_to(RAW)), "ok": ok})
        time.sleep(0.6)

    for sid, (label, url) in SAIKR.items():
        print("\n== %s (%s)" % (label, url))
        try:
            html = fetch(url).decode("utf-8", "replace")
        except Exception as e:
            print("  页面抓取失败:", e)
            continue
        cdn = sorted(set(re.findall(r'(https://publicqn\.saikr\.com/[^"\']+\.(?:zip|rar|7z|pdf|xlsx))', html)))
        if not cdn:
            print("  未发现 CDN 附件直链（可能需要登录）")
        for full in cdn:
            fname = name_from_url(full, "saikr_file")
            dest = RAW / label / fname
            ok = download(full, dest, url)
            manifest.append({"year_label": label, "source": url, "url": full,
                             "file": str(dest.relative_to(RAW)), "ok": ok})
        time.sleep(0.6)

    (ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = sum(1 for m in manifest if m["ok"])
    total = sum((RAW / m["file"]).stat().st_size for m in manifest if (RAW / m["file"]).exists())
    print("\n完成：%d/%d 个文件，共 %.1f MB" % (ok, len(manifest), total / 1048576))


if __name__ == "__main__":
    run()
