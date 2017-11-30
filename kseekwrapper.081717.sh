#!/bin/bash

for myread in `cat reads_kseek.txt`; do
  qsub kseek.081717.sh $myread
done

