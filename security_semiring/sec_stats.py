import sqlite3
import random
import sys
import csv
import numpy as np
import time

import pandas as pd

#open a connection to the appropriate sqlite3 database
db = 'test.db'
conn= sqlite3.connect(db)
c = conn.cursor()
#import all table names
q_tb = 'select name from sqlite_master where type = "table";'
tbs = [row[0] for row in c.execute(q_tb)]
#filter out all tables that are not for the bag security ring experiment
'''
    another_way = list(filter(lambda x: x.startswith('sec'), tbs))
    print("Another way: %s" %(another_way))
    '''
matchers = ('11_', '1010_', '55_', '1015_')
tbs = [tb for tb in tbs if tb[0].isdigit() and tb.startswith(matchers)]

tbs.sort()



#list of pre-computed results
pre_comp = []
#stores results for each test run
trials_res = []

#number of attributes to project
n = int(sys.argv[1])


#For testing, have the option to only work on one table
do_batch = True

#compute RMS per Oliver's definition: sqrt[\sum_{t \in T} (c_label_t - actual_t)^2 / 5] / |T|
def comp_rms(u_col, c_col, tb):
    #print(u_col, c_col, tb)
    query = 'select sum(%s* 1.0/5 * %s * 1.0/5) as u_rms, sum(%s *1.0/5 * %s * 1.0/5) as c_rms, count(*) as c from %s;' % (u_col, u_col, c_col, c_col, tb)
    u_rms, c_rms, cnt = c.execute(query).fetchall()[0]
    #we need to finish the rms computation, i.e. take the square root and divide by |T|
    rms = np.divide(np.sqrt(np.array([u_rms, c_rms])), cnt)
    return rms

#Gathers existing annotation stats before computing queries
def comp_mean(u_col, c_col, tb):
    #There are 5 levels in the security semiring, so we make the distance metric to be divisible by 5
    query = 'select avg(%s* 1.0/5) as u_mean, avg(%s * 1.0/5) as c_mean from %s;' % (u_col, c_col, tb)
    #type of c.execute(query).fetchall() is list[tuple], because this is an agg query, the size is one tuple
    result = c.execute(query).fetchall()[0]
    return result

#performs the test query, aggregates label distance from ground truth (r)
def onerun(attrs, n, tb):
    rd = random.sample(attrs, n)
    #print(rd, tb)
    attr_list = '", "'.join(rd)
    attr_list = '"' + attr_list + '"'
    inner_q1 = '(SELECT %s, max(u_label) as u_new, max(c_label) as c_new, max(actual) as r_new FROM %s GROUP BY %s));' % (attr_list, tb, attr_list)
    inner_q2 = '(SELECT %s, u_new, c_new, r_new, u_new - r_new as u_newdist, r_new - c_new as c_newdist FROM ' % (attr_list)
    #outer_q = 'SELECT (sum(u_newdist) * 1.0/5) as u_newmean, (sum(c_newdist) * 1.0/5) as c_newmean FROM '
    #outer_rms = 'SELECT (sum(u_newdist) * sum(u_newdist) * 1.0/5) / count(*) as u_rms, (sum(c_newdist) * sum(c_newdist) * 1.0/ 5) / count(*) as c_rms FROM '

    #sqlite3 requires alphanumeric names to be quoted; to get the table name, strip the quotes
    interim_tb = 'stats_' + tb[1:-1]
    query_tb = 'CREATE TABLE %s AS %s %s;' % (interim_tb, inner_q2[1:], inner_q1[:-2])
    c.execute(query_tb)
    conn.commit()
    result = comp_mean('u_newdist', 'c_newdist', interim_tb)
    rms = comp_rms('u_newdist', 'c_newdist', interim_tb)
    #print('Comp Mean (func): %s\nComp_rms (func): %s\n ++++++++++' %(result, rms))

    c.execute('drop table {}'.format(interim_tb))
    conn.commit()
    return result, rms

counter = 0
start = time.time()

file_name = str(n) + '_ProjectedAttr'
fields = ['Table', 'Pre_U_Mean', 'Pre_C_Mean', 'Pre_U_RMS', 'Pre_C_RMS', 'Ave_U_Mean', 'Ave_C_Mean', 'Ave_U_RMS', 'Ave_C_RMS']

with open(file_name, mode='w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()

for tb in tbs:
    if counter % 6 == 0:
        end = time.time()
        sec = int((end - start) % 60)
        min = int((end - start) / 60)
        time_comp = '%s:%s' % (min, sec)
        print(time_comp)
        print(tb)
        start = time.time()

    #Get pre-query stats
    tb = '"' + tb + '"'
    mean_dist = comp_mean('u_dist', 'c_dist', tb)
    pre_rms = comp_rms('u_dist', 'c_dist', tb)

    for m in mean_dist:
        pre_comp.append(m)
    for p in pre_rms:
        pre_comp.append(p)

    #Grab list of attributes less the annotations; note: annotations end with 'annot' or 'dist' in table structure
    attr_list = c.execute('PRAGMA TABLE_INFO({})'.format(tb))
    attrs = set([tup[1] for tup in attr_list.fetchall() if tup[1].endswith(('annot', 'dist')) == False])

    #Randomized projection queries
    #Code liberally borrowed and adapted from Su Feng
    for i in range(1,10):
        #python doesn't unpack two tuples across multiple vars apparently
        mean, rms = onerun(attrs, n, tb)
        #unpacking
        u_mean, c_mean = mean
        u_rms, c_rms = rms

        trials_res.append([u_mean, c_mean, u_rms, c_rms])
    stats = np.array(trials_res)
    #compute the mean over all trials
    trials_mn = np.mean(stats, axis = 0)
    #write the results out to csv file
    with open(file_name, mode='a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writerow({'Table': tb, 'Pre_U_Mean':str(pre_comp[0]), 'Pre_C_Mean':str(pre_comp[1]), 'Pre_U_RMS':str(pre_comp[2]), 'Pre_C_RMS':str(pre_comp[3]), 'Ave_U_Mean': str(trials_mn[0]), 'Ave_C_Mean':str(trials_mn[1]), 'Ave_U_RMS':str(trials_mn[2]), 'Ave_C_RMS':str(trials_mn[3])
})
    print('Finished another write.')

    counter += 1

    if not do_batch:
        break

conn.close()
