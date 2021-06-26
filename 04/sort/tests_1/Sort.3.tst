load Sort2.asm,
output-file Sort3.out,
RAM[5]%D1.6.1 RAM[6]%D1.6.1 RAM[7]%D1.6.1 RAM[8]%D1.6.1 RAM[9]%D1.6.1 RAM[10]%D1.6.1 RAM[11]%D1.6.1 RAM[12]%D1.6.1 RAM[13]%D1.6.1 RAM[14]%D1.6.1 RAM[15]%D1.6.1;


set RAM[5] 10,
set RAM[6] 9,
set RAM[7] 8,
set RAM[8] 7,
set RAM[9] 6,
set RAM[10] 5,
set RAM[11] 4,
set RAM[12] 3,
set RAM[13] 2,
set RAM[14] 5,
set RAM[15] 9;
repeat 34000 {
  ticktock;
}
output;
