import os
import math
import subprocess
#pip3 install pg8000
import pg8000
import psycopg2
from config import config
from bags import allrun
import time
from zipfile import ZipFile
import argparse

import sqlite3
import numpy as np
from sqlite3 import OperationalError
import random
import sys
import copy

dir = None
conn = None
cur = None
conn2 = None
cur2 = None

#s = [0.1, 1, 10]
s = [0.1, 1]
#x = [0.02,0.05]
x = [0.02, 0.05, 0.1, 0.3]

#psqlbin = '/Applications/Postgres.app/Contents/Versions/10/bin/psql -p5432 "uadb" -c '
gpromcom = [str("gprom"), "-host", "none", "-db", "/Users/sufeng/git/UADB_Reproducibility/dbs/incomp.db", "-port", "none", "-user", "none", "-passwd", "none", "-loglevel", "0", "-backend", "sqlite", "-Pexecutor", "sql", "-query"]

# pdbench
table_init_dir = 'table_init_sql'
pdbenchTables = ['customer','lineitem','nation','orders','part','partsupp','region','supplier']

#dir = '/Users/sufeng/sqlworkspace/pdbench'
mcdbRep = 10
test1 = ['s10_x2','s10_x5','s10_x10','s10_x30']
#test1 = ['s100_x2','s100_x5','s100_x10','s100_x30']
#test2 = ['s10_x2','s100_x2','s1000_x2']
test2 = ['s10_x2','s100_x2']
queries = ['pdQuery/Q1.sql','pdQuery/Q2.sql','pdQuery/Q3.sql']
queries_mb = ['pdQuery/Q1_maybms.sql','pdQuery/Q2_maybms.sql','pdQuery/Q3_maybms.sql']
queries_uadb = ['pdQuery/Q1_uadb.sql','pdQuery/Q2_uadb.sql','pdQuery/Q3_uadb.sql']
queries_cert = ['pdQuery/Q1_cert.sql','pdQuery/Q2_cert.sql','pdQuery/Q3_cert.sql']
    
def pushQuery(query, setion='postgresql'):
    global conn
    global cur
    if conn == None:
        try:
            params = config.config(section=setion)
            conn = psycopg2.connect(**params)
        except Exception as error:
            print(error)
    cur = conn.cursor()
    print(query)
    try:
        cur.execute(query)
        conn.commit()
    except Exception as e:
        print("query error: %s"%e)
        pass
    cur.close()
#    conn.close()
        
def runQuery(query, setion='postgresql'):
    global conn
    global cur
    if conn == None:
        try:
            # read connection parameters
            params = config.config(section=setion)
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
        except Exception as error:
            print(error)
    cur = conn.cursor()
    print(query)
    try:
        cur.execute(query)
#        conn.commit()
    except Exception as e:
        print("query error: %s"%e)
        pass
#   get outpu if any
    try:
        ret = cur.fetchall()
#        disconnect()
        return ret
    except Exception as e:
        print(e)
        pass
    except TypeError as e:
        print(e)
        pass
    cur.close()
    
def timeQuery(query, setion='postgresql'):
    ret = runQuery('EXPLAIN ANALYSE create table dummy as %s'%query, setion)
    runQuery("drop table IF EXISTS dummy;")
    return ret[-1][0].split()[-2]

def timeQuerySel(query, setion='postgresql'):
    ret = runQuery('EXPLAIN ANALYSE %s'%query, setion)
    return ret[-1][0].split()[-2]
    
def sizeQuery(query, setion='postgresql'):
    ret = runQuery('select count(*) from (%s) xyz;'%query[:-1], setion)
    return ret[-1][0];
    
def pdbenchGenOnX(sval = 1):
    global dir
    global x
    genDir = list()
    subprocess.call(["make","clean"],cwd='%s/dbgen'%dir)
    subprocess.call(["make"],cwd='%s/dbgen'%dir)
#    call dbgen
    for xval in x:
        os.chdir('%s/dbgen'%dir)
        os.system('./dbgen -x %f -s %f'%(xval,sval))
        print('./dbgen -x %f -s %f'%(xval,sval))
        os.chdir(dir)
        dirname = 's%d_x%d'%(sval*100,xval*100)
        os.system('mkdir %s'%dirname)
        os.system('mv dbgen/*.tbl %s'%dirname)
        genDir.append(dirname)
    global test1
    test1 = genDir
    
def pdbenchGenOnS(xval = 0.02):
    global dir
    global s
    genDir = list()
    subprocess.call(["make","clean"],cwd='%s/dbgen'%dir)
    subprocess.call(["make"],cwd='%s/dbgen'%dir)
#    call dbgen
    for sval in s:
        os.chdir('%s/dbgen'%dir)
        os.system('./dbgen -x %f -s %f'%(xval,sval))
        print('./dbgen -x %f -s %f'%(xval,sval))
        os.chdir(dir)
        dirname = 's%d_x%d'%(sval*100,xval*100)
        os.system('mkdir %s'%dirname)
        os.system('mv dbgen/*.tbl %s'%dirname)
        genDir.append(dirname)
    global test2
    test2 = genDir
    
#    subprocess.Popen(['%s/dbgen/dbgen'%dir, '-x', '0.02', '-s', '0.1'])

#def terminalQuery(query):
#    global psqlbin
#    os.system(psqlbin + '"%s"'%query)
        
#def importPdbenchTables(datadir):
#    for tbs in pdbenchTables:
#        with open("%s/%s.sql"%(table_init_dir, tbs)) as fp:
#            line = fp.readline()
#            while line:
#                tablename = line.split()[2]
#                terminalQuery("drop table IF EXISTS %s;"%tablename)
#                terminalQuery(line);
#                terminalQuery("COPY %s FROM '%s/%s/%s.tbl' DELIMITER '|';"%(tablename,dir,datadir,tablename))
#                line = fp.readline()
#        with open("%s/tlevel/%s.sql"%(table_init_dir, tbs)) as fp:
#            query = fp.read()
#            terminalQuery('drop table IF EXISTS %s;'%tbs)
#            terminalQuery('create table %s as %s'%(tbs,query));
#        with open("%s/uadb/%s.sql"%(table_init_dir, tbs)) as fp:
#            query = fp.read()
#            terminalQuery('drop table IF EXISTS %s_uadb;'%tbs)
#            terminalQuery('create table %s_uadb as %s'%(tbs,query));
#        with open("%s/bg/%s.sql"%(table_init_dir, tbs)) as fp:
#            query = fp.read()
#            terminalQuery('drop table IF EXISTS %s_bg;'%tbs)
#            terminalQuery('create table %s_bg as %s'%(tbs,query));
            
def importPdbenchTables(datadir):
    global conn
    with open("%s/cleanup.sql"%table_init_dir) as fp:
        line = fp.readline().split("\n")[0]
        while line:
            pushQuery(line)
            line = fp.readline()
    fp.close()
    for tbs in pdbenchTables:
        with open("%s/%s.sql"%(table_init_dir, tbs)) as fp:
            line = fp.readline().split("\n")[0]
            while line:
                tablename = line.split()[2]
#                pushQuery('drop table IF EXISTS %s;'%tablename)
                pushQuery(line);
                pushQuery("COPY %s FROM '%s/%s/%s.tbl' DELIMITER '|';"%(tablename,dir,datadir,tablename))
                line = fp.readline()
            fp.close()
        with open("%s/tlevel/%s.sql"%(table_init_dir, tbs)) as fp:
            query = fp.read()
#            pushQuery('drop table IF EXISTS %s;'%tbs)
            pushQuery('create table %s as %s'%(tbs,query));
            fp.close()
        with open("%s/uadb/%s.sql"%(table_init_dir, tbs)) as fp:
            query = fp.read()
#            pushQuery('drop table IF EXISTS %s_uadb;'%tbs)
            pushQuery('create table %s_uadb as %s'%(tbs,query));
            fp.close()
        with open("%s/bg/%s.sql"%(table_init_dir, tbs)) as fp:
            query = fp.read()
#            pushQuery('drop table IF EXISTS %s_bg;'%tbs)
            pushQuery('create table %s_bg as %s'%(tbs,query));
            fp.close()
                
def testQueryPDbench():
    global mcdbRep

    qt = list()
#    qts = list()
    uadbt = list()
    
    certt = list()
#    uadbts = list()
    mbt = list()
#    mbts = list()
    mcdbt = list()
    
    for qs in queries:
        with open(qs) as fp:
            q = fp.read()
            qt.append(timeQuery(q))
            totaltime = 0
            for i in range(0,mcdbRep):
                totaltime += float(timeQuery(q))
            mcdbt.append(str(totaltime))
#            qts.append(sizeQuery(q))
    for qs2 in queries_uadb:
        with open(qs2) as fp:
            q = fp.read()
            uadbt.append(timeQuery(q))
#            uadbts.append(sizeQuery(q))
    for qs2 in queries_cert:
        with open(qs2) as fp:
            q = fp.read()
            certt.append(timeQuery(q))
#            uadbts.append(sizeQuery(q))
    for qs3 in queries_mb:
        with open(qs3) as fp:
            q = fp.read()
            mbt.append(timeQuery(q))
#            mbts.append(sizeQuery(q))
    return [qt,uadbt,certt,mbt,mcdbt]

        
def plotPDbenchUncert(fn, maxval):
    global x
    with open("%s.gp"%fn, "w+") as file:
        file.write("\n".join([
            "set size ratio 0.5",
            "set terminal postscript color enhanced",
            "set output '%s.ps'"%fn,
            "unset title",
            "set tmargin -3",
            "set bmargin -2",
            "set rmargin 0",
            "set lmargin 8",
            "set border 3 front linetype -1 linewidth 1.000",
            "set boxwidth 0.95 absolute",
            "set style fill   solid 1.00 noborder",
            'set linetype 1 lw 1 lc rgb "#222222"',
            'set linetype 2 lw 1 lc rgb "#FF0000"',
            'set linetype 3 lw 1 lc rgb "#FFDD11"',
            'set linetype 4 lw 1 lc rgb "#0000FF"',
            'set linetype 5 lw 1 lc rgb "#55FF95"',
            "set linetype cycle 4",
            "set grid nopolar",
            "set grid noxtics nomxtics ytics nomytics noztics nomztics nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics",
            "set grid layerdefault linetype 0 linewidth 3.000,  linetype 0 linewidth 1.000",
            "set key nobox autotitles columnhead Left reverse left",
            'set key font "Arial,26"',
            "set key width 5",
            "set key samplen 2",
            "set key spacing 1",
            "set key maxrows 3",
            "set key at -0.5, %d"%int(maxval),
            "set style histogram clustered gap 1 title  offset character 2, -0.25, 1",
            "set datafile missing '-'",
            "set style data histograms",

            "set xtics border in scale 0,0 nomirror   offset character 0.5, -0.5, 2 autojustify",
            'set xtics norangelimit font ",24"',
            "set xtics   ()",
            "set xrange [ -0.5 : %d]"%len(x),
                
            'set ylabel "Runtime (ms)"',
            'set ylabel font "Arial,34"',
            "set ylabel  offset character -2, 0, 0",

            "set logscale y",
            "set yrange [ 0.1 : %d ]"%int(maxval),
            "set ytics border in scale 0,0 mirror norotate  offset character 0, 0, 0 autojustify",
            'set ytics font ",34"',

            'set xlabel font "Arial,34"',
            'set xlabel "Amount of Uncertainty"',
            "set xlabel  offset character 0, 0, 0  norotate",
                
            "plot '%s' using 2 t col, '' using 3:xtic(1) t col, '' using 4 t col, '' using 5 t col, '' using 6 t col"%fn
        ]))
        file.close()
        subprocess.call(["gnuplot", "%s.gp"%fn])
        subprocess.call(["ps2pdf", "%s.ps"%fn, "%s.pdf"%fn])
        subprocess.call(["rm", "%s.gp"%fn])
        subprocess.call(["rm", "%s.ps"%fn])
        return "%s.pdf"%fn
        
def plotPDbenchScale(fn, maxval):
    global s
    with open("%s.gp"%fn, "w+") as file:
        file.write("\n".join([
            "set size ratio 0.5",
            "set terminal postscript color enhanced",
            "set output '%s.ps'"%fn,
            "unset title",
            "set tmargin -3",
            "set bmargin -2",
            "set rmargin 0",
            "set lmargin 8",
            "set border 3 front linetype -1 linewidth 1.000",
            "set boxwidth 0.95 absolute",
            "set style fill   solid 1.00 noborder",
            'set linetype 1 lw 1 lc rgb "#222222"',
            'set linetype 2 lw 1 lc rgb "#FF0000"',
            'set linetype 3 lw 1 lc rgb "#FFDD11"',
            'set linetype 4 lw 1 lc rgb "#0000FF"',
            'set linetype 5 lw 1 lc rgb "#55FF95"',
            "set linetype cycle 4",
            "set grid nopolar",
            "set grid noxtics nomxtics ytics nomytics noztics nomztics nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics",
            "set grid layerdefault linetype 0 linewidth 3.000,  linetype 0 linewidth 1.000",
            "set key nobox autotitles columnhead Left reverse left",
            'set key font "Arial,26"',
            "set key width 5",
            "set key samplen 2",
            "set key spacing 1",
            "set key maxrows 3",
            "set key at -0.5, %d"%int(maxval),
            "set style histogram clustered gap 1 title  offset character 2, -0.25, 1",
            "set datafile missing '-'",
            "set style data histograms",

            "set xtics border in scale 0,0 nomirror   offset character 0.5, -0.5, 2 autojustify",
            'set xtics norangelimit font ",24"',
            "set xtics   ()",
            "set xrange [ -0.5 : %d]"%len(s),
                    
            'set ylabel "Runtime (ms)"',
            'set ylabel font "Arial,34"',
            "set ylabel  offset character -2, 0, 0",

            "set logscale y",
            "set yrange [ 0.1 : %d ]"%int(maxval),
            "set ytics border in scale 0,0 mirror norotate  offset character 0, 0, 0 autojustify",
            'set ytics font ",34"',

            'set xlabel font "Arial,34"',
            'set xlabel "Amount of Uncertainty"',
            "set xlabel  offset character 0, 0, 0  norotate",
                    
            "plot '%s' using 2 t col, '' using 3:xtic(1) t col, '' using 4 t col, '' using 5 t col, '' using 6 t col"%fn
        ]))
        file.close()
        subprocess.call(["gnuplot", "%s.gp"%fn])
        subprocess.call(["ps2pdf", "%s.ps"%fn, "%s.pdf"%fn])
        subprocess.call(["rm", "%s.gp"%fn])
        subprocess.call(["rm", "%s.ps"%fn])
        return "%s.pdf"%fn
        
def writetofile(fn, content):
    with open(fn,"w+") as f:
        f.write(content)
        f.close()
    
def test_pdbench_uncert():
    global test1
    global queries
    global x
    res = []
    flist = []
    for datadir in test1:
        importPdbenchTables(datadir)
        res.append(testQueryPDbench())
    #format and plot
    for i in range(0,len(queries)):
        writein = "Query\tDet\tUA-DB\tLibkin\tMayBMS\tMCDB \n"
        toplimit = 0
        for k in range(0,len(res)):
            list = res[k]
            writein = writein + "%d%%\t"%(x[k]*100);
            for j in range(0,len(list)):
                writein = writein + list[j][i] + "\t"
                toplimit = max(toplimit, int(float(list[j][i])))
            writein = writein + "\n"
#        print(writein)
        writetofile("uncert_Q%d.csv"%i, writein)
        pdfname = plotPDbenchUncert("uncert_Q%d.csv"%i, toplimit*10)
        flist.append(pdfname)
        flist.append("uncert_Q%d.csv"%i)
        
    subprocess.call(["mkdir", "results/pdbench_uncert"])
    for fn in flist:
        subprocess.call(["mv", "%s"%fn,"results/pdbench_uncert/%s"%fn])
        
def test_pdbench_scale():
    global test2
    global queries
    global s
    res = []
    flist = []
    for datadir in test2:
#        importPdbenchTables(datadir)
        res.append(testQueryPDbench())
        #format and plot
    for i in range(0,len(queries)):
        writein = "Query    Det    UA-DB    Libkin    MayBMS    MCDB \n"
        toplimit = 0
        for k in range(0,len(res)):
            list = res[k]
            writein = writein + "%dGB    "%(s[k]*100);
            for j in range(0,len(list)):
                writein = writein + list[j][i] + "    "
                toplimit = max(toplimit, int(float(list[j][i])))
            writein = writein + "\n"
        print(writein)

        writetofile("scale_Q%d.csv"%i, writein)
        pdfname = plotPDbenchScale("scale_Q%d.csv"%i, toplimit*10)
        flist.append(pdfname)
        flist.append("scale_Q%d.csv"%i)
        
    subprocess.call(["mkdir", "results/pdbench_scale"])
    for fn in flist:
        subprocess.call(["mv", "%s"%fn,"results/pdbench_scale/%s"%fn])
        
#db for incompletness test
db = 'dbs/incomp.db'
        #table
        #tb = 'pls'
tbs = ['graffiti','buffalo','busi','cont','crime','foodins','violation','permit','pls']
attrnums = [15,20,25,12,17,16,35,19,97]

def getSchema(tname, n):
    global db
    conn = sqlite3.connect(db)
    c = conn.cursor()
    res = c.execute("select * from %s limit 1;"%tname)
    names = [description[0] for description in res.description]
    return names[:n]

def runLiteQuery(q):
    global db
    conn = sqlite3.connect(db)
    c = conn.cursor()
    result = c.execute(q)
    conn.commit()
    row = result.fetchall()
    if len(row)>0:
        row = row[0]
    c.close()
    conn.close()
    return row
    
def timeLiteQuery(q):
    global db
    conn = sqlite3.connect(db)
    c = conn.cursor()
    start = time.time()
    c.execute(q)
    end = time.time()
    conn.commit()
    c.close()
    conn.close()
    return end-start
    
def runLiteQueryDB(dbn,q):
    conn = sqlite3.connect(dbn)
    c = conn.cursor()
    result = c.execute(q)
    conn.commit()
    row = result.fetchall()[0]
    c.close()
    conn.close()
    return row[0]

def onerun(attrs, n, tb):
    rd = random.sample(attrs, n)
    urd = ["U_"+itm for itm in rd]

    str = '","'.join(rd+urd)
    str = '"'+ str + '",U_R'

    wstrfn = " AND ".join(['"'+it+'"'+"='t'" for it in urd]) + " AND U_R_T='f'"
    wstrtp = " AND ".join(['"'+it+'"'+"='t'" for it in urd]) + " AND U_R_T='t'"
    wstrfp = "(" + " OR ".join(['"'+it+'"'+"='f'" for it in urd]) + ") AND U_R_T='f'"

    command = "select count(*) from (select %s from %s where %s);" % (str,tb,wstrfn)
    fn = runLiteQuery(command)
            
    command = "select count(*) from (select %s from %s where %s);" % (str,tb,wstrtp)
    tp = runLiteQuery(command)
            
    command = "select count(*) from (select %s from %s where %s);" % (str,tb,wstrfp)
    fp = runLiteQuery(command)
            
    return (tp,fn,fp),rd
    
def plotIncomplete(fn, maxx, maxy,gap):
    with open("%s.gp"%fn, "w+") as file:
        file.write("\n".join([
            "set size ratio 0.4",
            "set terminal postscript color enhanced",
            "set output '%s.ps'"%fn,
            "unset title",
            "set tmargin 0",
            "set bmargin 1",
            "set rmargin 0",
            "set lmargin 4.5",
            "set border 3 front linetype -1 linewidth 1.500",
            "set style fill solid 0.65 border -1",
            'set xlabel font "Arial,30" offset 0,-1',
            'set xlabel "Number of Projection Attributes"',
            'set xtics font "Arial,25"',
            'set xtics 1,%d'%gap,
            "set style line 1 lc rgb 'grey75' lt 1 lw 3",

            'set ylabel "false negative rate (%)" font "Arial,29"',
            "set ylabel  offset character -0.5, 0, 0",
            'set ytics font "Arial,24"',
            'set key font "Arial,28"',
            "set grid nopolar",
            "set grid noxtics nomxtics ytics nomytics noztics nomztics nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics",
            "set grid layerdefault linetype 0 linewidth 1.000,  linetype 0 linewidth 1.000",
            "set boxwidth %f absolute"%(0.55*gap),
     
            "set xrange [ 0.00000 : %d ] noreverse nowriteback"%maxx,
            "set yrange [ -0.05 : %f ] noreverse nowriteback"%maxy,
            
            "plot '%s' using 1:3:2:6:5 with candlesticks ls 1 title 'Quartiles' whiskerbars,      ''                 using 1:4:4:4:4 with candlesticks lt -1 lw 2 notitle"%fn
        ]))
        file.close()
        subprocess.call(["gnuplot", "%s.gp"%fn])
        subprocess.call(["ps2pdf", "%s.ps"%fn, "%s.pdf"%fn])
        subprocess.call(["rm", "%s.gp"%fn])
        subprocess.call(["rm", "%s.ps"%fn])
        return "%s.pdf"%fn
        
def plotUtility(fn):
    with open("%s.gp"%fn, "w+") as file:
        file.write("\n".join([
            "set size ratio 0.6",
            "set terminal postscript color enhanced",
            "set output '%s.ps'"%fn,
            "unset title",
            "set tmargin 0",
            "set bmargin 1",
            "set rmargin 0",
            "set lmargin 4.5",
            "set border 3 front linetype -1 linewidth 1.500",
            "set style fill solid 0.65 border -1",
            'set xlabel font "Arial,30" offset 0,-1',
            'set xlabel "Amount of uncertainty"',
            'set xtics font "Arial,25"',
            "set for [i=1:4] linetype i dt i",
            'set style line 1 lt 4 lc rgb "orange"  lw 9',
            'set style line 2 lt 1 lc rgb "orange" lw 9',
            'set style line 3 lt 4 lc rgb "#666666" lw 9',
            'set style line 4 lt 1 lc rgb "#666666" lw 9',
            'set style line 5 lt 4 lc rgb "#110099" lw 9',
            'set style line 6 lt 1 lc rgb "#110099" lw 9',
            'set ylabel "Rate" font "Arial,29"',
            'set ylabel  offset character -0.5, 0, 0',
            'set ytics font "Arial,23"',
            'set key inside left bottom vertical Right noreverse noenhanced autotitle nobox',
            'set key font "Arial,26"',
            'set key spacing 1',
            'set key samplen 5',
            'set grid nopolar',
            'set grid noxtics nomxtics ytics nomytics noztics nomztics nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics',
            'set grid layerdefault   linetype 0 linewidth 1.000,  linetype 0 linewidth 3.000',
            'set yrange [ 0.45 : 1.05 ] noreverse nowriteback',
            'plot "%s.csv" using 1:2 title "UADB - Precision" with lines linestyle 1, "%s.csv" using 1:3 title "UADB - Recall" with lines linestyle 2, "%s.csv" using 1:4 title "Libkin - Precision" with lines linestyle 3, "%s.csv" using 1:5 title "Libkin - Recall" with lines linestyle 4, "%s.csv" using 1:6 title "UADB(RGQP) - precision" with lines linestyle 5, "%s.csv" using 1:7 title "UADB(RGQP) - Recall" with lines linestyle 6'%(fn,fn,fn,fn,fn,fn)
        ]))
        file.close()
        subprocess.call(["gnuplot", "%s.gp"%fn])
        subprocess.call(["ps2pdf", "%s.ps"%fn, "%s.pdf"%fn])
        subprocess.call(["rm", "%s.gp"%fn])
        subprocess.call(["rm", "%s.ps"%fn])
        return "%s.pdf"%fn
        
#test result size and certain percentage
def test_pdbenchSize():
#    pdbenchGenOnX()
    global test1
    global queries
    global x
    res = []
    mbres = []
    ret = "uncert\tQ1\tQ2\tQ3\t"
    for k in range(0,len(test1)):
        datadir = test1[k]
        importPdbenchTables(datadir)
        ret = ret + "\n%d%%\t"%(x[k]*100)
        resl = []
        reslmb = []
        for i in range(0,len(queries_uadb)):
            with open(queries_uadb[i]) as fp:
                q = fp.read()
                resl.append(sizeQuery(q))
                qnew = q.split(';')[0]
                allres = runQuery("select count(*) from (%s) xx;"%qnew)[0]
                certres = runQuery("select count(*) from (%s) xx where u_r=1;"%qnew)[0]
                ret = ret + str(int(round(float(certres[0])/float(allres[0])))) + "%%(%d)\t"%certres[0]
            with open(queries_mb[i]) as fp:
                q = fp.read()
                reslmb.append(sizeQuery(q))
        res.append(resl)
        mbres.append(reslmb)
    result = "uncert\tQ1_uadb\tQ2_uadb\tQ3_uadb\tQ1_maybms\tQ2_maybms\tQ3_maybms\t"
    for i in range(0,len(res)):
        result = result + "\n%d%%\t"%int(x[i]*100)
        for j in range(0, len(res[0])):
            result = result + "%d\t"%res[i][j]
        for j in range(0, len(mbres[0])):
            result = result + "%d\t"%mbres[i][j]
    writetofile("size.csv",result)
    subprocess.call(["mkdir", "results/pdbench_stats"])
    subprocess.call(["mv", "size.csv","results/pdbench_stats/size.csv"])
    writetofile("results/pdbench_stats/uncert_percentage.csv",ret)
            
def test_ultility():
    #ultility test
    percent = [0.05,0.1,0.3,0.5]
    subprocess.call(["mkdir", "results/utility"])
    #buffalo
    dbn = 'dbs/buff_ulti.db'
    attrn = 'orig order_shooting'
    ret = "\t\tP_UADB\t\tR_UADB\t\tP_CERT\t\tR_CERT\tP_UADB_R\tR_UADB_R\n0.0\t\t1.0\t\t1.0\t\t1.0\t\t1.0\t\t1.0\t\t1.0"
    for pct in percent:
        ret += "\n%f"%pct
        tbn = 'buff'+str(int(pct*100))
        q = 'select count(*) from %s where "%s">1500 AND "%s"<2500;'%(tbn,attrn,attrn)
        rel = runLiteQueryDB(dbn, q)
        q = 'select count(*) from %s where "C_%s">1500 AND "C_%s"<2500 AND "" IN (select "" from %s where "%s">1500 AND "%s"<2500);'%(tbn,attrn,attrn,tbn,attrn,attrn)
        tp = runLiteQueryDB(dbn, q)
        q = 'select count(*) from %s where "C_%s">1500 AND "C_%s"<2500;'%(tbn,attrn,attrn)
        pred = runLiteQueryDB(dbn, q)
        uadb_precision = float(tp)/float(pred)
        uadb_recall = float(tp)/float(rel)
        ret += "\t%f"%uadb_precision
        ret += "\t%f"%uadb_recall
        q = 'select count(*) from %s where "D_%s">1500 AND "D_%s"<2500;'%(tbn,attrn,attrn)
        pred = runLiteQueryDB(dbn, q)
        q = 'select count(*) from %s where "D_%s">1500 AND "D_%s"<2500 AND "" IN (select "" from %s where "%s">1500 AND "%s"<2500 AND "U_%s2"=\'t\');'%(tbn,attrn,attrn,tbn,attrn,attrn,attrn)
        tp = runLiteQueryDB(dbn, q)
        cert_precision = float(tp)/float(pred)
        cert_recall = float(tp)/float(rel)
        ret += "\t%f"%cert_precision
        ret += "\t%f"%cert_recall
        q = 'select count(*) from %s_3 where "R_%s">\'1500\' AND "R_%s"<\'2500\';'%(tbn,attrn,attrn)
        pred = runLiteQueryDB(dbn, q)
        q = 'select count(*) from %s_3 where "R_%s">\'1500\' AND "R_%s"<\'2500\' AND "" IN (select "" from %s where "%s">\'1500\' AND "%s"<\'2500\');'%(tbn,attrn,attrn,tbn,attrn,attrn)
        tp = runLiteQueryDB(dbn, q)
        uadbr_precision = float(tp)/float(pred)
        uadbr_recall = float(tp)/float(rel)
        ret += "\t%f"%uadbr_precision
        ret += "\t%f"%uadbr_recall
#    print(ret)
    writetofile("buff.csv",ret)
    fn = plotUtility("buff")
    subprocess.call(["mv", "%s"%fn,"results/utility/%s"%fn])
    subprocess.call(["mv","buff.csv","results/utility/buff.csv"])
    
    #incom
    dbn = 'dbs/inq_ulti.db'
    attrn = 'IND235'
    ret = "\t\tP_UADB\t\tR_UADB\t\tP_CERT\t\tR_CERT\tP_UADB_R\tR_UADB_R\n0.0\t\t1.0\t\t1.0\t\t1.0\t\t1.0\t\t1.0\t\t1.0"
    for pct in percent:
        ret += "\n%f"%pct
        tbn = 'inq'+str(int(pct*100))
        q = 'select count(*) from %s where "%s"=\'99.0\';'%(tbn,attrn)
        rel = runLiteQueryDB(dbn, q)
        q = 'select count(*) from %s where "C_%s"=\'99.0\' AND "" IN (select "" from %s where "%s"=\'99.0\');'%(tbn,attrn,tbn,attrn)
        tp = runLiteQueryDB(dbn, q)
        q = 'select count(*) from %s where "C_%s"=\'99.0\';'%(tbn,attrn)
        pred = runLiteQueryDB(dbn, q)
        uadb_precision = float(tp)/float(pred)
        uadb_recall = float(tp)/float(rel)
        ret += "\t%f"%uadb_precision
        ret += "\t%f"%uadb_recall
        q = 'select count(*) from %s where "D_%s"=\'99.0\';'%(tbn,attrn)
        pred = runLiteQueryDB(dbn, q)
        q = 'select count(*) from %s where "D_%s"=\'99.0\' AND "" IN (select "" from %s where "%s"=99.0 AND "U_%s"=\'t\');'%(tbn,attrn,tbn,attrn,attrn)
        tp = runLiteQueryDB(dbn, q)
        cert_precision = float(tp)/float(pred)
        cert_recall = float(tp)/float(rel)
        ret += "\t%f"%cert_precision
        ret += "\t%f"%cert_recall
        q = 'select count(*) from %s_3 where "R_%s"=\'99.0\' AND "" IN (select "" from %s where "%s"=\'99.0\');'%(tbn,attrn,tbn,attrn)
        tp = runLiteQueryDB(dbn, q)
        q = 'select count(*) from %s_3 where "R_%s"=\'99.0\';'%(tbn,attrn)
        pred = runLiteQueryDB(dbn, q)
        uadbr_precision = float(tp)/float(pred)
        uadbr_recall = float(tp)/float(rel)
        ret += "\t%f"%uadbr_precision
        ret += "\t%f"%uadbr_recall
    writetofile("inq.csv",ret)
    fn = plotUtility("inq")
    subprocess.call(["mv", "%s"%fn,"results/utility/%s"%fn])
    subprocess.call(["mv", "inq.csv","results/utility/inq.csv"])
    
    #lisc
    dbn = 'dbs/lisc_ulti.db'
    attrn = 'ZIP CODE'
    ret = "\t\tP_UADB\t\tR_UADB\t\tP_CERT\t\tR_CERT\tP_UADB_R\tR_UADB_R\n0.0\t\t1.0\t\t1.0\t\t1.0\t\t1.0\t\t1.0\t\t1.0"
    for pct in percent:
        ret += "\n%f"%pct
        tbn = 'lisc'+str(int(pct*100))
        q = 'select count(*) from %s_3 where "%s"=\'60601\';'%(tbn,attrn)
        rel = runLiteQueryDB(dbn, q)
        q = 'select count(*) from %s_3 where "C_%s"=\'60601\' AND "" IN (select "" from %s where "%s"=\'60601\');'%(tbn,attrn,tbn,attrn)
        tp = runLiteQueryDB(dbn, q)
#        print(tp)
        q = 'select count(*) from %s_3 where "C_%s"=\'60601\';'%(tbn,attrn)
        pred = runLiteQueryDB(dbn, q)
        uadb_precision = float(tp)/float(pred)
        uadb_recall = float(tp)/float(rel)
        ret += "\t%f"%uadb_precision
        ret += "\t%f"%uadb_recall
        q = 'select count(*) from %s_3 where "D_%s"=\'60601\';'%(tbn,attrn)
        pred = runLiteQueryDB(dbn, q)
        q = 'select count(*) from %s_3 where "D_%s"=\'60601\' AND "" IN (select "" from %s where "%s"=\'60601\' AND "U_%s"=\'t\');'%(tbn,attrn,tbn,attrn,attrn)
        tp = runLiteQueryDB(dbn, q)
        cert_precision = float(tp)/float(pred)
        cert_recall = float(tp)/float(rel)
        ret += "\t%f"%cert_precision
        ret += "\t%f"%cert_recall
        q = 'select count(*) from %s_3 where "R_%s"=\'60601\';'%(tbn,attrn)
        pred = runLiteQueryDB(dbn, q)
        q = 'select count(*) from %s_3 where "R_%s"=\'60601\' AND "" IN (select "" from %s where "%s"=\'60601\');'%(tbn,attrn,tbn,attrn)
        tp = runLiteQueryDB(dbn, q)
        uadbr_precision = float(tp)/float(pred)
        uadbr_recall = float(tp)/float(rel)
#        print(uadbr_recall, uadb_recall)
        ret += "\t%f"%uadbr_precision
        ret += "\t%f"%uadbr_recall
    writetofile("lisc.csv",ret)
    fn = plotUtility("lisc")
    subprocess.call(["mv", "%s"%fn,"results/utility/%s"%fn])
    subprocess.call(["mv", "lisc.csv","results/utility/lisc.csv"])
    
        
def test_realQ():
    queries = ['realQuery/Q1.txt','realQuery/Q2.txt','realQuery/Q3.txt','realQuery/Q4.txt','realQuery/Q5.txt']
    runLiteQuery("drop table if exists dummy;")
    global gpromcom
    global dir
    gpromcom[4] = dir+"/dbs/incomp.db"
    rep = 5
    ret = "\tQ1\tQ2\tQ3\tQ4\tQ5\nOverhead\t"
    retl2 = "\nError Rate\t"
    for qf in queries:
        print("Testing Real Query %s"%qf)
        query = copy.copy(gpromcom)
        with open(qf) as fp:
            contents = fp.read().split(';')
            q = contents[0] + ";"
            qsize = "select count(*) from (" + contents[0] + ");"
            qsizeu = contents[1] + ";"
#            print(q)
            query.append(q)
            x = subprocess.check_output(query)
            x = x.decode()
            t0 = 0
            t1 = 0
            for i in range (0,rep):
                t1 += timeLiteQuery("create table dummy as " + x)
                runLiteQuery("drop table if exists dummy;")
                t0 += timeLiteQuery("create table dummy as " + q)
                runLiteQuery("drop table if exists dummy;")
            sz1 = runLiteQuery(qsize)
            sz2 = runLiteQuery(qsizeu)
            rsz = float(sz2[0])/float(sz1[0])
            ret = ret + "%s%%\t"%str(((t1-t0)/t0)*100)
            retl2 = retl2 + "%f%%\t"%(rsz*100)
    subprocess.call(["mkdir", "results/realQuery"])
    writetofile("results/realQuery/realQuery.csv",ret+retl2)
    
def test_incomp():
    subprocess.call(["mkdir", "results/incompleteness"])
    for x in range(0,len(tbs)):
        n = attrnums[x]
        attrs = getSchema(tbs[x], attrnums[x])
#        all = runLiteQuery("select count(*) from %s;" % tbs[x])
        result = ""
        maxy = 0
        gap = int(round(n/10))
        for j in range (1,n+1,gap):
            rez = []
            print(j)
            result = result + str(j) + "\t"
            for i in range(1,20):
                ct,samp = onerun(attrs, j, tbs[x])
                rez.append(ct[1][0]/(ct[0][0]+ct[1][0]+ct[2][0]))
                maxy = max(maxy, np.max(rez)*100)
            result = result + '{0:.12f}'.format(np.min(rez)*100) + "\t" +  '{0:.12f}'.format(np.percentile(rez, 25)*100) + "\t" + '{0:.12f}'.format(np.percentile(rez, 50)*100) + "\t" + '{0:.12f}'.format(np.percentile(rez, 75)*100) + "\t" + '{0:.12f}'.format(np.max(rez)*100) + "\n"
#        print(result)
        writetofile("incomp_%s.csv"%(tbs[x]), result)
        pdfname = plotIncomplete("incomp_%s.csv"%(tbs[x]),n,maxy,gap)
        subprocess.call(["mv", "incomp_%s.csv"%(tbs[x]),"results/incompleteness/incomp_%s.csv"%(tbs[x])])
        subprocess.call(["mv", "%s"%pdfname,"results/incompleteness/%s"%pdfname])
        
def test_maybms():
    global dir
    subprocess.call(["mkdir", "results/maybms"])
#    cert = [2,5]
    cert = [2,5,10,20]
    pushQuery("drop table if exists buffalo;", 'maybms')
    pushQuery("\n".join([
        'create table buffalo (',
        '"id" NUMERIC,',
        '"lat" NUMERIC,',
        '"lon" NUMERIC,',
        '"orig order_shooting" NUMERIC,',
        '"CD as number_shooting" NUMERIC,',
        '"CD_shooting" VARCHAR,',
        '"Date_shooting" VARCHAR,',
        '"Time_shooting" VARCHAR,',
        '"WeekNum_shooting" NUMERIC,',
        '"Month_shooting" VARCHAR,',
        '"Day_shooting" VARCHAR,',
        '"Hour_shooting" NUMERIC,',
        '"Year_shooting" NUMERIC,',
        '"city" VARCHAR,',
        '"state" VARCHAR,',
        '"Location_shooting" VARCHAR,',
        '"find space_shooting" NUMERIC,',
        '"street_shooting" VARCHAR,',
        '"District_shooting" VARCHAR,',
        '"Type_shooting" VARCHAR,',
        '"Victims_shooting" NUMERIC,',
        '"u_lat" VARCHAR,',
        '"u_lon" VARCHAR,',
        '"u_orig order_shooting" VARCHAR,',
        '"u_CD as number_shooting" VARCHAR,',
        '"u_CD_shooting" VARCHAR,',
        '"u_Date_shooting" VARCHAR,',
        '"u_Time_shooting" VARCHAR,',
        '"u_WeekNum_shooting" VARCHAR,',
        '"u_Month_shooting" VARCHAR,',
        '"u_Day_shooting" VARCHAR,',
        '"u_Hour_shooting" VARCHAR,',
        '"u_Year_shooting" VARCHAR,',
        '"u_city" VARCHAR,',
        '"u_state" VARCHAR,',
        '"u_Location_shooting" VARCHAR,',
        '"u_find space_shooting" VARCHAR,',
        '"u_street_shooting" VARCHAR,',
        '"u_District_shooting" VARCHAR,',
        '"u_Type_shooting" VARCHAR,',
        '"u_Victims_shooting" VARCHAR,',
        '"U_R" VARCHAR,',
        '"index" NUMERIC,',
        '"u_index" VARCHAR',
        ');'
    ]), 'maybms')
    pushQuery("copy buffalo from '%s/dbs/maybms/buffalo.csv' DELIMITER ',' CSV HEADER;"%(dir), 'maybms')
    q1u = timeQuerySel('select "U_R" from buffalo where index=1;','maybms')
    q2u = timeQuerySel('SELECT * FROM buffalo where index<2000 and index>650 and "District_shooting"=\'BD\';','maybms')
    q3u = timeQuerySel('select x.index, y.index, case when x."U_R"=\'f\' then \'f\' when y."U_R"=\'f\' then \'f\' else \'t\' end as U_R from buffalo x, buffalo y where x."District_shooting"=y."District_shooting" and x."Type_shooting"=y."Type_shooting" and x.index=690;','maybms')
    s1 = sizeQuery('select "U_R" from buffalo where index=1 and "u_index"=\'t\';','maybms')
    s2 = sizeQuery('select "U_R" from buffalo where index=1 and "u_index"=\'t\' and "U_R"=\'f\';','maybms')
    s12 = "%.2f%%"%(float(s2)/float(s1)*100)
    s3 = sizeQuery('SELECT * FROM buffalo where index<2000 and index>650 and "District_shooting"=\'BD\' and "u_index"=\'t\' and "u_District_shooting"=\'t\';','maybms')
    s4 = sizeQuery('SELECT * FROM buffalo where index<2000 and index>650 and "District_shooting"=\'BD\' and "u_index"=\'t\' and "u_District_shooting"=\'t\' and "U_R"=\'f\';','maybms')
    s34 = "%.2f%%"%(float(s4)/float(s3)*100)
    s5 = sizeQuery('select x.index, y.index, case when x."U_R"=\'f\' or y."U_R"=\'f\' then \'f\' else \'t\' end as "U_R" from buffalo x, buffalo y where x."District_shooting"=y."District_shooting" and x."Type_shooting"=y."Type_shooting" and x.index=690 and x."u_index"=\'t\' and y."u_Type_shooting"=\'t\' and x."u_Type_shooting"=\'t\' and y."u_District_shooting"=\'t\' and x."u_District_shooting"=\'t\';','maybms')
    s6 = sizeQuery('select * from (select x.index, y.index, case when x."U_R"=\'f\' or y."U_R"=\'f\' then \'f\' else \'t\' end as "U_R" from buffalo x, buffalo y where x."District_shooting"=y."District_shooting" and x."Type_shooting"=y."Type_shooting" and x.index=690 and x."u_index"=\'t\' and y."u_Type_shooting"=\'t\' and x."u_Type_shooting"=\'t\' and y."u_District_shooting"=\'t\' and x."u_District_shooting"=\'t\') z where z."U_R"=\'f\';','maybms')
    s56 = "%.2f%%"%(float(s6)/float(s5)*100)
    q1 = "Q1(time)\t" + q1u
    q2 = "Q2(time)\t" + q2u
    q3 = "Q3(time)\t" + q3u
    sq1 = "Q1(error)\t" + s12
    sq2 = "Q2(error)\t" + s34
    sq3 = "Q3(error)\t" + s56
#    print(q1,q2,q3)
    for ct in cert:
        pushQuery("drop table if exists buffalo%d;"%ct, 'maybms')
        pushQuery("drop table if exists bp%d;"%ct, 'maybms')
        pushQuery("\n".join([
            'create table buffalo%d ('%ct,
            '"id" NUMERIC,',
            '"lat" NUMERIC,',
            '"lon" NUMERIC,',
            '"orig order_shooting" NUMERIC,',
            '"CD as number_shooting" NUMERIC,',
            '"CD_shooting" VARCHAR,',
            '"Date_shooting" VARCHAR,',
            '"Time_shooting" VARCHAR,',
            '"WeekNum_shooting" NUMERIC,',
            '"Month_shooting" VARCHAR,',
            '"Day_shooting" VARCHAR,',
            '"Hour_shooting" NUMERIC,',
            '"Year_shooting" NUMERIC,',
            '"city" VARCHAR,',
            '"state" VARCHAR,',
            '"Location_shooting" VARCHAR,',
            '"find space_shooting" NUMERIC,',
            '"street_shooting" VARCHAR,',
            '"District_shooting" VARCHAR,',
            '"Type_shooting" VARCHAR,',
            '"Victims_shooting" NUMERIC,',
            '"u_lat" VARCHAR,',
            '"u_lon" VARCHAR,',
            '"u_orig order_shooting" VARCHAR,',
            '"u_CD as number_shooting" VARCHAR,',
            '"u_CD_shooting" VARCHAR,',
            '"u_Date_shooting" VARCHAR,',
            '"u_Time_shooting" VARCHAR,',
            '"u_WeekNum_shooting" VARCHAR,',
            '"u_Month_shooting" VARCHAR,',
            '"u_Day_shooting" VARCHAR,',
            '"u_Hour_shooting" VARCHAR,',
            '"u_Year_shooting" VARCHAR,',
            '"u_city" VARCHAR,',
            '"u_state" VARCHAR,',
            '"u_Location_shooting" VARCHAR,',
            '"u_find space_shooting" VARCHAR,',
            '"u_street_shooting" VARCHAR,',
            '"u_District_shooting" VARCHAR,',
            '"u_Type_shooting" VARCHAR,',
            '"u_Victims_shooting" VARCHAR,',
            '"U_R" VARCHAR,',
            '"index" NUMERIC,',
            '"p" NUMERIC',
            ');'
        ]), 'maybms')
        pushQuery("copy buffalo%d from '%s/dbs/maybms/buffalo%d.csv' DELIMITER ',' CSV HEADER;"%(ct,dir,ct), 'maybms')
#        os.system("psql -U postgres -d postgres -h 127.0.0.1 -p 5433 -c 'create table bp%d as repair key \"index\" in buffalo%d weight by \"p\";'"%(ct,ct))
        pushQuery('create table bp%d as repair key "index" in buffalo%d weight by "p";'%(ct,ct),'maybms')
        #time
        t1c = timeQuerySel('select conf() from bp%d where index=1;'%ct,'maybms')
        
        t2c = timeQuerySel('SELECT * FROM (select "District_shooting",index, conf() from bp%d group by "District_shooting",index) x where index<2000 and index>650 and "District_shooting"=\'BD\';'%ct,'maybms')
        t3c = timeQuerySel('select xind, yind,p from (select y.index as yind,x.index as xind,x."District_shooting" as xds, y."District_shooting" as yds,x."Type_shooting" as xts,y."Type_shooting" as yts, conf() as p from bp%d y, bp%d x group by y.index, x.index,y."District_shooting",x."District_shooting",x."Type_shooting",y."Type_shooting") z where xds=yds and xts=yts and xind=690;'%(ct,ct),'maybms')
        t1 = timeQuerySel('select conf(\'A\', 0.3) from bp%d where index=1;'%ct,'maybms')
        t2 = timeQuerySel('SELECT * FROM (select "District_shooting",index, conf(\'A\', 0.3) from bp%d group by "District_shooting",index) x where index<2000 and index>650 and "District_shooting"=\'BD\';'%ct,'maybms')
        t3 = timeQuerySel('select xind, yind,p from (select y.index as yind,x.index as xind,x."District_shooting" as xds, y."District_shooting" as yds,x."Type_shooting" as xts,y."Type_shooting" as yts, conf(\'A\', 0.3) as p from bp%d y, bp%d x group by y.index, x.index,y."District_shooting",x."District_shooting",x."Type_shooting",y."Type_shooting") z where xds=yds and xts=yts and xind=690;'%(ct,ct),'maybms')
        #error
        s2c = sizeQuery('select conf() from bp%d where index=1;'%ct,'maybms')
        s1c = sizeQuery('select * from (select conf() as cf from bp%d where index=1) x where x.cf!=1.0;'%ct,'maybms')
#        print(s1c,s2c)
        s12c = "%.2f%%"%(float(s1c)/float(s2c)*100)
        s4c = sizeQuery('SELECT * FROM (select "District_shooting",index, conf() from bp%d group by "District_shooting",index) x where index<2000 and index>650 and "District_shooting"=\'BD\';'%ct,'maybms')
        s3c = sizeQuery('SELECT * FROM (select "District_shooting",index, conf() as cf from bp%d group by "District_shooting",index) x where index<2000 and index>650 and "District_shooting"=\'BD\' and x.cf!=1.0;'%ct,'maybms')
#        print(s3c,s4c)
        s34c = "%.2f%%"%(float(s3c)/float(s4c)*100)
        s6c = sizeQuery('select xind, yind,p from (select y.index as yind,x.index as xind,x."District_shooting" as xds, y."District_shooting" as yds,x."Type_shooting" as xts,y."Type_shooting" as yts, conf() as p from bp%d y, bp%d x group by y.index, x.index,y."District_shooting",x."District_shooting",x."Type_shooting",y."Type_shooting") z where xds=yds and xts=yts and xind=690;'%(ct,ct),'maybms')
        s5c = sizeQuery('select * from (select xind, yind,p from (select y.index as yind,x.index as xind,x."District_shooting" as xds, y."District_shooting" as yds,x."Type_shooting" as xts,y."Type_shooting" as yts, conf() as p from bp%d y, bp%d x group by y.index, x.index,y."District_shooting",x."District_shooting",x."Type_shooting",y."Type_shooting") z where xds=yds and xts=yts and xind=690) ax where p!=1.0;'%(ct,ct),'maybms')
#        print(s5c,s6c)
        s56c = "%.2f%%"%(float(s5c)/float(s6c)*100)
        s2 = sizeQuery('select conf(\'A\', 0.3) from bp%d where index=1;'%ct,'maybms')
        s1 = sizeQuery('select * from (select conf(\'A\', 0.3) as cf from bp%d where index=1) x where x.cf!=1.0;'%ct,'maybms')
        s12 = "%.2f%%"%(float(s1)/float(s2)*100)
        s4 = sizeQuery('SELECT * FROM (select "District_shooting",index, conf(\'A\', 0.3) from bp%d group by "District_shooting",index) x where index<2000 and index>650 and "District_shooting"=\'BD\';'%ct,'maybms')
        s3 = sizeQuery('SELECT * FROM (select "District_shooting",index, conf(\'A\', 0.3) as cf from bp%d group by "District_shooting",index) x where index<2000 and index>650 and "District_shooting"=\'BD\' and ((x.cf<1.0 and x.cf>0.99)or(x.cf>0 and x.cf<0.01));'%ct,'maybms')
        s34 = "%.2f%%"%(float(s3)/float(s4)*100)
        s6 = sizeQuery('select xind, yind,p from (select y.index as yind,x.index as xind,x."District_shooting" as xds, y."District_shooting" as yds,x."Type_shooting" as xts,y."Type_shooting" as yts, conf(\'A\', 0.3) as p from bp%d y, bp%d x group by y.index, x.index,y."District_shooting",x."District_shooting",x."Type_shooting",y."Type_shooting") z where xds=yds and xts=yts and xind=690;'%(ct,ct),'maybms')
        s5 = sizeQuery('select * from (select xind, yind,p from (select y.index as yind,x.index as xind,x."District_shooting" as xds, y."District_shooting" as yds,x."Type_shooting" as xts,y."Type_shooting" as yts, conf(\'A\', 0.3) as p from bp%d y, bp%d x group by y.index, x.index,y."District_shooting",x."District_shooting",x."Type_shooting",y."Type_shooting") z where xds=yds and xts=yts and xind=690) ax where ((p<1.0 and p>0.99)or(p>0 and p<0.01));'%(ct,ct),'maybms')
        s56 = "%.2f%%"%(float(s5)/float(s6)*100)
        q1 += "\t%s(%s)"%(t1,t1c)
        q2 += "\t%s(%s)"%(t2,t2c)
        q3 += "\t%s(%s)"%(t3,t3c)
        sq1 += "\t%s(%s)"%(s12,s12c)
        sq2 += "\t%s(%s)"%(s34,s34c)
        sq3 += "\t%s(%s)"%(s56,s56c)
    ret = "\t\tUADB\t\tMB-02\t\tMB-05\t\tMB-10\t\tMB-20\n"
    ret += q1 + "\n" + sq1 + "\n" + q2 + "\n" + sq2 + "\n" + q3 + "\n" + sq3
    writetofile("results/maybms/maybms.csv", ret)
    
def test_bags():
    ret = allrun()
#    print(ret)
    writetofile("bags.csv", ret)
    with open("bags.gp", "w+") as file:
        file.write("\n".join([
            'set size ratio 0.35',
            'set terminal postscript color enhanced',
            "set output 'bags.ps'",
            'unset title',
            'set tmargin 0',
            'set bmargin 1',
            'set rmargin 0',
            'set lmargin 4.5',
            'set border 3 front linetype -1 linewidth 1.500',
            'set style fill solid 0.65 border -1',
            'set xlabel font "Arial,30" offset 0,-1',
            'set xlabel "Number of projection attributes"',
            'set xtics font "Arial,25"',
            'set style line 1 lt 1 lc rgb "#AA00FF" lw 9',
            'set style line 2 lt 1 lc rgb "#0055AA" lw 9',
            'set style line 3 lt 1 lc rgb "#FFAA00" lw 9',
            'set ylabel "Mean error rate" font "Arial,29"',
            'set ylabel  offset character -0.5, 0, 0',
            'set ytics font "Arial,23"',
            'set key inside right top vertical Right noreverse noenhanced autotitle nobox',
            'set key font "Arial,26"',
            'set key spacing 1',
            'set grid nopolar',
            'set grid noxtics nomxtics ytics nomytics noztics nomztics nox2tics nomx2tics noy2tics nomy2tics nocbtics nomcbtics',
            'set grid layerdefault   linetype 0 linewidth 1.000,  linetype 0 linewidth 3.000',
            'set yrange [ 0 : 0.055 ] noreverse nowriteback',
            'plot "bags.csv" using 1:2 title \'buffalo\' with lines linestyle 1, "bags.csv" using 1:3 title \'foodins\' with lines linestyle 2, "bags.csv" using 1:4 title \'permits\' with lines linestyle 3'
        ]))
        file.close()
    subprocess.call(["gnuplot", "bags.gp"])
    subprocess.call(["ps2pdf", "bags.ps", "bags.pdf"])
    subprocess.call(["rm", "bags.gp"])
    subprocess.call(["rm", "bags.ps"])
    subprocess.call(["mkdir", "results/bags"])
    subprocess.call(["mv", "bags.pdf","results/bags/bags.pdf"])
    subprocess.call(["mv", "bags.csv","results/bags/bags.csv"])
    
def test_secu():
    subprocess.call(["mkdir", "results/security"])
    subprocess.call(["python3", "security_semiring/draw.py"])
    subprocess.call(["cp", "security_semiring/unified_final_mean.pdf","results/security/unified_final_mean.pdf"])
    
def exittest():
    print("Closing postgres servers")
    os.system('sudo -u postgres /usr/lib/postgresql/9.5/bin/pg_ctl -D /postgresdata -m fast stop')
    os.system('sudo -u postgres /maybms/install/bin/pg_ctl -D /maybms/data -m fast stop')
#    time.sleep(10)
    quit()
        
        
if __name__ == '__main__':
    dir = os.path.dirname(os.path.abspath(__file__))
    print(dir)
    subprocess.call(["mkdir", "results"])
    
    #start postgres server
    print("start server")
#    os.system('sudo -u postgres /usr/lib/postgresql/9.5/bin/pg_ctl -D /postgresdata stop')
#    os.system('sudo -u postgres /maybms/install/bin/pg_ctl -D /maybms/data stop')
    os.system('sudo -u postgres /usr/lib/postgresql/9.5/bin/pg_ctl -o "-p 5432" -D /postgresdata restart')
    os.system('sudo -u postgres /maybms/install/bin/pg_ctl -o "-p 5433" -D /maybms/data restart')
#    subprocess.Popen(["sudo","-u","postgres","/usr/lib/postgresql/9.5/bin/pg_ctl", "-o", '"-p 5432"', "-D", "/postgresdata", "start"],shell=False,close_fds=True)
#    subprocess.Popen(["sudo","-u","postgres","/maybms/install/bin/pg_ctl", "-o", '"-p 5464"', "-D", "/maybms/data", "start"],shell=False,close_fds=True)
    time.sleep(10)
#    print("server started")
    
    
    #parse arguments
    helpmsg  = "UADB reproducibility main script. By default the script will run all default test and if interrupted continue running from last experiment without repeating previous experiments."
    
    parser = argparse.ArgumentParser(description=helpmsg)
    parser.add_argument("-r", "--redo", help="Start the script from begining discrd all progress", action="store_true")
    parser.add_argument("-s", "--step", help="Specify a single step to execute")
    args = parser.parse_args()
    singlestep = -1
    if args.step:
        singlestep = int(args.step)
    if args.redo:
        config.stepsetconfig(curstep=1)
    
    curs = config.stepconfig()
#    unzip databases
#    if curs == 0:
#        print('Unzipping tables')
#        with ZipFile('dbs/dbs.zip', 'r') as zipObj:
#            zipObj.extractall(path='dbs/')
#        curs += 1
#        config.stepsetconfig(curs)
#        if singlestep==0:
#            exittest()
#    else:
#        print("By passing unzip")
    
    if (curs==1 and (singlestep == 2 or singlestep == 3 or singlestep == 4 or singlestep == -1)) or singlestep == 1:
        pdbenchGenOnX(0.1)#gen pdbench uncert
        pdbenchGenOnS()#gen pdbench scale.
        curs += 1
        config.stepsetconfig(curs)
        if singlestep==1:
            exittest()
    else:
        print("By passing pdbench gen")
        
    if curs == 2 and singlestep == -1 or singlestep == 2:
        test_pdbench_uncert()
        if(singlestep == -1):
            curs += 1
        else:
            exittest()
        config.stepsetconfig(curs)
    else:
        print("By passing PDbench uncert test")
#
    if curs == 3 and singlestep == -1 or singlestep == 3:
        test_pdbench_scale()
        if(singlestep == -1):
            curs += 1
        else:
            exittest()
        config.stepsetconfig(curs)
    else:
        print("By Passing PDbench scale test")

    if curs == 4 and singlestep == -1 or singlestep == 4:
        test_pdbenchSize()
        if(singlestep == -1):
            curs += 1
        else:
            exittest()
        config.stepsetconfig(curs)
    else:
        print("By passing PDbench size test")

    if curs == 5 and singlestep == -1 or singlestep == 5:
        test_incomp()
        if(singlestep == -1):
            curs += 1
        else:
            exittest()
        config.stepsetconfig(curs)
    else:
        print("By passing incomplete test")

    if curs == 6 and singlestep == -1 or singlestep == 6:
        test_ultility()
        if(singlestep == -1):
            curs += 1
        else:
            exittest()
        config.stepsetconfig(curs)
    else:
        print("By passing ultility test")
        
    if curs == 7 and singlestep == -1 or singlestep == 7:
        test_realQ()
        if(singlestep == -1):
            curs += 1
        else:
            exittest()
        config.stepsetconfig(curs)
    else:
        print("By passing real query test")
        
    if curs == 8 and singlestep == -1 or singlestep == 8:
        test_maybms()
        if(singlestep == -1):
            curs += 1
        else:
            exittest()
        config.stepsetconfig(curs)
    else:
        print("By passing maybms test")
        
    if curs == 9 and singlestep == -1 or singlestep == 9:
        test_bags()
        if(singlestep == -1):
            curs += 1
        else:
            exittest()
        config.stepsetconfig(curs)
    else:
        print("By passing bags test")
        
    if curs == 10 and singlestep == -1 or singlestep == 10:
        test_secu()
        if(singlestep == -1):
            curs += 1
        else:
            exittest()
        config.stepsetconfig(curs)
    else:
        print("By passing security semiring test")
        
    
        
    exittest()
#    subprocess.call(["/usr/lib/postgresql/9.5/bin/pg_ctl", "-D", "/postgresdata", "stop"])
    
