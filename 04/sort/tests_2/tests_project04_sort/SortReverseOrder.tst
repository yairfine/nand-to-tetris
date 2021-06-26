// Must be less than 30,000 for 20 elements. Takes us ~6,800 ticktocks.

load Sort.asm;
output-file SortReverseOrder.out,
compare-to SortReverseOrder.cmp,
output-list 
  RAM[3000]%D2.6.2 RAM[3001]%D2.6.2 RAM[3002]%D2.6.2 RAM[3003]%D2.6.2
  RAM[3004]%D2.6.2 RAM[3005]%D2.6.2   RAM[3007]%D2.6.2 
  RAM[3008]%D2.6.2 RAM[3009]%D2.6.2 RAM[3010]%D2.6.2 RAM[3011]%D2.6.2
  RAM[3012]%D2.6.2 RAM[3013]%D2.6.2   RAM[3015]%D2.6.2
  RAM[3016]%D2.6.2 RAM[3017]%D2.6.2 RAM[3018]%D2.6.2 RAM[3019]%D2.6.2
  RAM[14]%D2.6.2 RAM[15]%D2.6.2;

echo "If you haven't selected 'No animation' you'll be waiting here for a while ;)";

set RAM[14] 3000,
set RAM[15] 20,
set RAM[3000] 1,
set RAM[3001] 2,
set RAM[3002] 3,
set RAM[3003] 4,
set RAM[3004] 5,
set RAM[3005] 6,
set RAM[3006] 7,
set RAM[3007] 8,
set RAM[3008] 9,
set RAM[3009] 10,
set RAM[3010] 11,
set RAM[3011] 12,
set RAM[3012] 13,
set RAM[3013] 14,
set RAM[3014] 15,
set RAM[3015] 16,
set RAM[3016] 17,
set RAM[3017] 18,
set RAM[3018] 19,
set RAM[3019] 20;

repeat 30000 {
  ticktock;
}

output;
