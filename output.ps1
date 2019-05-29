For ($i=3; $i -le 8; $i++) {
    python src/lp_gen.py 9 $i 9 lp_files
    $perf = Measure-Command -Expression {$data = cplex -c ("read lp_files/problem_9_" + $i + "_9.lp") "optimize" "display solution variables -"}
    $ms = $perf.TotalMilliseconds
    [System.IO.File]::WriteAllLines("cplex_logs/$i.txt", $data + "`nelapsed_time: $ms ms")
}

python src/lp_csv.py cplex_logs lp_files/cplex_data.csv
python src/lp_graph.py lp_files/cplex_data.csv graphs