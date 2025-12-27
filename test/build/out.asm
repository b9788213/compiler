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
sub rsp, 0
mov rax, 3
push rax
mov rax, 2
pop rbx
imul rax, rbx
push rax
mov rax, 1
pop rbx
add rax, rbx
jmp .exit
.exit:
leave
ret
section .data
section .rodata