#!/usr/bin/python
import sqlite3
import numpy as np
from sqlite3 import OperationalError
import random
import sys

#db
db = 'dbs/bags.db'
#table
tbs=['buffalo2','foodins2','permits2']
#tb = 'foodins2'
#tb = 'permits2'
#attribute list

attrs = [set(["lat","lon","orig order_shooting","CD as number_shooting","CD_shooting","Date_shooting","Time_shooting","WeekNum_shooting","Month_shooting","Day_shooting","Hour_shooting","Year_shooting","city","state","Location_shooting","find space_shooting","street_shooting","District_shooting","Type_shooting","Victims_shooting","index"]), set(["Inspection ID","DBA Name","AKA Name","License #","Risk","Address","City","State","Zip","Inspection Date","Inspection Type","Results","Latitude","Longitude"]), set(["Permit Number","Permit Type","Permit Type Definition","Permit Creation Date","Block","Lot","Street Number","Street Name","Street Suffix","Description","Current Status","Current Status Date","Filed Date","Supervisor District","Neighborhoods - Analysis Boundaries","Zipcode","Location","Record ID"])]

#sample size
#result size
#ressize = 0

def runquery(q):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    result = c.execute(q)
    conn.commit()
    row = result.fetchall()[0]
    return row[0]

def onerun(attrs, n, i):
    rd = random.sample(attrs, n)
    urd = ["U_"+itm for itm in rd]
    #print("random chosen attrs: ", rd)

    casestr = " AND ".join(['"'+it+'"'+"='t'" for it in urd])
    casestr = ", CASE WHEN " + casestr + " THEN '1' ELSE '0' END AS CL"
    str = '","'.join(rd)
    gpb = '"'+ str + '"'
    str = '"'+ str + '"' + casestr + ',OL'
    
    #wstrfn = " AND ".join(['"'+it+'"'+"='t'" for it in urd]) + " AND U_R='f'"
    #wstrtp = " AND ".join(['"'+it+'"'+"='t'" for it in urd]) + " AND U_R='t'"
    #wstrfp = "(" + " OR ".join(['"'+it+'"'+"='f'" for it in urd]) + ") AND U_R='f'"
    
    command = "select avg((CL-OL)*1.0/CL) AS rate from (select %s, sum(OL) AS OL, sum(CL) AS CL from (select %s from %s) GROUP BY %s);" % (gpb,str,tbs[i], gpb)
    #print(command)
    #command = "insert into R values ('8','9','f','f','f');"
    fn = runquery(command)

    return fn

#all = runquery("select count(*) from %s;" % (tb))
def allrun():
    n = max([len(attr) for attr in attrs])
    result = {}
    for i in range (1,n+1,2):
        result[i] = "%d"%i
    for k in range (0,len(attrs)):
        attr = attrs[k]
        nl = len(attr)
        print(nl)
        rez=[]
        j = 0
        for j in range (1,nl+1,2):
#for j in range (1,2):
            print(j,end="\r")
            for i in range(1,20):
                rt = onerun(attr, j, k)
                rez.append(rt)
            result[j] += "\t" + '{0:.12f}'.format(np.mean(rez))
            rez = []
        for x in range (j+2, n+1, 2):
            result[x] += "\t" + '{0:.12f}'.format(0.0)
        print()
    res = "\tbuffalo\t\tfoodins\t\tpermits"
    for i in range (1,n+1,2):
        res += "\n" + result[i]
    return res
#print('{0:.12f}'.format((np.mean(rez)))
