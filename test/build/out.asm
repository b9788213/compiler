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
mov rax, label_1
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
input:
push rbp
mov rbp, rsp
sub rsp, 0
mov rdi, 4096 ;bufsize
call alloc ;ptr rax'ta
mov rsi, rax; buffer
xor rax, rax ;write
xor rdi, rdi ;stdin
mov rdx, 4096 ;bufsize
syscall
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
alloc:
push rbp
mov rbp, rsp
sub rsp, 16
mov [rbp -8], rdi
mov rsi, rdi
mov rax, 9
xor rdi, rdi
mov rdx, 0x1 | 0x2
mov r10, 0x02 | 0x20
mov r8, -1
mov r9, 0
syscall
xor rax, rax
.exit:
leave
ret
section .data
section .rodata
label_1: db 98, 105, 114, 32, 197, 159, 101, 121, 32, 103, 105, 114, 105, 110, 32, 58, 0