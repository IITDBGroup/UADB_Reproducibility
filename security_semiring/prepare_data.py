import sqlite3


db = 'test.db'
#tb = 'food_inspec'
#prefix of all prepared tables used in security semiring testing
#pre = 'sec_'
#Experiment has changed to control two probability counters, the first: best_guess != actual, the second c_label != actual
#pre = ['one_one', 'one_five', 'one_ten', 'one_fifteen', 'five_one', 'five_five', 'five_fifteen', 'ten_one', \
#    'ten_five', 'ten_ten', 'ten_fifteen']

#pre = [i + '_sec' for i in pre]
#probability measures for situation 1
pr1 = [1, 5, 10]
#probability measures for situation 2
pr2 = [1, 5, 10, 15]
perc =[(i, j) for i in pr1 for j in pr2]
#percents = [99, 95 90, 85]
#five value mappings in security semiring: P < C < S < T < 0 (note this is the reverse of the natural order)
#mod_sec = 5

#cols = ['c_annot', 'r_annot', 'u_annot', 'u_dist', 'c_dist']
#query = 'CREATE TABLE '

#set up connection
conn = sqlite3.connect(db)
c = conn.cursor()
#run the script on one hard-coded table
no_batch = True


def drop_tb():
    result = c.execute('select name from sqlite_master where type = "table";')
    d_tbs = [i[0] for i in result if i[0][0].isdigit()]
    if len(d_tbs) != 0:
        for tb in d_tbs:
            c.execute('drop table "' + tb + '";')
            conn.commit()
if no_batch:
    #for trial runs, we need to drop the created tables before running again (assuming we are using the same tb in each trial)
    #drop_tb()
    tbs = ['graf_rmv']
else:
    q_tb = 'SELECT name from sqlite_master WHERE type = "table";'
    tbs = [row[0] for row in c.execute(q_tb) if not row[0][0].isdigit()]
    print(tbs)

for t in tbs:
    for p in perc:
        pre = ''.join([str(i) for i in p]) + '_sec_'
        final = '"' + pre + t + '"'
        #names of in between tables used to populate attributes with random values, which are correlated
        iter = ['iter1', 'iter2', 'iter3', final]
        #recall by the encoding, that we have the following relationship between labels: u \leq r \leq c
        for i in range(0, len(iter)):
            #build certain random annotation values
            if i == 0:
                query = 'CREATE TABLE '+ iter[i] + ' AS SELECT *, abs(Random() % 5) as u_label FROM ' + t + ';'
                c.execute(query)
                conn.commit()
            #build real (actual) random annotation values
            elif i == 1:
                query = 'CREATE TABLE ' + iter[i] + \
                    ' AS SELECT *, case when (abs(random() % 100) < ' + str(100 - p[0]) + ') OR (u_label = 0) then u_label else abs(random() % u_label) end as actual from ' + iter[i - 1] + ';'
                c.execute(query)
                d_query = 'DROP TABLE ' + iter[i - 1]+';'
                c.execute(d_query)
                conn.commit()
            #build uncertain random annotation values
            elif i == 2:
                query = 'CREATE TABLE '+ iter[i] + \
                ' AS SELECT *, case when (abs(random() % 100) < ' + str(100 - p[1]) + ') OR (actual = 0) then actual else abs(random() % actual) end as c_label from ' + iter[i - 1] + ';'
                c.execute(query)
                d_query = 'DROP TABLE ' + iter[i - 1] + ';'
                c.execute(d_query)
                conn.commit()

            elif i == 3:
                query = 'CREATE TABLE ' + iter[i] + \
                    ' AS SELECT *, u_label - actual as u_dist, actual - c_label as c_dist from ' + iter[i - 1] + ';'
                c.execute(query)
                d_query = 'DROP TABLE ' + iter[i - 1] + ';'
                c.execute(d_query)
                conn.commit()

        #test if it's working
        c.execute('select u_label, actual, c_label, u_dist, c_dist from' + final + ' limit 30;')
        print('\n' + final)
        for tup in c.fetchall():
            print(tup)
