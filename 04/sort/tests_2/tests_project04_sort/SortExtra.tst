load Sort.asm,
output-file SortExtra.out,
compare-to SortExtra.cmp,
output-list RAM[14]%D2.6.2 RAM[15]%D2.6.2
  RAM[3000]%D2.6.2 RAM[3001]%D2.6.2 RAM[3002]%D2.6.2   
  RAM[3003]%D2.6.2 RAM[3004]%D2.6.2 RAM[3005]%D2.6.2;

echo "If you haven't selected 'No animation' you'll be waiting here for a while ;)";

set RAM[14] 3001,
set RAM[15] 1,
set RAM[3000] 9191,
set RAM[3001] 0,
set RAM[3002] 9191,
set RAM[3003] 0,
set RAM[3004] 0,
set RAM[3005] -1;

repeat 10000 {
  ticktock;
}

output;


set PC 0,
set RAM[15] 0;

repeat 10000 {
  ticktock;
}

output;


set PC 0,
set RAM[15] 1,
set RAM[3000] -8181,
set RAM[3002] -8181;

repeat 10000 {
  ticktock;
}

output;


set PC 0,
set RAM[15] 0;

repeat 10000 {
  ticktock;
}

output;


set PC 0,
set RAM[15] 2;

repeat 10000 {
  ticktock;
}

output;


set PC 0,
set RAM[14] 3000,

repeat 10000 {
  ticktock;
}

output;


set PC 0,
set RAM[14] 3001,
set RAM[15] 4,
set RAM[3000] 9191,
set RAM[3001] -16383,
set RAM[3002] 16383,
set RAM[3003] 16383,
set RAM[3004] -1,
set RAM[3005] 8181;

repeat 10000 {
  ticktock;
}

output;


set PC 0,
set RAM[3002] -16383,
set RAM[3004] 16383;

repeat 10000 {
  ticktock;
}

output;


set PC 0,
set RAM[3001] -2,
set RAM[3002] -1;

repeat 10000 {
  ticktock;
}

output;


set PC 0,
set RAM[3001] -1,
set RAM[3002] -2;

repeat 10000 {
  ticktock;
}

output;


set PC 0,
set RAM[3001] 0,
set RAM[3002] -1;

repeat 10000 {
  ticktock;
}

output;


set PC 0,
set RAM[3001] -1,
set RAM[3002] 0;

repeat 10000 {
  ticktock;
}

output;
