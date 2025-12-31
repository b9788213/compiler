bits 64
default rel
section .text
global main
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
sub rsp, 16
mov [rbp -8], rdi
mov rdi, 4096
call alloc 
mov r8, rax
mov r12, rax
mov rax, [rbp-8]
mov rbx, 10
xor rcx, rcx
cmp rax, 0
jge .is_zero
neg rax
mov byte [r8], '-'
inc r8
.is_zero:
test rax, rax
jnz .loop
mov rdx, '0'
push rdx
inc rcx
jmp .write_to_buffer
.loop:
test rax, rax
jz .write_to_buffer
cqo
idiv rbx
add rdx, '0'
push rdx
inc rcx
jmp .loop
.write_to_buffer:
test rcx, rcx
jz .done
pop rdx
mov [r8], dl
inc r8
dec rcx
jmp .write_to_buffer
.done:
mov byte [r8], 0
mov rax, r12
jmp .exit
xor rax, rax
.exit:
leave
ret
factorial:
push rbp
mov rbp, rsp
sub rsp, 16
mov [rbp -8], rdi
.label_1:
mov rax, [rbp -8]
test rax, rax
jz .label_2
mov rax, 1
push rax
mov rax, [rbp -8]
pop rbx
sub rax, rbx
push rax
pop rdi
call factorial
push rax
mov rax, [rbp -8]
pop rbx
imul rax, rbx
jmp .exit
jmp .label_3
.label_2:
.label_3:
mov rax, 1
jmp .exit
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
mov rsi, [rbp-8]
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
main:
push rbp
mov rbp, rsp
sub rsp, 0
call input
push rax
pop rdi
call atoi
push rax
pop rdi
call factorial
push rax
pop rdi
call itoa
push rax
pop rdi
call print
lea rax, label_4
push rax
pop rdi
call print
xor rax, rax
.exit:
mov rdi, rax
mov rax, 60
syscall
section .data
section .rodata
label_4: db 10, 0
section .note.GNU-stack noalloc noexec nowrite progbits