// Must be less than 30,000 for 20 elements. Takes us ~5,400 ticktocks.

load Sort.asm,
output-file SortUnordered.out,
compare-to SortUnordered.cmp,
output-list 
  RAM[3000]%D2.6.2 RAM[3001]%D2.6.2 RAM[3002]%D2.6.2 RAM[3003]%D2.6.2
  RAM[3004]%D2.6.2   RAM[3006]%D2.6.2 RAM[3007]%D2.6.2
  RAM[3008]%D2.6.2 RAM[3009]%D2.6.2    RAM[3011]%D2.6.2
  RAM[3012]%D2.6.2 RAM[3013]%D2.6.2 RAM[3014]%D2.6.2 RAM[3015]%D2.6.2
  RAM[3016]%D2.6.2 RAM[3017]%D2.6.2 RAM[3018]%D2.6.2 RAM[3019]%D2.6.2
  RAM[14]%D2.6.2 RAM[15]%D2.6.2;

echo "If you haven't selected 'No animation' you'll be waiting here for a while ;)";

set RAM[14] 3000,
set RAM[15] 20,
set RAM[3000] 55,
set RAM[3001] -3,
set RAM[3002] 3,
set RAM[3003] -16383,
set RAM[3004] 232,
set RAM[3005] 16383,
set RAM[3006] 49,
set RAM[3007] -39,
set RAM[3008] 383,
set RAM[3009] 1,
set RAM[3010] 3840,
set RAM[3011] -16383,
set RAM[3012] 938,
set RAM[3013] 220,
set RAM[3014] 2,
set RAM[3015] 93,
set RAM[3016] 16383,
set RAM[3017] 298,
set RAM[3018] -1,
set RAM[3019] 0;

repeat 30000 {
  ticktock;
}

output;
