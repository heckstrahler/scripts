#!/bin/bash

indir=$2
outdir=$1


for file in "$indir"*
do
  var="${file%.*}"
  var=${var##*/}
  tempFolder=.convertTemp$var
  echo $tempFolder

  7z x "$file" -o"$tempFolder"
  7z a -t7z -m0=lzma2 -mx=9 -mfb=64 -md=64m -ms=on "$outdir$var.7z" -r ./"$tempFolder"/* 
  rm -r "$tempFolder"

done
