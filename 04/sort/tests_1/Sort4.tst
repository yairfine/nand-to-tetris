load Sort.asm,
output-file Sort4.out,
compare-to Sort4.cmp,
output-list RAM[3000]%D1.6.1 RAM[3001]%D1.6.1 RAM[3002]%D1.6.1 RAM[3003]%D1.6.1 RAM[3004]%D1.6.1 RAM[3005]%D1.6.1 RAM[3006]%D1.6.1 RAM[3007]%D1.6.1 RAM[3008]%D1.6.1 RAM[3009]%D1.6.1 RAM[3010]%D1.6.1 RAM[3011]%D1.6.1 RAM[3012]%D1.6.1 RAM[3013]%D1.6.1 RAM[3014]%D1.6.1 RAM[3015]%D1.6.1 RAM[3016]%D1.6.1;



set RAM[3000] 0,
set RAM[14] 3000,
set RAM[15] 1;
repeat 30000 {
  ticktock;
}
output;

set PC 0,
set RAM[3010] -89,
set RAM[3011] 5,
set RAM[3012] 16,
set RAM[3013] 15,
set RAM[14] 3010,
set RAM[15] 4;
repeat 30000 {
  ticktock;
}
output;




set PC 0,
set RAM[3000] -2,
set RAM[3001] 4,
set RAM[3002] 1,
set RAM[3003] 59,
set RAM[3004] 65,
set RAM[3005] -100,
set RAM[3006] 70,
set RAM[3007] 0,
set RAM[3008] 71,
set RAM[3009] 4,
set RAM[3010] 10,
set RAM[3011] 4,
set RAM[3012] 72,
set RAM[3013] 0,
set RAM[3014] 34,
set RAM[3015] -5000,
set RAM[3016] 5000,
set RAM[14] 3000,
set RAM[15] 17;
repeat 30000 {
  ticktock;
}
output;


