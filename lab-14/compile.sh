#!/usr/bin/env bash

flex lexer.l
bison -dv parser.y
gcc -o compiler lex.yy.c parser.tab.c
./compiler code.in

