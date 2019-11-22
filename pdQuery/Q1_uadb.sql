select o_orderkey,o_orderdate,o_shippriority,least(b1.u_r,b2.u_r) AS u_r from
(select o_orderkey,o_orderdate,o_shippriority,least(a1.u_r,a2.u_r) AS u_r from 
(select c_custkey,u_r from customer_uadb where c_mktsegment = 'BUILDING') a1
JOIN
(select o_orderkey,o_orderdate,o_shippriority,o_custkey, u_r from orders_uadb where to_date(o_orderdate,'yyyy-mm-dd') > to_date('1995-03-15','yyyy-mm-dd')) a2 ON c_custkey = o_custkey) b1
JOIN
(select l_orderkey,l_shipdate,u_r from lineitem_uadb where to_date(l_shipdate,'yyyy-mm-dd') < to_date('1995-03-17','yyyy-mm-dd')) b2
ON o_orderkey = l_orderkey;