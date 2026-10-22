"""把 MathorCup 大数据赛模板注入到运行中的工作区。

背景：Modex 的竞赛技能是服务端下发的加密胶囊，模板直到论文步骤才开始
落盘到 <workspace>/_templates/。因此无法通过改安装目录生效，只能在
_templates 出现的瞬间替换。

用法：
    python inject_templates.py --once <workspace_dir>     # 对已有工作区立即注入
    python inject_templates.py --watch                    # 常驻监听所有工作区
"""
from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

KIT = Path(r"D:\ModexWork\mathorcup-bigdata-kit\templates\mathorcup_bigdata")
ROOT = Path(r"C:\Users\lenovo\AppData\Roaming\MHAgent\workspaces")
MARK = ".bigdata_injected"
TARGET = "mathorcup"          # 技能里的模板目录名
BACKUP = ".backup_mathorcup"


def log(msg: str) -> None:
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def is_bigdata(ws: Path) -> bool:
    """从工作区 CLAUDE.md 判断是否为大数据赛（避免误伤常规赛）。"""
    f = ws / "CLAUDE.md"
    if not f.exists():
        return False
    try:
        t = f.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False
    keys = ("大数据", "BigData", "bigdata", "MathorCup数学应用挑战赛——大数据")
    return any(k in t for k in keys)


def inject(ws: Path, force: bool = False, check_comp: bool = True) -> bool:
    """把模板写入 ws/_templates/mathorcup/，首次覆盖前备份原文件。"""
    if check_comp and not force and not is_bigdata(ws):
        return False
    tmpl_dir = ws / "_templates" / TARGET
    if not tmpl_dir.exists():
        return False
    mark = tmpl_dir / MARK
    if mark.exists() and not force:
        return False

    backup = ws / "_templates" / BACKUP
    backup.mkdir(parents=True, exist_ok=True)
    moved = 0
    for f in tmpl_dir.iterdir():
        if f.is_file() and f.name != MARK:
            dst = backup / f.name
            if not dst.exists():
                shutil.copy2(f, dst)
                moved += 1

    copied = []
    for src in KIT.iterdir():
        if src.is_file():
            shutil.copy2(src, tmpl_dir / src.name)
            copied.append(src.name)

    mark.write_text("injected at %s\n" % time.strftime("%Y-%m-%d %H:%M:%S"), encoding="utf-8")
    log("%s → 注入 %d 个模板文件（备份原文件 %d 个）" % (ws.name, len(copied), moved))
    return True


def watch(interval: float = 2.0, force: bool = False) -> None:
    log("监听工作区：%s" % ROOT)
    seen: set[str] = set()
    while True:
        try:
            for ws in ROOT.iterdir():
                if not ws.is_dir():
                    continue
                tmpl = ws / "_templates" / TARGET
                if tmpl.exists():
                    key = str(tmpl)
                    if key not in seen:
                        if inject(ws, force=force):
                            seen.add(key)
                    elif not (tmpl / MARK).exists():
                        # 被步骤覆盖后重新注入
                        if inject(ws):
                            seen.add(key)
        except Exception as e:
            log("监听异常: %s" % e)
        time.sleep(interval)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", metavar="WORKSPACE")
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--force", action="store_true", help="跳过赛事识别，强制注入")
    ap.add_argument("--all", action="store_true", help="同 --force")
    a = ap.parse_args()

    if a.once:
        ws = Path(a.once)
        if not ws.exists():
            print("工作区不存在:", ws)
            return 1
        ok = inject(ws, force=(a.force or a.all))
        if not ok:
            if not is_bigdata(ws):
                print("已跳过：%s 不像大数据赛（CLAUDE.md 无相关标识）；确需注入加 --force" % ws.name)
            else:
                print("未注入：%s 下还没有 _templates/%s（等论文步骤开始后再执行）" % (ws, TARGET))
            return 2
        return 0

    if a.watch:
        watch(force=(a.force or a.all))
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
