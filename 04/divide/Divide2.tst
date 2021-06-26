// This file is part of www.nand2tetris.org

load Divide.asm,
output-file Divide2.out,
compare-to Divide2.cmp,
output-list RAM[15]%D2.6.2;


set PC 0,
set RAM[13] 8,
set RAM[14] 10,
repeat 1000 {
  ticktock;
}

output;

set PC 0,
set RAM[13] 8,
set RAM[14] 9,
repeat 1000 {
  ticktock;
}

output;


set PC 0,
set RAM[13] 15,
set RAM[14] 17,
repeat 1000 {
  ticktock;
}

output;

set PC 0,
set RAM[13] 15,
set RAM[14] 18,
repeat 1000 {
  ticktock;
}

output;

