all:test
test:*.asm
	nasm -felf32 test.asm -F dwarf -g -o test.o
	ld -m elf_i386 test.o -o test
	rm -f test.o
.PHONY:clean
clean:
	rm -f test