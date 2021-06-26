load,
output-file ComplexArrays.out,
compare-to ComplexArrays.cmp,
output-list RAM[20000]%D1.6.1 RAM[20001]%D1.6.1 RAM[20002]%D1.6.1 RAM[20003]%D1.6.1 RAM[20004]%D1.6.1;

repeat 1000000 {
  vmstep;
}

output;
