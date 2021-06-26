// Must be less than 30,000 for 20 elements. Takes us ~3,700 ticktocks.

load Sort.asm,
output-file SortOrdered.out,
compare-to SortOrdered.cmp,
output-list 
  RAM[3000]%D2.6.2 RAM[3001]%D2.6.2 RAM[3002]%D2.6.2 RAM[3003]%D2.6.2
  RAM[3004]%D2.6.2 RAM[3005]%D2.6.2 RAM[3006]%D2.6.2 RAM[3007]%D2.6.2 
  RAM[3008]%D2.6.2 RAM[3009]%D2.6.2    RAM[3011]%D2.6.2
  RAM[3012]%D2.6.2   RAM[3014]%D2.6.2 RAM[3015]%D2.6.2
  RAM[3016]%D2.6.2 RAM[3017]%D2.6.2 RAM[3018]%D2.6.2 RAM[3019]%D2.6.2
  RAM[14]%D2.6.2 RAM[15]%D2.6.2;

echo "If you haven't selected 'No animation' you'll be waiting here for a while ;)";

set RAM[14] 3000,
set RAM[15] 20,
set RAM[3000] 1,
set RAM[3000] 30,
set RAM[3001] 29,
set RAM[3002] 28,
set RAM[3003] 27,
set RAM[3004] 26,
set RAM[3005] 25,
set RAM[3006] 24,
set RAM[3007] 23,
set RAM[3008] 22,
set RAM[3009] 21,
set RAM[3010] 20,
set RAM[3011] 19,
set RAM[3012] 18,
set RAM[3013] 17,
set RAM[3014] 16,
set RAM[3015] 15,
set RAM[3016] 14,
set RAM[3017] 13,
set RAM[3018] 12,
set RAM[3019] 11;

repeat 30000 {
  ticktock;
}

output;
