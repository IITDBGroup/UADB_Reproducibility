
import csv
from collections import defaultdict
import subprocess
import sys
import os

attrs = [1, 3, 5, 7, 9]

experiment = "with_stable_choices_18"

uncertainty = [
  (1,1),
  # (5,1),
  # (10,1),
  (1,5),
  # (5,5), 
  # (10,5), 
  (1,10), 
  # (5,10),
  # (10,10),
  (1,15),
  # (5,15), 
  # (10,15)
]
uncertainty_lookup = dict([
  ("{}{}".format(*x), x)
  for x in uncertainty
])

datasets = {
  'chi_crime',
  'food_inspec',
  'bus_lic',
  'contracts',
  'build_vio',
  'graf_rmv',
  'more_tables'
}

if len(sys.argv) > 1:
  datasets = sys.argv[1:]


all_metrics = ["RMS", "Mean"]
try:
  os.mkdir("gp_data")
except:
  print("dir already there")

for metric in all_metrics:
  target_field = "Ave_C_{}".format(metric)
  data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [])))

  for a in attrs:
    filename = '{}/{}_ProjectedAttr.csv'.format(experiment, a)
    print("Processing {} for {}".format(filename, metric))
    with open(filename) as file:
      reader = csv.reader(file)
      schema = next(reader)
      schema = dict(zip(schema, range(0, len(schema))))
      
      for row in reader:
        u, ds = row[schema["Table"]].split("_sec_")
        if str(u) in uncertainty_lookup:
          u = uncertainty_lookup.get(u)[1]
          data[ds][a][u].append(float(row[schema[target_field]]))
        # else:
        #   print(u)
        #   print("Skipping {} in {}".format(u, ds))
  try:
    os.unlink("gp_data/unified_{}_all.csv".format(metric))
  except:
    print("no files to delete")
  for ds in datasets:
    with open("gp_data/{}_{}.csv".format(ds, metric), "w+") as file:
      writer = csv.writer(file, delimiter='\t')
      for a in attrs:
        writer.writerow([a]+[
          sum(data[ds][a][u])
          for (c, u) in uncertainty
        ])
    with open("gp_data/{}_{}_all.csv".format(ds, metric), "w+") as file:
      writer = csv.writer(file, delimiter='\t')
      row_data = [
        data[ds][a][u]
        for (c, u) in uncertainty
        for a in attrs
      ] # output schema: (u1, a1), (u1, a2), (u1, a3), ...
      row_data = zip(*row_data)
      for row in row_data:
        writer.writerow(list(row))

    with open("gp_data/unified_{}_all.csv".format(metric), "a") as file:
      writer = csv.writer(file, delimiter='\t')
      row_data = [
        data[ds][a][u]
        for (c, u) in uncertainty
        for a in attrs
      ] # output schema: (u1, a1), (u1, a2), (u1, a3), ...
      row_data = zip(*row_data)
      for row in row_data:
        writer.writerow(list(row))



# with open("plot.gp", "w+") as file:

for metric in all_metrics:
  for ds in list(datasets) + ["unified"]:
    plot_cmd = "plot 'gp_data/{}_{}_all.csv' using ".format(ds, metric)

    columns = [
      (i, u, j)
      for (i, (c, u)) in zip(range(0, len(uncertainty) ), uncertainty)
      for (j) in range(0, len(attrs))
    ]

    plot_lines = [
      " ({}):{} lt {} {}".format(
        a_idx+(u_idx-1)*0.15, 
        col_idx,
        u_idx+1,
        "title '{}% errors'".format(u) if a_idx == 0 else "notitle"
      )
      for (col_idx, (u_idx, u, a_idx)) in zip(range(0, len(columns)), columns)
    ]
    plot_cmd += ", '' using ".join(plot_lines)
    # print(plot_cmd)
    x_ticks = "set xtics ("+",".join([
      "'{}' {}".format(a, j)
      for (j, a) in zip(range(0, len(attrs)), attrs)
    ])+")"

    with open("draw.gp", "w+") as file:
      file.write("\n".join(
        [
          "set size ratio 0.5",
          "set terminal postscript color enhanced",
          "set output '{}_{}.ps'".format(ds,metric),
          # "set terminal png",
          # "set output '{}.png'".format(ds),
          # # Linetype
          "set linetype 1 lw 1 lc rgb '#222222'",
          "set linetype 2 lw 1 lc rgb '#FF0000'",
          "set linetype 3 lw 1 lc rgb '#0000FF'",
          "set linetype 4 lw 1 lc rgb '#55FF95'",
          "set linetype cycle 4",
          # Title
          "unset title",
          # # Margins
          "set tmargin -3",
          "set bmargin -2",
          "set rmargin 0",
          "set lmargin 8",

          # border
          "set border 3 front linetype -1 linewidth 2.00",

          # # Boxes
          "set style fill solid 0.65 border -1",
          "set style boxplot nooutliers",
          "set style data boxplot",
          "set boxwidth  0.15",
          "set pointsize 0.5",
          # "set boxwidth 0.95 absolute",
          # "set style fill   solid 1.00 noborder",

          # Grid
          # "set grid nopolar",
          "set grid noxtics nomxtics ytics nomytics noztics nomztics nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics linewidth 1.5",
          # "set grid layerdefault   linetype 0 linewidth 3.000,  linetype 0 linewidth 1.000",

          # Key
          # "set key nobox autotitles columnhead Left reverse left",
          # "set key font 'Arial,24'",
          # "set key width 5",
          # "set key samplen 2",
          "set key spacing 3.0",
            "set key maxrows 2",
          # "set key at -0.5,700",

          # Axis
          "set xtics border in scale 0,0 nomirror   offset character 0.5, -0.5, 2 autojustify",
         'set xtics font "Arial,20"',
         "set xtics ('1' 0,'3' 1,'5' 2,'7' 3,'9' 4)",
          # "set xtics norangelimit font ',24'",
          # "set xtics   ()",
          x_ticks,
         
         'set key font "Arial,25"',
         "set key spacing 3.0",

          "set logscale y",
          'set format y "%e"',
          "set yrange [ : 200 ]",
          "set ytics border in scale 0,0 mirror norotate  offset character 0, 0, 0 autojustify",
          # "set ytics font ',34'",
         'set ytics font ",15"',

          # "set xlabel font 'Arial,34'",
          "set xlabel 'Number of Projection Attributes' ",
          "set xlabel  offset character 0, 0, 0  norotate",
         "set xlabel font 'Arial,26'",

          "set ylabel 'Mean error rate dshkdhsajfkdshjakf' ".format(metric),
          "set ylabel font 'Arial,25'",
          "set ylabel  offset character 2, 0, 0 rotate",

          plot_cmd
        ]
      ))
    subprocess.call(["gnuplot", "draw.gp"])

