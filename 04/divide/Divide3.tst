load Divide.asm,
output-file Divide3.out,
compare-to Divide3.cmp,
output-list RAM[15]%D2.6.2;

set PC 0,
set RAM[13] 15000,
set RAM[14] 4,
repeat 3000 {
  ticktock;
}

output;
