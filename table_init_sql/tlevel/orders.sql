select l1.tid,o_orderkey,o_custkey,o_orderstatus,o_totalprice,o_orderdate,o_orderpriority,o_clerk,o_shippriority,o_comment,
u_o_orderkey,u_o_custkey,u_o_orderstatus,u_o_totalprice,u_o_orderdate,u_o_orderpriority,u_o_clerk,u_o_shippriority,u_o_comment from
(Select c1.tid,o_orderkey,CASE WHEN o1.w1>1 THEN 0 ELSE 1 END AS u_o_orderkey from
(select tid,o_orderkey from orders_o_orderkey where w1=1) c1 join (select max(w1) as w1,tid from orders_o_orderkey group by tid) o1 on c1.tid=o1.tid) l1
JOIN
(Select c2.tid,o_custkey,CASE WHEN o2.w1>1 THEN 0 ELSE 1 END AS u_o_custkey from
(select tid,o_custkey from orders_o_custkey where w1=1) c2 join (select max(w1) as w1,tid from orders_o_custkey group by tid) o2 on c2.tid=o2.tid) l2 on l1.tid=l2.tid
JOIN
(Select c3.tid,o_orderstatus,CASE WHEN o3.w1>1 THEN 0 ELSE 1 END AS u_o_orderstatus from
(select tid,o_orderstatus from orders_o_orderstatus where w1=1) c3 join (select max(w1) as w1,tid from orders_o_orderstatus group by tid) o3 on c3.tid=o3.tid) l3 on l1.tid=l3.tid
JOIN
(Select c4.tid,o_totalprice,CASE WHEN o4.w1>1 THEN 0 ELSE 1 END AS u_o_totalprice from
(select tid,o_totalprice from orders_o_totalprice where w1=1) c4 join (select max(w1) as w1,tid from orders_o_totalprice group by tid) o4 on c4.tid=o4.tid) l4 on l1.tid=l4.tid
JOIN
(Select c5.tid,o_orderdate,CASE WHEN o5.w1>1 THEN 0 ELSE 1 END AS u_o_orderdate from
(select tid,o_orderdate from orders_o_orderdate where w1=1) c5 join (select max(w1) as w1,tid from orders_o_orderdate group by tid) o5 on c5.tid=o5.tid) l5 on l1.tid=l5.tid
JOIN
(Select c6.tid,o_orderpriority,CASE WHEN o6.w1>1 THEN 0 ELSE 1 END AS u_o_orderpriority from
(select tid,o_orderpriority from orders_o_orderpriority where w1=1) c6 join (select max(w1) as w1,tid from orders_o_orderpriority group by tid) o6 on c6.tid=o6.tid) l6 on l1.tid=l6.tid
JOIN
(Select c7.tid,o_clerk,CASE WHEN o7.w1>1 THEN 0 ELSE 1 END AS u_o_clerk from
(select tid,o_clerk from orders_o_clerk where w1=1) c7 join (select max(w1) as w1,tid from orders_o_clerk group by tid) o7 on c7.tid=o7.tid) l7 on l1.tid=l7.tid
JOIN
(Select c8.tid,o_shippriority,CASE WHEN o8.w1>1 THEN 0 ELSE 1 END AS u_o_shippriority from
(select tid,o_shippriority from orders_o_shippriority where w1=1) c8 join (select max(w1) as w1,tid from orders_o_shippriority group by tid) o8 on c8.tid=o8.tid) l8 on l1.tid=l8.tid
JOIN
(Select c9.tid,o_comment,CASE WHEN o9.w1>1 THEN 0 ELSE 1 END AS u_o_comment from
(select tid,o_comment from orders_o_comment where w1=1) c9 join (select max(w1) as w1,tid from orders_o_comment group by tid) o9 on c9.tid=o9.tid) l9 on l1.tid=l9.tid;