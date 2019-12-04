set size ratio 0.45
set terminal postscript color enhanced
set output 'unified_Mean.ps'
set linetype 1 lw 3 lc rgb '#222222'
set linetype 2 lw 3 lc rgb '#FF0000'
set linetype 3 lw 3 lc rgb '#0000FF'
set linetype 4 lw 3 lc rgb '#55FF95'
set linetype cycle 4
unset title
set tmargin -3
set bmargin -2
set rmargin 0
set lmargin 8
set border 3 front linetype -1 linewidth 2.00
set style fill solid 0.65 border -1
set style boxplot nooutliers
set style data boxplot
set boxwidth  0.15
set pointsize 0.5
set grid noxtics nomxtics ytics nomytics noztics nomztics nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics linewidth 3
set key maxrows 2
set xtics border in scale 0,0 nomirror   offset character 0.5, 0, 2 autojustify
set xtics font "Arial,25"
set xtics ('1' 0,'3' 1,'5' 2,'7' 3,'9' 4)
set xtics ('1' 0,'3' 1,'5' 2,'7' 3,'9' 4)
set key font "Arial,25"
set key spacing 1
set logscale y
set format y "%.0e"
set yrange [ : 200 ]
set ytics border in scale 0,0 mirror norotate  offset character 0.5, 0, 0 autojustify
set ytics font ",20"
set xlabel 'Number of Projection Attributes' 
set xlabel  offset character 0, 0, 0  norotate
set xlabel font 'Arial,28'
set ylabel 'Mean error rate' 
set ylabel font 'Arial,28'
set ylabel  offset character -1, 0, 0 rotate
plot 'gp_data/unified_Mean_all.csv' using  (-0.15):0 lt 1 title '1% errors', '' using  (0.85):1 lt 1 notitle, '' using  (1.85):2 lt 1 notitle, '' using  (2.85):3 lt 1 notitle, '' using  (3.85):4 lt 1 notitle, '' using  (0.0):5 lt 2 title '5% errors', '' using  (1.0):6 lt 2 notitle, '' using  (2.0):7 lt 2 notitle, '' using  (3.0):8 lt 2 notitle, '' using  (4.0):9 lt 2 notitle, '' using  (0.15):10 lt 3 title '10% errors', '' using  (1.15):11 lt 3 notitle, '' using  (2.15):12 lt 3 notitle, '' using  (3.15):13 lt 3 notitle, '' using  (4.15):14 lt 3 notitle, '' using  (0.3):15 lt 4 title '15% errors', '' using  (1.3):16 lt 4 notitle, '' using  (2.3):17 lt 4 notitle, '' using  (3.3):18 lt 4 notitle, '' using  (4.3):19 lt 4 notitle