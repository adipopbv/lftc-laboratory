%{
#include <stdio.h>
#include <string.h>
#include "parser.tab.h"
int lineNumber = 1;
%}

identifier [a-zA-Z]{1,250}
constant   0|([1-9][0-9]{0,8})

%option noyywrap

%%
"{"                   { return(LEFT_CB); }
"}"                   { return(RIGHT_CB); }
"int"                 { return(INT_TYPE); }
"+"                   { return(PLUS); }
"-"                   { return(MINUS); }
"*"                   { return(MUL); }
"/"                   { return(DIV); }
"="                   { return(EQ); }
"cin >>"              { return(IN); }
"cout <<"             { return(OUT); } 
";"                   { return(SEMICOLON); }
{identifier}          { strcpy(yylval.str, yytext); return(ID); }
{constant}            { strcpy(yylval.str, yytext); return(CT); }
\n                    { lineNumber++; }
[ \t\s\r]+	          { }
.      		          { return(OTHER); }

%%
