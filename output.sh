#!/bin/bash
for y in 3 4 5 6 7 8
do
   python3 src/lp_gen.py 9 $y 9 lp_files
   start=$(date +%s%N)
   cplex -c "read lp_files/problem_9_${y}_9.lp" "optimize" "display solution variables -" > cplex_logs/$y.txt
   end=$(date +%s%N)
   duration=$(expr $end - $start)
   duration=$(expr $duration / 1000000)
   echo -e "\nelapsed_time: $duration ms" >> cplex_logs/$y.txt
done

python3 src/lp_csv.py cplex_logs lp_files/cplex_data.csv
python3 src/lp_graph.py lp_files/cplex_data.csv graphs