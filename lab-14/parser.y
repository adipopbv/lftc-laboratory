%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// lexer
int yylex();
// error handling
void yyerror(char *s);

// input file from flex
extern FILE *yyin;
// line number from flex
extern int lineNumber;

// asm data segment
char DS[4096];
void addToDS(char *s);
// asm code segment
char CS[4096];
void addToCS(char *s);

void writeToFile();
%}

%union{
	char str[250];
}

%token LEFT_CB RIGHT_CB INT_TYPE PLUS MINUS MUL DIV EQ IN OUT SEMICOLON OTHER
%token <str> ID
%token <str> CT

%type <str> variable
%type <str> constant
%type <str> value

%%
program: header declarations instructions footer
	   ;

header: LEFT_CB
	  ;

declarations: /* empty */
			| declaration SEMICOLON declarations
			;

declaration: type variable
{
	char *tmp = (char*)malloc(sizeof(char)*250);
	sprintf(tmp, "%s dd 0\n", $2);
	addToDS(tmp);
	free(tmp);
}
		   ;

type: INT_TYPE
	;

instructions: /* empty */
			| instruction SEMICOLON instructions
			;

instruction: assignment
		   | input
		   | output
		   ;

assignment: variable EQ expression
{
	char *tmp = (char*)malloc(sizeof(char)*250);
	sprintf(tmp, "mov [%s], ebx\n", $1);
	addToCS(tmp);
	free(tmp);
}
		  ;

expression: value
{
	char *tmp = (char*)malloc(sizeof(char)*250);
	sprintf(tmp, "mov ebx, %s\n", $1);
	addToCS(tmp);
	free(tmp);
}
		  | value PLUS expression
{
	char *tmp = (char*)malloc(sizeof(char)*250);
	sprintf(tmp, "add ebx, %s\n", $1);
	addToCS(tmp);
	free(tmp);
}
		  | value MINUS expression
{
	char *tmp = (char*)malloc(sizeof(char)*250);
	sprintf(tmp, "sub ebx, %s\n", $1);
	addToCS(tmp);
	free(tmp);
}
		  | value MUL expression
{
	char *tmp = (char*)malloc(sizeof(char)*250);
	sprintf(tmp, "mov eax, %s\n", $1);
	addToCS(tmp);
	strcpy(tmp, "mul ebx\nmov ebx, eax\n");
	addToCS(tmp);
	free(tmp);
}
		  | value DIV expression
{
	char *tmp = (char*)malloc(sizeof(char)*250);
	sprintf(tmp, "mov eax, %s\n", $1);
	addToCS(tmp);
	strcpy(tmp, "mov edx, 0\ndiv ebx\nmov ebx, eax\n");
	addToCS(tmp);
	free(tmp);
}
		  ;

value: variable
{
	strcpy($$, "[");
	strcat($$, $1);
	strcat($$, "]");
}
	 | constant
{
	strcpy($$, $1);
}
	 ;

constant: CT
{
	strcpy($$, $1);
}
		;

input: IN variable
{
	char *tmp = (char*)malloc(sizeof(char)*250);
	sprintf(tmp, "push dword %s\npush dword int_in_format\ncall [scanf]\nadd esp, 4*2\n" ,$2);
	addToCS(tmp);
}
	 ;

output: OUT variable
{
	char *tmp = (char *)malloc(sizeof(char)*250);
	sprintf(tmp, "push dword [%s]\npush dword int_out_format\ncall [printf]\nadd esp, 4*2\n", $2);
	addToCS(tmp);
}
	  ;

variable: ID
{
	strcpy($$, $1);
}
		;

footer: RIGHT_CB
{
	printf("Program syntax is ok\n");
	return 0;
}
	  ;

%%

void addToDS(char *s){
    strcat(DS, s);
}

void addToCS(char *s){
    strcat(CS, s);
}

void yyerror(char *s)
{
	printf("%s on line %d\n", s, lineNumber);
	exit(0);
}

int main(int argc, char** argv)
{
    memset(DS, 0, 4096);
    memset(CS, 0 ,4096);
    if (argc == 2) {
        yyin = fopen(argv[1], "r");
        yyparse();
		writeToFile();
    }
    return 0;
}

void writeToFile() {
	char *header = (char *) malloc(sizeof(char)*3000);
	char *dataSegment = (char *) malloc(sizeof(char)*3000);
	char *codeSegment = (char *) malloc(sizeof(char)*3000);
	char *footer = (char *) malloc(sizeof(char)*3000);
	
	strcpy(header, "bits 32\nglobal start\nextern exit, scanf, printf\nimport exit msvcrt.dll\nimport scanf msvcrt.dll\nimport printf msvcrt.dll\n");

	strcpy(dataSegment, "\nsegment data use32 class=data\nint_in_format db \"%d\", 0\nint_out_format db \"%d \", 0\n");
	strcat(dataSegment, DS);

	strcpy(codeSegment, "\nsegment code use32 class=code\nstart:\n");
	strcat(codeSegment ,CS);

	strcpy(footer, "\npush dword 0\ncall [exit]\n");

	FILE *f = fopen("code.asm", "w");
	if(f == NULL) {
		perror("Failed to write to file");
		exit(1);
	}

	fwrite(header, strlen(header), 1, f);
	fwrite(dataSegment, strlen(dataSegment), 1, f);
	fwrite(codeSegment, strlen(codeSegment), 1, f);
	fwrite(footer, strlen(header), 1, f);

	fclose(f);
	free(header);
	free(dataSegment);
	free(codeSegment);
	free(footer);
}

