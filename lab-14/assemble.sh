#/usr/bin/env bash

wine ./nasm/nasm.exe -fobj "code.asm" -l "code.lst" -I "./nasm/"
wine ./nasm/ALINK.EXE -oPE -subsys console -entry start "code.obj"

