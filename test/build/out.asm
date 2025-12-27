bits 64
default rel
section .text
global _start
_start:
call main
mov rdi, rax
mov rax, 60
syscall
print:
push rbp
mov rbp, rsp
sub rsp, 16
mov [rbp -8], rdi
call len
mov rdx, rax
mov rax, 1
mov rsi, rdi
mov rdi, 1
syscall
.exit:
leave
ret
len:
push rbp
mov rbp, rsp
sub rsp, 16
mov [rbp -8], rdi
xor rax, rax
.loop:
cmp byte [rdi + rax], 0
je .exit
inc rax
jmp .loop
.exit:
leave
ret
main:
push rbp
mov rbp, rsp
sub rsp, 0
mov rax, label_1
push rax
pop rdi
push 0
call print
xor rax, rax
.exit:
leave
ret
section .data
section .rodata
label_1: db 109, 101, 114, 104, 97, 98, 97, 0