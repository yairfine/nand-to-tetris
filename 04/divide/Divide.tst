// This file is part of www.nand2tetris.org

load divide.asm,
output-file Divide.out,
compare-to Divide.cmp,
output-list RAM[15]%D2.6.2;

set RAM[13] 90,
set RAM[14] 15,

repeat 1000 {
  ticktock;
}

output;

set PC 0,
set RAM[13] 1001,
set RAM[14] 11,

repeat 1000 {
  ticktock;
}

output;

set PC 0,
set RAM[13] 1001,
set RAM[14] 13,

repeat 1000 {
  ticktock;
}

output;

set PC 0,
set RAM[13] 3125,
set RAM[14] 5,

repeat 1000 {
  ticktock;
}

output;

set PC 0,
set RAM[13] 4096,
set RAM[14] 15,

repeat 1000 {
  ticktock;
}

output;

set PC 0,
set RAM[13] 754,
set RAM[14] 4,

repeat 1000 {
  ticktock;
}

output;

set PC 0,
set RAM[13] 774,
set RAM[14] 3,

repeat 1000 {
  ticktock;
}

output;

set PC 0,
set RAM[13] 9086,
set RAM[14] 256,
repeat 1000 {
  ticktock;
}

output;

set PC 0,
set RAM[13] 8,
set RAM[14] 3,
repeat 1000 {
  ticktock;
}

output;

set PC 0,
set RAM[13] 8,
set RAM[14] 6,
repeat 1000 {
  ticktock;
}

output;


set PC 0,
set RAM[13] 8,
set RAM[14] 4,
repeat 1000 {
  ticktock;
}

output;

set PC 0,
set RAM[13] 15,
set RAM[14] 3,
repeat 1000 {
  ticktock;
}

output;

set PC 0,
set RAM[13] 15,
set RAM[14] 6,
repeat 1000 {
  ticktock;
}

output;

set PC 0,
set RAM[13] 15,
set RAM[14] 5,
repeat 1000 {
  ticktock;
}

output;