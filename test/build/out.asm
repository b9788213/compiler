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
push rax
pop rdi
call print
push 0
call input
add rsp, 8
push rax
pop rdi
push 0
call atoi
add rsp, 8
mov [rbp -8], rax 
mov rax, label_2
push rax
pop rdi
push 0
call print
add rsp, 8
push 0
call input
add rsp, 8
push rax
pop rdi
push 0
call atoi
add rsp, 8
mov [rbp -16], rax 
mov rax, [rbp -16]
push rax
mov rax, [rbp -8]
pop rbx
add rax, rbx
push rax
pop rdi
push 0
call itoa
add rsp, 8
push rax
pop rdi
push 0
call print
add rsp, 8
xor rax, rax
.exit:
leave
ret
print:
push rbp
mov rbp, rsp
sub rsp, 16
mov [rbp -8], rdi
push rdi
call len
mov rdx, rax
pop rsi
mov rax, 1
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
mov rdi, 4096
call alloc
mov rsi, rax
xor rax, rax
xor rdi, rdi
mov rdx, 4096
syscall
mov byte [rsi + rax - 1], 0
mov rax, rsi
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
alloc:
push rbp
mov rbp, rsp
sub rsp, 16
mov [rbp -8], rdi
mov rsi, rdi
mov rax, 9
xor rdi, rdi
mov rdx, 0x3
mov r10, 0x22
mov r8, -1
mov r9, 0
syscall
jmp .exit
xor rax, rax
.exit:
leave
ret
atoi:
push rbp
mov rbp, rsp
sub rsp, 16
mov [rbp -8], rdi
xor rax, rax
xor rcx, rcx
movzx rdx, byte [rdi]
cmp dl, '-'
je .prepare_negative
cmp dl, '+'
jne .atoi_loop
inc rcx
jmp .atoi_loop
.prepare_negative:
inc rcx
.neg_loop:
movzx rdx, byte [rdi + rcx]
test dl, dl
jz .apply_neg
cmp dl, '0'
jl .apply_neg
cmp dl, '9'
jg .apply_neg
sub dl, '0'
imul rax, 10
add rax, rdx
inc rcx
jmp .neg_loop
.apply_neg:
neg rax
jmp .exit
.atoi_loop:
movzx rdx, byte [rdi + rcx]
test dl, dl
jz .exit
cmp dl, '0'
jl .exit
cmp dl, '9'
jg .exit
sub dl, '0'
imul rax, 10
add rax, rdx
inc rcx
jmp .atoi_loop
xor rax, rax
.exit:
leave
ret
itoa:
push rbp
mov rbp, rsp
sub rsp, 0
mov rdi, 32
call alloc
mov rsi, rax
add rsi, 31
mov byte [rsi], 0
mov rax, [rbp-8]
mov r8, 0
test rax, rax
jge .start_div
mov r8, 1
neg rax
.start_div:
mov rbx, 10
.loop:
xor rdx, rdx
div rbx
add dl, 48
dec rsi
mov [rsi], dl
test rax, rax
jnz .loop
cmp r8, 1
jne .exit_final
dec rsi
mov byte [rsi], 45
.exit_final:
mov rax, rsi
jmp .exit
xor rax, rax
.exit:
leave
ret
section .data
section .rodata
label_1: db 98, 105, 114, 32, 197, 159, 101, 121, 32, 103, 105, 114, 105, 110, 58, 32, 0
label_2: db 98, 105, 114, 32, 197, 159, 101, 121, 32, 103, 105, 114, 105, 110, 58, 32, 0