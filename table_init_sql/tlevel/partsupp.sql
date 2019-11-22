select l1.tid,ps_partkey,ps_suppkey,ps_availqty,ps_supplycost,ps_comment,
u_ps_partkey,u_ps_suppkey,u_ps_availqty,u_ps_supplycost,u_ps_comment from
(Select c1.tid,ps_partkey,CASE WHEN o1.w1>1 THEN 0 ELSE 1 END AS u_ps_partkey from
(select tid,ps_partkey from psupp_ps_partkey where w1=1) c1 join (select max(w1) as w1,tid from psupp_ps_partkey group by tid) o1 on c1.tid=o1.tid) l1
JOIN
(Select c2.tid,ps_suppkey,CASE WHEN o2.w1>1 THEN 0 ELSE 1 END AS u_ps_suppkey from
(select tid,ps_suppkey from psupp_ps_suppkey where w1=1) c2 join (select max(w1) as w1,tid from psupp_ps_suppkey group by tid) o2 on c2.tid=o2.tid) l2 on l1.tid=l2.tid
JOIN
(Select c3.tid,ps_availqty,CASE WHEN o3.w1>1 THEN 0 ELSE 1 END AS u_ps_availqty from
(select tid,ps_availqty from psupp_ps_availqty where w1=1) c3 join (select max(w1) as w1,tid from psupp_ps_availqty group by tid) o3 on c3.tid=o3.tid) l3 on l1.tid=l3.tid
JOIN
(Select c4.tid,ps_supplycost,CASE WHEN o4.w1>1 THEN 0 ELSE 1 END AS u_ps_supplycost from
(select tid,ps_supplycost from psupp_ps_supplycost where w1=1) c4 join (select max(w1) as w1,tid from psupp_ps_supplycost group by tid) o4 on c4.tid=o4.tid) l4 on l1.tid=l4.tid
JOIN
(Select c5.tid,ps_comment,CASE WHEN o5.w1>1 THEN 0 ELSE 1 END AS u_ps_comment from
(select tid,ps_comment from psupp_ps_comment where w1=1) c5 join (select max(w1) as w1,tid from psupp_ps_comment group by tid) o5 on c5.tid=o5.tid) l5 on l1.tid=l5.tid;