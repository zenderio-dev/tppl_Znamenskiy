default rel

%define SYS_READ    0
%define SYS_WRITE   1
%define SYS_OPEN    2
%define SYS_CLOSE   3
%define SYS_EXIT    60

%define BUF_SIZE    65536

section .data
    sep         db ": "
    sep_len     equ $ - sep
    bad_msg     db "файл испорчен", 10
    bad_len     equ $ - bad_msg
    newline     db 10

section .bss
    buf         resb BUF_SIZE
    numbuf      resb 32

section .text
global _start

_start:
    cmp qword [rsp], 2
    jl .exit
    mov r12, [rsp + 16]             ; r12 = argv[1] - имя файла

    ; выводим "<имя_файла>: "
    mov rdi, r12
    call strlen
    mov rsi, r12
    mov rdx, rax
    call write_out
    lea rsi, [sep]
    mov edx, sep_len
    call write_out

    ; открываем и читаем файл
    mov rdi, r12
    xor esi, esi                    ; O_RDONLY
    mov eax, SYS_OPEN
    syscall
    test rax, rax
    js .bad                         ; файл не найден
    mov rbx, rax                    ; rbx = дескриптор

    mov rdi, rbx
    lea rsi, [buf]
    mov edx, BUF_SIZE
    mov eax, SYS_READ
    syscall
    mov r8, rax                     ; r8 = сколько байт прочитано

    mov rdi, rbx
    mov eax, SYS_CLOSE
    syscall

    test r8, r8
    js .bad                         ; ошибка чтения
    lea rsi, [buf]                  ; rsi = текущая позиция
    add r8, rsi                     ; r8 = конец данных

    ; первая строка
    call parse_line
    jc .bad
    mov r14, rax                    ; r14 = сумма x
    mov r13, rcx                    ; r13 = количество x

    ; вторая строка
    call parse_line
    jc .bad
    cmp rcx, r13
    jne .bad                        ; разное количество чисел
    sub r14, rax                    ; r14 = сумма x - сумма y

    ; после второй строки могут быть только пустые строки
.tail:
    cmp rsi, r8
    jae .result
    mov dl, [rsi]
    inc rsi
    cmp dl, 10
    je .tail
    cmp dl, 13
    je .tail
    cmp dl, ' '
    je .tail
    jmp .bad

.result:
    mov rax, r14
    cqo
    idiv r13                        ; rax = сумма разностей / n
    call print_int
    lea rsi, [newline]
    mov edx, 1
    call write_out
    jmp .exit

.bad:
    lea rsi, [bad_msg]
    mov edx, bad_len
    call write_out

.exit:
    xor edi, edi
    mov eax, SYS_EXIT
    syscall


; вход:  rsi - начало строки, r8 - конец данных
; выход: rax - сумма, rcx - количество чисел,
; rsi - начало следующей строки, CF = 1 если строка испорчена
parse_line:
    xor eax, eax
    xor ecx, ecx
.number:
    call skip_spaces
    xor edx, edx                    ; rdx - текущее число
    xor r9d, r9d                    ; r9 = 1, если есть минус
    xor r10d, r10d                  ; r10 - количество цифр
    cmp rsi, r8
    jae .error
    cmp byte [rsi], '-'
    jne .digit
    mov r9d, 1
    inc rsi
.digit:
    cmp rsi, r8
    jae .end_number
    movzx r11d, byte [rsi]
    sub r11d, '0'
    cmp r11d, 9
    ja .end_number                  ; не цифра
    imul rdx, rdx, 10
    add rdx, r11
    inc rsi
    inc r10d
    jmp .digit
.end_number:
    test r10d, r10d
    jz .error                       ; ни одной цифры
    test r9d, r9d
    jz .add
    neg rdx
.add:
    add rax, rdx
    inc rcx

    call skip_spaces
    cmp rsi, r8
    jae .ok                         ; конец файла
    mov dl, [rsi]
    inc rsi
    cmp dl, ','
    je .number
    cmp dl, 10
    je .ok                          ; конец строки
.error:
    stc
    ret
.ok:
    clc
    ret


; skip_spaces - пропустить пробелы и \r
skip_spaces:
    cmp rsi, r8
    jae .done
    cmp byte [rsi], ' '
    je .skip
    cmp byte [rsi], 13
    jne .done
.skip:
    inc rsi
    jmp skip_spaces
.done:
    ret


; print_int - вывести знаковое число из rax
print_int:
    lea rsi, [numbuf + 32]
    xor r9d, r9d
    test rax, rax
    jns .convert
    mov r9d, 1
    neg rax
.convert:
    mov rcx, 10
.loop:
    xor edx, edx
    div rcx
    add dl, '0'
    dec rsi
    mov [rsi], dl
    test rax, rax
    jnz .loop

    test r9d, r9d
    jz .write
    dec rsi
    mov byte [rsi], '-'
.write:
    lea rdx, [numbuf + 32]
    sub rdx, rsi
    call write_out
    ret


strlen:
    xor eax, eax
.loop:
    cmp byte [rdi + rax], 0
    je .done
    inc rax
    jmp .loop
.done:
    ret


write_out:
    mov edi, 1
    mov eax, SYS_WRITE
    syscall
    ret
