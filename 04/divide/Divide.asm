// D13 - Dividend
// D14 - Divisor
// if D == 0 jump to END
@R14
D=M

@END
D; JEQ

@R15
M=0

@remainder
M=0

@16384
D=A
// D=D<<

@mask
M=D

(LOOP)
    @remainder
    M=M<<

    // Set LSB of the remainder to the i'th bit of the dividend.
    @R13
    D=M

    @mask
    D=D&M

    // R[0] = R13[i]
    @AFTER_REMEINDER_LSB
    D; JEQ

    @remainder
    M=M+1

(AFTER_REMEINDER_LSB)
    
    // Compute R - D
    @R14
    D=M

    @remainder
    D=M-D

    // If R < D then continue to next iteration.
    @AFTER_SUB
    D; JLT

    // R = R - D
    @remainder
    M=D

    @R15
    D=M

    @mask
    D=D|M

    @R15
    M=D

(AFTER_SUB)
    @mask
    M=M>>
    D=M

    @LOOP
    D; JNE