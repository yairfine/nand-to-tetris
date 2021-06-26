// R14 - Starting address.
// R15 - The length of the array.

@R15
D=M

@END
D;JEQ

D=D-1
@END
D;JEQ

// i = (Starting Address) + Length - 1
@R15
D=M
@i
M=D
@R14
D=M
@i
M=M+D
M=M-1

// stop_iteration = 0
@stop_iteration
M=0

(OUTER_LOOP)
    // ===== INITIALIZE OUTER LOOP ======
    // j = i
    @i
    D=M
    @j
    M=D
    
(INNER_LOOP)
    // ====== COMPUTE DIFFERANCE ======
    // D = arr[j]
    @j
    A=M
    D=M

    // M = arr[j-1]
    @j
    A=M
    A=A-1 // A is j-1

    D=M-D // arr[j-1] - arr[j]
    
    @AFTER_SWAP
    D; JGT // (if arr[j-1] > arr[j] jump to AFTER_SWAP)
    
    // ===== SWAPPING arr[j-1] and arr[j] =====
    // temp = arr[j]
    @j
    A=M
    D=M
    @temp
    M=D

    // d=arr[j-1]
    @j
    A=M
    A=A-1
    D=M

    // arr[j] = d = arr[j-1]
    @j
    A=M
    M=D
    
    // arr[j-1] = temp
    @temp
    D=M
    @j
    A=M
    A=A-1
    M=D

(AFTER_SWAP)
    @j
    M=M-1
    D=M
    @R14
    D=D-M
    @stop_iteration
    D=D-M
 
    @INNER_LOOP
    D; JNE

    @stop_iteration
    M=M+1
    D=M
    @R15
    D=D-M
    D=D+1

    @OUTER_LOOP
    D; JNE

(END)
	@END
	0;JMP