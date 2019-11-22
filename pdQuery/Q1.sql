SELECT o_orderkey, o_orderdate, o_shippriority FROM customer_bg c, orders_bg o, lineitem_bg l WHERE to_date(o_orderdate,'yyyy-mm-dd') > to_date('1995-03-15','yyyy-mm-dd') AND to_date(l_shipdate,'yyyy-mm-dd') < to_date('1995-03-17','yyyy-mm-dd') AND c_mktsegment = 'BUILDING' AND c_custkey = o_custkey AND o_orderkey = l_orderkey;