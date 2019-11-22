select l1.tid,s_suppkey,s_name,s_address,s_nationkey,s_phone,s_acctbal,s_comment,
u_s_suppkey,u_s_name,u_s_address,u_s_nationkey,u_s_phone,u_s_acctbal,u_s_comment from
(Select c1.tid,s_suppkey,CASE WHEN o1.w1>1 THEN 0 ELSE 1 END AS u_s_suppkey from
(select tid,s_suppkey from supp_s_suppkey where w1=1) c1 join (select max(w1) as w1,tid from supp_s_suppkey group by tid) o1 on c1.tid=o1.tid) l1
JOIN
(Select c2.tid,s_name,CASE WHEN o2.w1>1 THEN 0 ELSE 1 END AS u_s_name from
(select tid,s_name from supp_s_name where w1=1) c2 join (select max(w1) as w1,tid from supp_s_name group by tid) o2 on c2.tid=o2.tid) l2 on l1.tid=l2.tid
JOIN
(Select c3.tid,s_address,CASE WHEN o3.w1>1 THEN 0 ELSE 1 END AS u_s_address from
(select tid,s_address from supp_s_address where w1=1) c3 join (select max(w1) as w1,tid from supp_s_address group by tid) o3 on c3.tid=o3.tid) l3 on l1.tid=l3.tid
JOIN
(Select c4.tid,s_nationkey,CASE WHEN o4.w1>1 THEN 0 ELSE 1 END AS u_s_nationkey from
(select tid,s_nationkey from supp_s_nationkey where w1=1) c4 join (select max(w1) as w1,tid from supp_s_nationkey group by tid) o4 on c4.tid=o4.tid) l4 on l1.tid=l4.tid
JOIN
(Select c5.tid,s_phone,CASE WHEN o5.w1>1 THEN 0 ELSE 1 END AS u_s_phone from
(select tid,s_phone from supp_s_phone where w1=1) c5 join (select max(w1) as w1,tid from supp_s_phone group by tid) o5 on c5.tid=o5.tid) l5 on l1.tid=l5.tid
JOIN
(Select c6.tid,s_acctbal,CASE WHEN o6.w1>1 THEN 0 ELSE 1 END AS u_s_acctbal from
(select tid,s_acctbal from supp_s_acctbal where w1=1) c6 join (select max(w1) as w1,tid from supp_s_acctbal group by tid) o6 on c6.tid=o6.tid) l6 on l1.tid=l6.tid
JOIN
(Select c7.tid,s_comment,CASE WHEN o7.w1>1 THEN 0 ELSE 1 END AS u_s_comment from
(select tid,s_comment from supp_s_comment where w1=1) c7 join (select max(w1) as w1,tid from supp_s_comment group by tid) o7 on c7.tid=o7.tid) l7 on l1.tid=l7.tid;