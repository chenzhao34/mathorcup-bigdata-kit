@echo off
chcp 65001 >nul
title MathorCup 大数据模板注入器
cd /d "D:\ModexWork\mathorcup-bigdata-kit\tools"

echo 正在监听工作区，论文步骤落盘 _templates\mathorcup 时自动替换为大数据赛模板。
echo 关闭本窗口即停止。
echo.

"D:\Modex-MH-Agent\runtime\python\python.exe" inject_templates.py --watch
pause
