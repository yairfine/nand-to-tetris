// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Initialize variables
@mask
M=1

@R0
D=M

@shifted
M=D

@R2
M=0

// Start multiplication loop
(LOOP)
    @R1
    D=M

    @mask
    D=D&M

    @AFTER_ADD
    D; JEQ

    @shifted
    D=M
    @R2
    M=M+D

(AFTER_ADD)
    @shifted
    M=M<<

    @mask
    M=M<<
    D=M

    @LOOP
    D; JNE
