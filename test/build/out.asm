bits 64
default rel
section .text
global main
main:
push rbp
mov rbp, rsp
sub rsp, 16
mov rax, label_1
mov [rbp -8], rax 
extern printf
mov rdi, [rbp-8]
mov al, 0
call printf
xor rax, rax
.exit:
mov rdi, rax
mov rax, 60
syscall
section .data
section .rodata
label_1: db 109, 101, 114, 104, 97, 98, 97, 10, 0
section .note.GNU-stack noalloc noexec nowrite progbits