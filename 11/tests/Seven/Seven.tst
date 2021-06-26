load,
output-file Seven.out,
compare-to Seven.cmp,
output-list RAM[20000]%D1.6.1;

repeat 1000000 {
  vmstep;
}

output;
