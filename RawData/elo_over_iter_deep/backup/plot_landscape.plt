# Gnuplot Template for PDF Output

# Set terminal and output file
set terminal pdfcairo size 16cm,10cm enhanced font 'Arial,14'
set output 'output.pdf'

# Set multiplot layout: 2 rows, 3 columns
set multiplot layout 1,3


# Set grid and key (legend)
set grid
set key inside right bottom font ",10"  # Legend font size set to 14

set xtics (200, 400, 600, 800, 1000) font ",12"
set ytics font ",12"  # Y-axis ticks font size set to 14

set lmargin -1
set bmargin -1
set rmargin 2
set tmargin 3


# Set colorblind-friendly line styles
set style line 1 lc rgb '#0072B2' dt 1 lw 2 pt 0 ps 1.5  # Blue
set style line 2 lc rgb '#D55E00' dt 1 lw 2 pt 0 ps 1.5  # Vermilion
set style line 3 lc rgb '#009E73' dt 1 lw 2 pt 0 ps 1.5  # Green
set style line 4 lc rgb '#0072B2' dt 2 lw 2 pt 0 ps 1.5  # Yellow
set style line 5 lc rgb '#D55E00' dt 2 lw 2 pt 0 ps 1.5  # Purple
set style line 6 lc rgb '#009E73' dt 2 lw 2 pt 0 ps 1.5  # Light Blue
set style line 7 lc rgb '#F0E442' dt 1 lw 2 pt 0 ps 1.5  # Orange

# Set xrange and yrange (optional)
# set xrange [0:10]
set yrange [1000:2200]



# Set title and labels
set title "Connect4" font ",16"  # Title font size set to 18

set xlabel "" font ",14"  # X-axis label font size set to 16
set ylabel "Elo" font ",14" # Y-axis label font size set to 16

# Load data and plot
# For a simple line plot
plot 'Connect4/AlphaViT_Large_Test.dat' using 1:2 with lines linestyle 1 title 'AlphaViT Large', \
     'Connect4/AlphaViD_Large_Test.dat' using 1:2 with lines linestyle 2 title 'AlphaViD Large', \
     'Connect4/AlphaVDA_Large_Test.dat' using 1:2 with lines linestyle 3 title 'AlphaVDA Large', \
     'Connect4/AlphaViT_Multi_Test.dat' using 1:2 with lines linestyle 7  title 'AlphaViT Multi', \
     'Connect4/AlphaViD_Multi_Test.dat' using 1:2 with lines linestyle 8  title 'AlphaViD Multi', \
     'Connect4/AlphaVDA_Multi_Test.dat' using 1:2 with lines linestyle 9  title 'AlphaVDA Multi'


set title "Gomoku" font ",16"  # Title font size set to 18
set xlabel "" font ",14"  # X-axis label font size set to 16
set ylabel "" font ",14" # Y-axis label font size set to 16

# Load data and plot
# For a simple line plot
plot 'Gomoku/AlphaViT_Large_Test.dat' using 1:2 with lines linestyle 1  title 'AlphaViT Large', \
     'Gomoku/AlphaViD_Large_Test.dat' using 1:2 with lines linestyle 2  title 'AlphaViD Large', \
     'Gomoku/AlphaVDA_Large_Test.dat' using 1:2 with lines linestyle 3  title 'AlphaVDA Large', \
     'Gomoku/AlphaViT_Multi_Test.dat' using 1:2 with lines linestyle 7  title 'AlphaViT Multi', \
     'Gomoku/AlphaViD_Multi_Test.dat' using 1:2 with lines linestyle 8  title 'AlphaViD Multi', \
     'Gomoku/AlphaVDA_Multi_Test.dat' using 1:2 with lines linestyle 9  title 'AlphaVDA Multi'

set title "Othello" font ",16"  # Title font size set to 18
set xlabel "" font ",14"  # X-axis label font size set to 16
set ylabel "" font ",14" # Y-axis label font size set to 16

# Load data and plot
# For a simple line plot
plot 'Othello/AlphaViT_Large_Test.dat' using 1:2 with lines linestyle 1  title 'AlphaViT Large', \
     'Othello/AlphaViD_Large_Test.dat' using 1:2 with lines linestyle 2  title 'AlphaViD Large', \
     'Othello/AlphaVDA_Large_Test.dat' using 1:2 with lines linestyle 3  title 'AlphaVDA Large', \
     'Othello/AlphaViT_Multi_Test.dat' using 1:2 with lines linestyle 7  title 'AlphaViT Multi', \
     'Othello/AlphaViD_Multi_Test.dat' using 1:2 with lines linestyle 8  title 'AlphaViD Multi', \
     'Othello/AlphaVDA_Multi_Test.dat' using 1:2 with lines linestyle 9  title 'AlphaVDA Multi'
