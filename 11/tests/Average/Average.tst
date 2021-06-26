load,
output-file Average.out,
compare-to Average.cmp,
output-list RAM[20000]%D1.6.1;

repeat 1000000 {
  vmstep;
}

output;
