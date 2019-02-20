set term pdf font ",80" size 14,8
set size ratio 0.67
set lmargin at screen 0.25

set style data lines
set yrange[0.25:0.5]

set xlabel "|S|"
set ylabel "p"

set xtics 1
set ytics 0.05

#set key bottom right
#set key out top center
#set key out top right

set output "tmp.pdf"

plot "Res_To_Plot_5.dat" using 1:2 notitle with linespoints lt rgb "blue" lw 8 pointtype 4 pointsize 2, "Res_To_Plot_5.dat" using 1:3 notitle with linespoints lt rgb "orange" lw 8 pointtype 8 pointsize 2

set output

##############################################
set term pdf font ",80" size 14,8
set size ratio 0.67
#set bmargin 5
#unset lmargin

set style data lines
set yrange[0.25:0.5]

set xlabel "|S|"
set noylabel

set xrange[1:10]
set xtics 2
set ytics 0.05
set format y ""

#set key bottom right
#set key out top center
#set key out top right

set output "tmp2.pdf"

plot "Res_To_Plot_10.dat" using 1:2 notitle with linespoints lt rgb "blue" lw 8 pointtype 4 pointsize 2, "Res_To_Plot_10.dat" using 1:3 notitle with linespoints lt rgb "orange" lw 8 pointtype 8 pointsize 2

set output

##############################################
set term pdf font ",80" size 14,8
set size ratio 0.67
#set bmargin 5

set style data lines
set yrange[0.25:0.5]

set xlabel "|S|"
set noylabel

set xrange[1:15]
set xtics 3
set ytics 0.05
set format y ""
set key bottom right
set key font ",64"

set output "tmp3.pdf"

plot "Res_To_Plot_15.dat" using 1:2 title "variable C" with linespoints lt rgb "blue" lw 8 pointtype 4 pointsize 2, "Res_To_Plot_15.dat" using 1:3 title "C=|S|" with linespoints lt rgb "orange" lw 8 pointtype 8 pointsize 2

set output
