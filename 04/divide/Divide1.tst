// This file is part of www.nand2tetris.org

load Divide.asm,
output-file Divide1.out,
compare-to Divide1.cmp,
output-list RAM[15]%D2.6.2;

set PC 0,
set RAM[13] 30000,
set RAM[14] 4,
repeat 7000 {
  ticktock;
}

output;
