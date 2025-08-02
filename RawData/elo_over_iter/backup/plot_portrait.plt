# Gnuplot Template for PDF Output

# Set terminal and output file
set terminal pdfcairo size 15cm,20cm enhanced font 'Arial,16'
set output 'output.pdf'

# Set multiplot layout: 2 rows, 3 columns
set multiplot layout 3,2


# Set grid and key (legend)
set grid
set key inside right bottom font ",11"  # Legend font size set to 14

set lmargin -1
set bmargin -1
set rmargin 2
set tmargin 3


# Set colorblind-friendly line styles
set style line 1 lc rgb '#0072B2' dt 1 lw 2 pt 0 ps 1.5
set style line 2 lc rgb '#7f7f7f' dt 1 lw 2 pt 0 ps 1.5
set style line 3 lc rgb '#ff7f0e' dt 1 lw 2 pt 0 ps 1.5
set style line 4 lc rgb '#56B4E9' dt 2 lw 2 pt 0 ps 1.5
set style line 5 lc rgb '#4D4D4D' dt 2 lw 2 pt 0 ps 1.5
set style line 6 lc rgb '#FDB863' dt 2 lw 2 pt 0 ps 1.5
set style line 7 lc rgb '#F0E442' dt 1 lw 2 pt 0 ps 1.5

# Set xrange and yrange (optional)
# set xrange [0:10]
# set yrange [0:100]

set yrange [800:2300]

# Set title and labels
set title "Connect4" font ",20"  # Title font size set to 18

set ylabel "Elo rating" font ",18" # Y-axis label font size set to 16

set xtics (500, 1000, 1500, 2000, 2500, 3000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

# Load data and plot
# For a simple line plot
plot 'Connect4/AlphaViT_Large_Test.dat' using 1:2 with lines linestyle 1 title 'AlphaViT LB', \
     'Connect4/AlphaViD_Large_Test.dat' using 1:2 with lines linestyle 2 title 'AlphaViD LB', \
     'Connect4/AlphaVDA_Large_Test.dat' using 1:2 with lines linestyle 3 title 'AlphaVDA LB', \
     'Connect4/AlphaViT_Multi_Test.dat' using 1:2 with lines linestyle 4 title 'AlphaViT Multi', \
     'Connect4/AlphaViD_Multi_Test.dat' using 1:2 with lines linestyle 5 title 'AlphaViD Multi', \
     'Connect4/AlphaVDA_Multi_Test.dat' using 1:2 with lines linestyle 6 title 'AlphaVDA Multi', \
     'Connect4/AlphaZero_Test.dat'      using 1:2 with lines linestyle 7 title 'AlphaZero'

set title "Connect4 5x4" font ",20"  # Title font size set to 18
set lmargin -0.5
set bmargin -1
set xtics (200, 400, 600, 800, 1000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

# Load data and plot
# For a simple line plot
plot 'Connect4_54/AlphaViT_Small_Test.dat' using 1:2 with lines linestyle 1  title 'AlphaViT SB', \
     'Connect4_54/AlphaViD_Small_Test.dat' using 1:2 with lines linestyle 2  title 'AlphaViD SB', \
     'Connect4_54/AlphaVDA_Small_Test.dat' using 1:2 with lines linestyle 3  title 'AlphaVDA SB', \
     'Connect4_54/AlphaZero_Test.dat'      using 1:2 with lines linestyle 7  title 'AlphaZero'

set title "Gomoku" font ",20"  # Title font size set to 18
set ylabel "Elo rating" font ",18" # Y-axis label font size set to 16

set xtics (500, 1000, 1500, 2000, 2500, 3000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14


# Load data and plot
# For a simple line plot
plot 'Gomoku/AlphaViT_Large_Test.dat' using 1:2 with lines linestyle 1  title 'AlphaViT LB', \
     'Gomoku/AlphaViD_Large_Test.dat' using 1:2 with lines linestyle 2  title 'AlphaViD LB', \
     'Gomoku/AlphaVDA_Large_Test.dat' using 1:2 with lines linestyle 3  title 'AlphaVDA LB', \
     'Gomoku/AlphaViT_Multi_Test.dat' using 1:2 with lines linestyle 4  title 'AlphaViT Multi', \
     'Gomoku/AlphaViD_Multi_Test.dat' using 1:2 with lines linestyle 5  title 'AlphaViD Multi', \
     'Gomoku/AlphaVDA_Multi_Test.dat' using 1:2 with lines linestyle 6  title 'AlphaVDA Multi', \
     'Gomoku/AlphaZero_Test.dat'      using 1:2 with lines linestyle 7  title 'AlphaZero'

set title "Gomoku 6x6" font ",20"  # Title font size set to 18
set lmargin -1
set bmargin -1
set xtics (200, 400, 600, 800, 1000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

# Load data and plot
# For a simple line plot
plot 'Gomoku66/AlphaViT_Small_Test.dat' using 1:2 with lines linestyle 1  title 'AlphaViT SB', \
     'Gomoku66/AlphaViD_Small_Test.dat' using 1:2 with lines linestyle 2  title 'AlphaViD SB', \
     'Gomoku66/AlphaVDA_Small_Test.dat' using 1:2 with lines linestyle 3  title 'AlphaVDA SB', \
     'Gomoku66/AlphaZero_Test.dat'      using 1:2 with lines linestyle 7  title 'AlphaZero'

set title "Othello" font ",20"  # Title font size set to 18
set xlabel "Iterations" font ",18"  # X-axis label font size set to 16
set ylabel "Elo rating" font ",18" # Y-axis label font size set to 16

set xtics (500, 1000, 1500, 2000, 2500, 3000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

# Load data and plot
# For a simple line plot
plot 'Othello/AlphaViT_Large_Test.dat' using 1:2 with lines linestyle 1  title 'AlphaViT LB', \
     'Othello/AlphaViD_Large_Test.dat' using 1:2 with lines linestyle 2  title 'AlphaViD LB', \
     'Othello/AlphaVDA_Large_Test.dat' using 1:2 with lines linestyle 3  title 'AlphaVDA LB', \
     'Othello/AlphaViT_Multi_Test.dat' using 1:2 with lines linestyle 4  title 'AlphaViT Multi', \
     'Othello/AlphaViD_Multi_Test.dat' using 1:2 with lines linestyle 5  title 'AlphaViD Multi', \
     'Othello/AlphaVDA_Multi_Test.dat' using 1:2 with lines linestyle 6  title 'AlphaVDA Multi', \
     'Othello/AlphaZero_Test.dat'      using 1:2 with lines linestyle 7  title 'AlphaZero'

set title "Othello 6x6" font ",20"  # Title font size set to 18
set xlabel "Iterations" font ",18"  # X-axis label font size set to 16
set xtics (200, 400, 600, 800, 1000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

# Load data and plot
# For a simple line plot
plot 'Othello66/AlphaViT_Small_Test.dat' using 1:2 with lines linestyle 1  title 'AlphaViT SB', \
     'Othello66/AlphaViD_Small_Test.dat' using 1:2 with lines linestyle 2  title 'AlphaViD SB', \
     'Othello66/AlphaVDA_Small_Test.dat' using 1:2 with lines linestyle 3  title 'AlphaVDA SB', \
     'Othello66/AlphaZero_Test.dat'      using 1:2 with lines linestyle 7  title 'AlphaZero'
