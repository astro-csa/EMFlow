@echo off

wsl -d IFX-Ubuntu-24.04 -e bash -lc "bash ~/emsoft_gui/run.sh %*"

pause