//dosen't use R0..R4
load Sort.asm,
output-file Sort11.out,
compare-to Sort11.cmp,
output-list RAM[5]%D1.6.1 RAM[6]%D1.6.1 RAM[7]%D1.6.1 RAM[8]%D1.6.1 RAM[9]%D1.6.1 RAM[10]%D1.6.1 RAM[11]%D1.6.1 RAM[12]%D1.6.1 RAM[13]%D1.6.1;



set RAM[11] 0,
set RAM[14] 11,
set RAM[15] 1;
repeat 30000 {
  ticktock;
}
output;

set PC 0,
set RAM[10] -89,
set RAM[11] 5,
set RAM[12] 16,
set RAM[13] 15,
set RAM[14] 10,
set RAM[15] 4;
repeat 30000 {
  ticktock;
}
output;




set PC 0,
set RAM[5] -100,
set RAM[6] 70,
set RAM[7] 0,
set RAM[8] 71,
set RAM[9] 4,
set RAM[10] 10,
set RAM[11] 4,
set RAM[12] 72,
set RAM[13] 0,
set RAM[14] 5,
set RAM[15] 9;
repeat 30000 {
  ticktock;
}
output;


