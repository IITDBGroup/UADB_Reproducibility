select l1.tid,p_partkey,p_name,p_mfgr,p_brand,p_type,p_size,p_container,p_retailprice,p_comment,
u_p_partkey,u_p_name,u_p_mfgr,u_p_brand,u_p_type,u_p_size,u_p_container,u_p_retailprice,u_p_comment from
(Select c1.tid,p_partkey,CASE WHEN o1.w1>1 THEN 0 ELSE 1 END AS u_p_partkey from
(select tid,p_partkey from part_p_partkey where w1=1) c1 join (select max(w1) as w1,tid from part_p_partkey group by tid) o1 on c1.tid=o1.tid) l1
JOIN
(Select c2.tid,p_name,CASE WHEN o2.w1>1 THEN 0 ELSE 1 END AS u_p_name from
(select tid,p_name from part_p_name where w1=1) c2 join (select max(w1) as w1,tid from part_p_name group by tid) o2 on c2.tid=o2.tid) l2 on l1.tid=l2.tid
JOIN
(Select c3.tid,p_mfgr,CASE WHEN o3.w1>1 THEN 0 ELSE 1 END AS u_p_mfgr from
(select tid,p_mfgr from part_p_mfgr where w1=1) c3 join (select max(w1) as w1,tid from part_p_mfgr group by tid) o3 on c3.tid=o3.tid) l3 on l1.tid=l3.tid
JOIN
(Select c4.tid,p_brand,CASE WHEN o4.w1>1 THEN 0 ELSE 1 END AS u_p_brand from
(select tid,p_brand from part_p_brand where w1=1) c4 join (select max(w1) as w1,tid from part_p_brand group by tid) o4 on c4.tid=o4.tid) l4 on l1.tid=l4.tid
JOIN
(Select c5.tid,p_type,CASE WHEN o5.w1>1 THEN 0 ELSE 1 END AS u_p_type from
(select tid,p_type from part_p_type where w1=1) c5 join (select max(w1) as w1,tid from part_p_type group by tid) o5 on c5.tid=o5.tid) l5 on l1.tid=l5.tid
JOIN
(Select c6.tid,p_size,CASE WHEN o6.w1>1 THEN 0 ELSE 1 END AS u_p_size from
(select tid,p_size from part_p_size where w1=1) c6 join (select max(w1) as w1,tid from part_p_size group by tid) o6 on c6.tid=o6.tid) l6 on l1.tid=l6.tid
JOIN
(Select c7.tid,p_container,CASE WHEN o7.w1>1 THEN 0 ELSE 1 END AS u_p_container from
(select tid,p_container from part_p_container where w1=1) c7 join (select max(w1) as w1,tid from part_p_container group by tid) o7 on c7.tid=o7.tid) l7 on l1.tid=l7.tid
JOIN
(Select c8.tid,p_retailprice,CASE WHEN o8.w1>1 THEN 0 ELSE 1 END AS u_p_retailprice from
(select tid,p_retailprice from part_p_retailprice where w1=1) c8 join (select max(w1) as w1,tid from part_p_retailprice group by tid) o8 on c8.tid=o8.tid) l8 on l1.tid=l8.tid
JOIN
(Select c9.tid,p_comment,CASE WHEN o9.w1>1 THEN 0 ELSE 1 END AS u_p_comment from
(select tid,p_comment from part_p_comment where w1=1) c9 join (select max(w1) as w1,tid from part_p_comment group by tid) o9 on c9.tid=o9.tid) l9 on l1.tid=l9.tid;