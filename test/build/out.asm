bits 64
default rel
section .text
global main
main:
push rbp
mov rbp, rsp
sub rsp, 32
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
mov rax, label_3
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
mov [rbp -24], rax 
label_4:
mov rax, 1
push rax
mov rax, [rbp -24]
pop rbx
cmp rax, rbx
sete al
movzx rax, al
test rax, rax
jz label_5
mov rax, label_10
push rax
pop rdi
push 0
call print
add rsp, 8
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
jmp label_9
label_5:
mov rax, 2
push rax
mov rax, [rbp -24]
pop rbx
cmp rax, rbx
sete al
movzx rax, al
test rax, rax
jz label_6
mov rax, label_11
push rax
pop rdi
push 0
call print
add rsp, 8
mov rax, [rbp -16]
push rax
mov rax, [rbp -8]
pop rbx
sub rax, rbx
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
jmp label_9
label_6:
mov rax, 3
push rax
mov rax, [rbp -24]
pop rbx
cmp rax, rbx
sete al
movzx rax, al
test rax, rax
jz label_7
mov rax, label_12
push rax
pop rdi
push 0
call print
add rsp, 8
mov rax, [rbp -16]
push rax
mov rax, [rbp -8]
pop rbx
imul rax, rbx
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
jmp label_9
label_7:
mov rax, 4
push rax
mov rax, [rbp -24]
pop rbx
cmp rax, rbx
sete al
movzx rax, al
test rax, rax
jz label_8
mov rax, label_13
push rax
pop rdi
push 0
call print
add rsp, 8
mov rax, [rbp -16]
push rax
mov rax, [rbp -8]
pop rbx
cqo
idiv rbx
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
jmp label_9
label_8:
mov rax, label_14
push rax
pop rdi
push 0
call print
add rsp, 8
mov rax, [rbp -16]
push rax
mov rax, [rbp -8]
pop rbx
cqo
idiv rbx
mov rax, rdx
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
label_9:
mov rax, label_15
push rax
pop rdi
push 0
call print
add rsp, 8
xor rax, rax
.exit:
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
section .data
section .rodata
label_1: db 98, 105, 114, 32, 115, 97, 121, 196, 177, 32, 103, 105, 114, 105, 110, 58, 32, 0
label_2: db 98, 105, 114, 32, 115, 97, 121, 196, 177, 32, 103, 105, 114, 105, 110, 58, 32, 0
label_3: db 98, 105, 114, 32, 111, 112, 101, 114, 97, 116, 195, 182, 114, 32, 103, 105, 114, 105, 110, 58, 32, 0
label_10: db 116, 111, 112, 108, 97, 109, 196, 177, 58, 32, 0
label_11: db 102, 97, 114, 107, 196, 177, 58, 32, 0
label_12: db 195, 167, 97, 114, 112, 196, 177, 109, 196, 177, 58, 32, 0
label_13: db 98, 195, 182, 108, 195, 188, 109, 195, 188, 58, 32, 0
label_14: db 109, 111, 100, 117, 58, 32, 0
label_15: db 10, 0
section .note.GNU-stack noalloc noexec nowrite progbits