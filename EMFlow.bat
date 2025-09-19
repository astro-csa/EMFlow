@echo off

wsl -d Ubuntu-24.04 -e bash -lc "bash ~/EMFlow/run.sh %*"

pause