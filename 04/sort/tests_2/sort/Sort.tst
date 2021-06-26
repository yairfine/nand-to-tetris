load Sort.asm,
compare-to Sort.cmp,
output-file Sort.out,
output-list RAM[22]%D2.6.2 RAM[23]%D2.6.2 RAM[24]%D2.6.2 RAM[25]%D2.6.2 RAM[26]%D2.6.2 RAM[27]%D2.6.2 RAM[28]%D2.6.2 RAM[29]%D2.6.2 RAM[30]%D2.6.2 RAM[31]%D2.6.2 RAM[32]%D2.6.2

set RAM[14] 22,   // Set test arguments
set RAM[15] 10,
set RAM[22] 0, // cell values
set RAM[23] 3, 
set RAM[24] 6, 
set RAM[25] 9, 
set RAM[26] 1, 
set RAM[27] 4, 
set RAM[28] 7, 
set RAM[29] 10, 
set RAM[30] 2, 
set RAM[31] 5, 
set RAM[32] 8;

repeat 200 {
  ticktock;
}
set RAM[14] 22,   // Set test arguments
set RAM[15] 10,
output;

set PC 0,
set RAM[22] 0, 
set RAM[23] 1,
set RAM[24] 2,
set RAM[25] 3, 
set RAM[26] 4, 
set RAM[27] 5, 
set RAM[28] 6, 
set RAM[29] 7,
set RAM[30] 8,
set RAM[31] 9,
set RAM[32] 10;
repeat 200 {
  ticktock;
}
output;

set PC 0,
set RAM[22] 0, 
set RAM[23] 4,
set RAM[24] 8,
set RAM[25] 1, 
set RAM[26] 5, 
set RAM[27] 9, 
set RAM[28] 2, 
set RAM[29] 6, 
set RAM[30] 10, 
set RAM[31] 3, 
set RAM[32] 7;
repeat 200 {
  ticktock;
}
output;


set PC 0,

set RAM[22] 5316, 
set RAM[23] 6194, 
set RAM[24] 7072, 
set RAM[25] 7950, 
set RAM[26] 8828, 
set RAM[27] 9706, 
set RAM[28] 10584, 
set RAM[29] 11462, 
set RAM[30] 12340,
set RAM[31] 13218, 
set RAM[32] 96;

repeat 200 {
  ticktock;
}
output;

set PC 0,

set RAM[22] 5316, 
set RAM[23] -6240, 
set RAM[24] 7072, 
set RAM[25] -8000, 
set RAM[26] 8828, 
set RAM[27] -9760, 
set RAM[28] 10584, 
set RAM[29] -11520, 
set RAM[30] 12340, 
set RAM[31] -13280, 
set RAM[32] 96;

repeat 200 {
  ticktock;
}
output;


