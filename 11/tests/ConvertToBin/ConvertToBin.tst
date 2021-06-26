load,
output-file ConvertToBin.out,
compare-to ConvertToBin.cmp,
output-list RAM[8001]%D1.6.1 RAM[8002]%D1.6.1 RAM[8003]%D1.6.1
RAM[8004]%D1.6.1 RAM[8005]%D1.6.1 RAM[8006]%D1.6.1 RAM[8007]%D1.6.1
RAM[8008]%D1.6.1 RAM[8009]%D1.6.1 RAM[8010]%D1.6.1 RAM[8011]%D1.6.1
RAM[8012]%D1.6.1 RAM[8013]%D1.6.1 RAM[8014]%D1.6.1 RAM[8015]%D1.6.1
RAM[8016]%D1.6.1;

repeat 1000000 {
  vmstep;
}

output;
