select l1.tid,l_orderkey,l_partkey,l_suppkey,l_linenumber,l_quantity,l_extendedprice,l_discount,l_tax,l_returnflag,l_linestatus,l_shipdate,l_commitdate,l_receiptdate,l_shipinstruct,l_shipmode,l_comment, 
u_l_orderkey,u_l_partkey,u_l_suppkey,u_l_linenumber,u_l_quantity,u_l_extendedprice,u_l_discount,u_l_tax,u_l_returnflag,u_l_linestatus,u_l_shipdate,u_l_commitdate,u_l_receiptdate,u_l_shipinstruct,u_l_shipmode,u_l_comment from
(Select c1.tid,l_orderkey,CASE WHEN o1.w1>1 THEN 0 ELSE 1 END AS u_l_orderkey from
(select tid,l_orderkey from lineitem_l_orderkey where w1=1) c1 join (select max(w1) as w1,tid from lineitem_l_orderkey group by tid) o1 on c1.tid=o1.tid) l1
JOIN
(Select c2.tid,l_partkey,CASE WHEN o2.w1>1 THEN 0 ELSE 1 END AS u_l_partkey from
(select tid,l_partkey from lineitem_l_partkey where w1=1) c2 join (select max(w1) as w1,tid from lineitem_l_partkey group by tid) o2 on c2.tid=o2.tid) l2 on l1.tid=l2.tid 
JOIN
(Select c3.tid,l_suppkey,CASE WHEN o3.w1>1 THEN 0 ELSE 1 END AS u_l_suppkey from
(select tid,l_suppkey from lineitem_l_suppkey where w1=1) c3 join (select max(w1) as w1,tid from lineitem_l_suppkey group by tid) o3 on c3.tid=o3.tid) l3 on l1.tid=l3.tid
JOIN
(Select c4.tid,l_linenumber,CASE WHEN o4.w1>1 THEN 0 ELSE 1 END AS u_l_linenumber from
(select tid,l_linenumber from lineitem_l_linenumber where w1=1) c4 join (select max(w1) as w1,tid from lineitem_l_linenumber group by tid) o4 on c4.tid=o4.tid) l4 on l1.tid=l4.tid 
JOIN
(Select c5.tid,l_quantity,CASE WHEN o5.w1>1 THEN 0 ELSE 1 END AS u_l_quantity from
(select tid,l_quantity from lineitem_l_quantity where w1=1) c5 join (select max(w1) as w1,tid from lineitem_l_quantity group by tid) o5 on c5.tid=o5.tid) l5 on l1.tid=l5.tid 
JOIN
(Select c6.tid,l_extendedprice,CASE WHEN o6.w1>1 THEN 0 ELSE 1 END AS u_l_extendedprice from
(select tid,l_extendedprice from lineitem_l_extendedprice where w1=1) c6 join (select max(w1) as w1,tid from lineitem_l_extendedprice group by tid) o6 on c6.tid=o6.tid) l6 on l1.tid=l6.tid 
JOIN
(Select c7.tid,l_discount,CASE WHEN o7.w1>1 THEN 0 ELSE 1 END AS u_l_discount from
(select tid,l_discount from lineitem_l_discount where w1=1) c7 join (select max(w1) as w1,tid from lineitem_l_discount group by tid) o7 on c7.tid=o7.tid) l7 on l1.tid=l7.tid 
JOIN
(Select c8.tid,l_tax,CASE WHEN o8.w1>1 THEN 0 ELSE 1 END AS u_l_tax from
(select tid,l_tax from lineitem_l_tax where w1=1) c8 join (select max(w1) as w1,tid from lineitem_l_tax group by tid) o8 on c8.tid=o8.tid) l8 on l1.tid=l8.tid 
JOIN
(Select c9.tid,l_returnflag,CASE WHEN o9.w1>1 THEN 0 ELSE 1 END AS u_l_returnflag from
(select tid,l_returnflag from lineitem_l_returnflag where w1=1) c9 join (select max(w1) as w1,tid from lineitem_l_returnflag group by tid) o9 on c9.tid=o9.tid) l9 on l1.tid=l9.tid 
JOIN
(Select c10.tid,l_linestatus,CASE WHEN o10.w1>1 THEN 0 ELSE 1 END AS u_l_linestatus from
(select tid,l_linestatus from lineitem_l_linestatus where w1=1) c10 join (select max(w1) as w1,tid from lineitem_l_linestatus group by tid) o10 on c10.tid=o10.tid) l10 on l1.tid=l10.tid 
JOIN
(Select c11.tid,l_shipdate,CASE WHEN o11.w1>1 THEN 0 ELSE 1 END AS u_l_shipdate from
(select tid,l_shipdate from lineitem_l_shipdate where w1=1) c11 join (select max(w1) as w1,tid from lineitem_l_shipdate group by tid) o11 on c11.tid=o11.tid) l11 on l1.tid=l11.tid 
JOIN
(Select c12.tid,l_commitdate,CASE WHEN o12.w1>1 THEN 0 ELSE 1 END AS u_l_commitdate from
(select tid,l_commitdate from lineitem_l_commitdate where w1=1) c12 join (select max(w1) as w1,tid from lineitem_l_commitdate group by tid) o12 on c12.tid=o12.tid) l12 on l1.tid=l12.tid 
JOIN
(Select c13.tid,l_receiptdate,CASE WHEN o13.w1>1 THEN 0 ELSE 1 END AS u_l_receiptdate from
(select tid,l_receiptdate from lineitem_l_receiptdate where w1=1) c13 join (select max(w1) as w1,tid from lineitem_l_receiptdate group by tid) o13 on c13.tid=o13.tid) l13 on l1.tid=l13.tid 
JOIN
(Select c14.tid,l_shipinstruct,CASE WHEN o14.w1>1 THEN 0 ELSE 1 END AS u_l_shipinstruct from
(select tid,l_shipinstruct from lineitem_l_shipinstruct where w1=1) c14 join (select max(w1) as w1,tid from lineitem_l_shipinstruct group by tid) o14 on c14.tid=o14.tid) l14 on l1.tid=l14.tid 
JOIN
(Select c15.tid,l_shipmode,CASE WHEN o15.w1>1 THEN 0 ELSE 1 END AS u_l_shipmode from
(select tid,l_shipmode from lineitem_l_shipmode where w1=1) c15 join (select max(w1) as w1,tid from lineitem_l_shipmode group by tid) o15 on c15.tid=o15.tid) l15 on l1.tid=l15.tid 
JOIN
(Select c16.tid,l_comment,CASE WHEN o16.w1>1 THEN 0 ELSE 1 END AS u_l_comment from
(select tid,l_comment from lineitem_l_comment where w1=1) c16 join (select max(w1) as w1,tid from lineitem_l_comment group by tid) o16 on c16.tid=o16.tid) l16 on l1.tid=l16.tid;