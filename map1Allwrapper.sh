#!/bin/bash

for myindex in `cat indexes.txt`; do
  for myread in `cat reads.txt`; do
    qsub map1All.sh $myread $myindex
  done
done
