"""断点续传下载（应对 CDN 中途断流）。"""
from __future__ import annotations

import os
import sys
import time
import urllib.request
from urllib.parse import quote

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
CHUNK = 32 << 20  # 每段 32MB


def total_size(url: str) -> int:
    req = urllib.request.Request(quote(url, safe=":/?&=%#"), method="HEAD", headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return int(r.headers.get("Content-Length") or 0)


def fetch_range(url: str, start: int, end: int, retries: int = 6) -> bytes:
    for attempt in range(retries):
        try:
            h = dict(UA)
            h["Range"] = "bytes=%d-%d" % (start, end)
            req = urllib.request.Request(quote(url, safe=":/?&=%#"), headers=h)
            with urllib.request.urlopen(req, timeout=300) as r:
                data = r.read()
            if data:
                return data
        except Exception as e:
            print("   段 %d-%d 第%d次失败: %s" % (start, end, attempt + 1, e), flush=True)
            time.sleep(3 + attempt * 2)
    return b""


def download(url: str, dest: str) -> bool:
    size = total_size(url)
    if not size:
        print("无法获取文件大小", flush=True)
        return False
    print("目标 %s，共 %.2f GB" % (dest, size / (1 << 30)), flush=True)
    done = os.path.getsize(dest) if os.path.exists(dest) else 0
    with open(dest, "ab") as f:
        while done < size:
            end = min(done + CHUNK - 1, size - 1)
            data = fetch_range(url, done, end)
            if not data:
                print("  连续失败，停止（已下 %.1f MB）" % (done / 1048576), flush=True)
                return False
            f.write(data)
            f.flush()
            done += len(data)
            print("  %.1f%%  %.0f MB / %.0f MB" % (done * 100 / size, done / 1048576, size / 1048576), flush=True)
    print("完成", flush=True)
    return done == size


if __name__ == "__main__":
    url, dest = sys.argv[1], sys.argv[2]
    ok = download(url, dest)
    print("RESULT", "OK" if ok else "INCOMPLETE")
