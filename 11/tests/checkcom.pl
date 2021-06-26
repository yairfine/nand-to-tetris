#!/usr/bin/perl -w   
#use strict;

$SIG{ALRM} = sub {
  die;
};

alarm 30;

die "No argument was given.\n" unless @ARGV;

$com=join(' ',@ARGV);

`$com`


