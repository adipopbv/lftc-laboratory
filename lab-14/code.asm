bits 32
global start
extern exit, scanf, printf
import exit msvcrt.dll
import scanf msvcrt.dll
import printf msvcrt.dll

segment data use32 class=data
int_in_format db "%d", 0
int_out_format db "%d ", 0
a dd 0
b dd 0
c dd 0

segment code use32 class=code
start:
push dword a
push dword int_in_format
call [scanf]
add esp, 4*2
push dword b
push dword int_in_format
call [scanf]
add esp, 4*2
mov ebx, 2
mov eax, 8
mov edx, 0
div ebx
mov ebx, eax
mov [a], ebx
push dword [a]
push dword int_out_format
call [printf]
add esp, 4*2
mov ebx, 5
mov eax, 100
mov edx, 0
div ebx
mov ebx, eax
mov [b], ebx
push dword [b]
push dword int_out_format
call [printf]
add esp, 4*2
mov ebx, [a]
mov eax, [b]
mul ebx
mov ebx, eax
add ebx, 1
mov [c], ebx
push dword [c]
push dword int_out_format
call [printf]
add esp, 4*2

push dword 0
call [exit]
                                                                                              