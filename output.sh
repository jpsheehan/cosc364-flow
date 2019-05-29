#!/bin/bash
for y in 3 4 5 6 7 8
do
   python3 src 9 $y 9
   start=$(date +%s%N)
   cplex -c "read problem_9_${y}_9.lp" "optimize" "display solution variables -" > tests/$y.txt
   end=$(date +%s%N)
   duration=$(expr $end - $start)
   duration=$(expr $duration / 1000000)
   echo "elapsed time: $duration us" >> tests/$y.txt
done
