# Gnuplot Template for PDF Output

# Set terminal and output file
#set terminal pdfcairo size 15cm,20cm enhanced font 'Arial,16'
# set output 'output.pdf'
set terminal pngcairo size 1024,1280 enhanced font 'Arial,16'
set output 'Fig7.png'

# Set multiplot layout: 2 rows, 3 columns
set multiplot layout 3,3


# Set grid and key (legend)
set grid
set key inside right bottom font ",16"  # Legend font size set to 14

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

set xrange[0:3000]
set yrange [800:2300]

# Set title and labels
set title "Connect4 AlphaViT L8" font ",18"  # Title font size set to 18

set xlabel "" font ",16"  # X-axis label font size set to 16
set ylabel "Elo rating" font ",18" # Y-axis label font size set to 16

set xtics (500, 1000, 1500, 2000, 2500, 3000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

# Load data and plot
# For a simple line plot
plot 'EloRating_Deep/Connect4/AlphaViT_Large_Test.dat' using 1:2 with lines linestyle 1 title 'Random', \
     'EloRating_Finetuning_Deep/Connect4/AlphaViT_Large_Test.dat' using 1:2 with lines linestyle 2 title 'Finetuning'

# Set title and labels
set title "Connect4 AlphaViD L5" font ",18"  # Title font size set to 18

set xlabel "" font ",16"  # X-axis label font size set to 16
set ylabel "" font ",16" # Y-axis label font size set to 16

set xtics (500, 1000, 1500, 2000, 2500, 3000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

# Load data and plot
# For a simple line plot
plot 'EloRating_Deep/Connect4/AlphaViD_Large_Test.dat' using 1:2 with lines linestyle 1 title 'Random', \
     'EloRating_Finetuning_Deep/Connect4/AlphaViD_Large_Test.dat' using 1:2 with lines linestyle 2 title 'Finetuning'


# Set title and labels
set title "Connect4 AlphaVDA L5" font ",18"  # Title font size set to 18

set xlabel "" font ",16"  # X-axis label font size set to 16
set ylabel "" font ",16" # Y-axis label font size set to 16

set xtics (500, 1000, 1500, 2000, 2500, 3000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

# Load data and plot
# For a simple line plot
plot 'EloRating_Deep/Connect4/AlphaVDA_Large_Test.dat' using 1:2 with lines linestyle 1 title 'Random', \
     'EloRating_Finetuning_Deep/Connect4/AlphaVDA_Large_Test.dat' using 1:2 with lines linestyle 2 title 'Finetuning'








# Set title and labels
set title "Gomoku AlphaViT L8" font ",18"  # Title font size set to 18

set xlabel "" font ",16"  # X-axis label font size set to 16
set ylabel "Elo rating" font ",18" # Y-axis label font size set to 16

set xtics (500, 1000, 1500, 2000, 2500, 3000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

# Load data and plot
# For a simple line plot
plot 'EloRating_Deep/Gomoku/AlphaViT_Large_Test.dat' using 1:2 with lines linestyle 1 title 'Random', \
     'EloRating_Finetuning_Deep/Gomoku/AlphaViT_Large_Test.dat' using 1:2 with lines linestyle 2 title 'Finetuning'

# Set title and labels
set title "Gomoku AlphaViD L5" font ",18"  # Title font size set to 18

set xlabel "" font ",16"  # X-axis label font size set to 16
set ylabel "" font ",16" # Y-axis label font size set to 16

set xtics (500, 1000, 1500, 2000, 2500, 3000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

# Load data and plot
# For a simple line plot
plot 'EloRating_Deep/Gomoku/AlphaViD_Large_Test.dat' using 1:2 with lines linestyle 1 title 'Random', \
     'EloRating_Finetuning_Deep/Gomoku/AlphaViD_Large_Test.dat' using 1:2 with lines linestyle 2 title 'Finetuning'

# Set title and labels
set title "Gomoku AlphaVDA L5" font ",18"  # Title font size set to 18

set xlabel "" font ",16"  # X-axis label font size set to 16
set ylabel "" font ",16" # Y-axis label font size set to 16

set xtics (500, 1000, 1500, 3000, 2000, 2500, 3000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

# Load data and plot
# For a simple line plot
plot 'EloRating_Deep/Gomoku/AlphaVDA_Large_Test.dat' using 1:2 with lines linestyle 1 title 'Random', \
     'EloRating_Finetuning_Deep/Gomoku/AlphaVDA_Large_Test.dat' using 1:2 with lines linestyle 2 title 'Finetuning'





# Set title and labels
set title "Othello AlphaViT L8" font ",20"  # Title font size set to 18

set xlabel "Iterations" font ",18"  # X-axis label font size set to 16
set ylabel "Elo rating" font ",18" # Y-axis label font size set to 16

set xtics (500, 1000, 1500, 2000, 2500, 3000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

# Load data and plot
# For a simple line plot
plot 'EloRating_Deep/Othello/AlphaViT_Large_Test.dat' using 1:2 with lines linestyle 1 title 'Random', \
     'EloRating_Finetuning_Deep/Othello/AlphaViT_Large_Test.dat' using 1:2 with lines linestyle 2 title 'Finetuning'


# Set title and labels
set title "Othello  AlphaViD L5" font ",18"  # Title font size set to 18

set xlabel "Iterations" font ",18"  # X-axis label font size set to 16
set ylabel "" font ",16" # Y-axis label font size set to 16

set xtics (500, 1000, 1500, 2000, 2500, 3000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

# Load data and plot
# For a simple line plot
plot 'EloRating_Deep/Othello/AlphaViD_Large_Test.dat' using 1:2 with lines linestyle 1 title 'Random', \
     'EloRating_Finetuning_Deep/Othello/AlphaViD_Large_Test.dat' using 1:2 with lines linestyle 2 title 'Finetuning'

# Set title and labels
set title "Othello AlphaVDA L5" font ",18"  # Title font size set to 18

set xlabel "Iterations" font ",18"  # X-axis label font size set to 16
set ylabel "" font ",16" # Y-axis label font size set to 16

set xtics (500, 1000, 1500, 2000, 2500, 3000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

# Load data and plot
# For a simple line plot
plot 'EloRating_Deep/Othello/AlphaVDA_Large_Test.dat' using 1:2 with lines linestyle 1 title 'Random', \
     'EloRating_Finetuning_Deep/Othello/AlphaVDA_Large_Test.dat' using 1:2 with lines linestyle 2 title 'Finetuning'
