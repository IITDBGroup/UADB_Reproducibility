select l1.tid,c_custkey,c_name,c_address,c_nationkey,c_phone,c_acctbal,c_mktsegment,c_comment,u_c_custkey,u_c_name,u_c_address,u_c_nationkey,u_c_phone,u_c_acctbal,u_c_mktsegment,u_c_comment from 
(Select c1.tid,c_custkey,CASE WHEN o1.w1>1 THEN 0 ELSE 1 END AS u_c_custkey from 
(select tid,c_custkey from cust_c_custkey where w1=1) c1 join (select max(w1) as w1,tid from cust_c_custkey group by tid) o1 on c1.tid=o1.tid) l1
JOIN
(Select c2.tid,c_name,CASE WHEN o2.w1>1 THEN 0 ELSE 1 END AS u_c_name from 
(select tid,c_name from cust_c_name where w1=1) c2  join (select max(w1) as w1,tid from cust_c_name group by tid) o2 on c2.tid=o2.tid) l2 on l1.tid=l2.tid
JOIN
(Select c3.tid,c_address,CASE WHEN o3.w1>1 THEN 0 ELSE 1 END AS u_c_address from
(select tid,c_address from cust_c_address where w1=1) c3 join (select max(w1) as w1,tid from cust_c_address group by tid) o3 on c3.tid=o3.tid) l3 on l1.tid=l3.tid
JOIN
(Select c4.tid,c_nationkey,CASE WHEN o4.w1>1 THEN 0 ELSE 1 END AS u_c_nationkey from
(select tid,c_nationkey from cust_c_nationkey where w1=1) c4 join (select max(w1) as w1,tid from cust_c_nationkey group by tid) o4 on c4.tid=o4.tid) l4 on l1.tid=l4.tid
JOIN
(Select c5.tid,c_phone,CASE WHEN o5.w1>1 THEN 0 ELSE 1 END AS u_c_phone from
(select tid,c_phone from cust_c_phone where w1=1) c5 join (select max(w1) as w1,tid from cust_c_phone group by tid) o5 on c5.tid=o5.tid) l5 on l1.tid=l5.tid
JOIN
(Select c6.tid,c_acctbal,CASE WHEN o6.w1>1 THEN 0 ELSE 1 END AS u_c_acctbal from
(select tid,c_acctbal from cust_c_acctbal where w1=1) c6 join (select max(w1) as w1,tid from cust_c_acctbal group by tid) o6 on c6.tid=o6.tid) l6 on l1.tid=l6.tid
JOIN
(Select c7.tid,c_mktsegment,CASE WHEN o7.w1>1 THEN 0 ELSE 1 END AS u_c_mktsegment from
(select tid,c_mktsegment from cust_c_mktsegment where w1=1) c7 join (select max(w1) as w1,tid from cust_c_mktsegment group by tid) o7 on c7.tid=o7.tid) l7 on l1.tid=l7.tid
JOIN
(Select c8.tid,c_comment,CASE WHEN o8.w1>1 THEN 0 ELSE 1 END AS u_c_comment from
(select tid,c_comment from cust_c_comment where w1=1) c8 join (select max(w1) as w1,tid from cust_c_comment group by tid) o8 on c8.tid=o8.tid) l8 on l1.tid=l8.tid;