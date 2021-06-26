// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// INITIAL SETUP
// sets address=SCREEN and screenend=24575
(INIT)
@SCREEN
D=A
@address
M=D


// reads keyboard input
@KBD
D=M
@SETCOLORBLACK
D;JGT // if button pressed, color=black

// ...otherwise, color=white
@color
M=0 
@LOOP
0;JMP

(SETCOLORBLACK)
	@color
	M=-1 // sets color to black


(LOOP)
	@address
	D=M
	@24575
	D=D-A
	@INIT
	D;JGT 

	@color
	D=M
	@address
	A=M
	M=D // paints address with color
	
	@address
	M=M+1
	@LOOP
	0; JMP
