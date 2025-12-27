bits 64
default rel
section .text
global _start
_start:
call main
mov rdi, rax
mov rax, 60
syscall
main:
push rbp
mov rbp, rsp
sub rsp, 16
mov rax, label_1
mov [rbp -8], rax 
mov rax, [rbp -8]
push rax
pop rdi
push 0
call print
mov rax, [rbp -8]
push rax
pop rdi
push 0
call print
xor rax, rax
.exit:
leave
ret
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
jmp .exit
xor rax, rax
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
xor rax, rax
.exit:
leave
ret
section .data
section .rodata
label_1: db 109, 101, 114, 104, 97, 98, 97, 32, 10, 0