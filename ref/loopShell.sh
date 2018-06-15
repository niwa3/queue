#!/bin/bash
for i in `seq $1`
do
  echo $i
  python3 $2
done
