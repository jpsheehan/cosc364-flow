For ($i=3; $i -le 8; $i++) {
    python src 9 $i 9
    $perf = Measure-Command -Expression {$data = cplex -c ("read problem_9_" + $i + "_9.lp") "optimize" "display solution variables -"}
    $ms = $perf.TotalMilliseconds
    [System.IO.File]::WriteAllLines("tests/$i.txt", $data + "`nelapsed_time: $ms ms")
}

python tests/process_data.py tests cplex_data.csv
python src/lp_csv_plot.py cplex_data.csv graphs