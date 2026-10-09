ASM = nasm
ASMFLAGS = -f elf64
LD = ld

all: average

average: main.o
	$(LD) -o average main.o

main.o: main.asm
	$(ASM) $(ASMFLAGS) -o main.o main.asm

run: average
	./average data.txt

clean:
	rm -f main.o average

.PHONY: all run clean
