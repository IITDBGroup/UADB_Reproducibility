# length/width ratio and terminal
set size ratio 0.5
set terminal postscript color enhanced  
set output 'gprom_oracle_flight_uni.ps'

# Title
unset title

# Margins
set tmargin -3
set bmargin -2
set rmargin 0
set lmargin 8

# border
set border 3 front linetype -1 linewidth 1.000

# Boxes
set boxwidth 0.95 absolute
set style fill   solid 1.00 noborder

# line styles
set linetype 1 lw 1 lc rgb "#222222" 
set linetype 2 lw 1 lc rgb "#FF0000"
set linetype 3 lw 1 lc rgb "#0000FF" 
set linetype 4 lw 1 lc rgb "#55FF95"

set linetype cycle 4

# Grid
set grid nopolar
set grid noxtics nomxtics ytics nomytics noztics nomztics \
 nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics
set grid layerdefault   linetype 0 linewidth 3.000,  linetype 0 linewidth 1.000

# Key
set key nobox autotitles columnhead Left reverse left
set key font "Arial,28"
set key width 5
set key samplen 2
set key spacing 1
set key maxrows 2
set key at -0.5,700

# style - histogram
set style histogram clustered gap 2 title  offset character 2, 0.25, 0
set datafile missing '-'
set style data histograms

# Axis
set xtics border in scale 0,0 nomirror   offset character 0.5, -0.5, 2 autojustify
set xtics norangelimit font ",25"
set xtics   ()
set xrange [ -0.5 : 3]

set logscale y
set yrange [ 0.1 : 300 ]
set ytics border in scale 0,0 mirror norotate  offset character 0, 0, 0 autojustify
set ytics font ",34"

set xlabel font "Arial,34"
set xlabel "\nData Scaling" 
set xlabel  offset character 0, 0, 0  norotate


set ylabel "Runtime (sec)" 
set ylabel font "Arial,34"
set ylabel  offset character -2, 0, 0

# Plot command
plot 'gprom_oracle_flight_uni.csv' using 2 t col, '' using 3:xtic(1) t col, '' using 4 t col, '' using 5 t col
