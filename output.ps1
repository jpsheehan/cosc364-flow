For ($i=3; $i -le 8; $i++) {
    python src 9 $i 9
    $perf = Measure-Command -Expression {$data = cplex -c ("read problem_9_" + $i + "_9.lp") "optimize" "display solution variables -"}
    $ms = $perf.TotalMilliseconds
    [System.IO.File]::WriteAllLines("cplex_logs/$i.txt", $data + "`nelapsed_time: $ms ms")
}

python src/lp_csv.py cplex_logs cplex_data.csv
python src/lp_graph.py cplex_data.csv graphs