-- late rate on shipped orders
select round(count(*) filter( where days_shipping_real > days_shipping_scheduled)*100.0/ count(*),1) 
as late_pct from orders where delivery_status <> 'Shipping canceled';

-- delivery-status breakdown
SELECT delivery_status,
       COUNT(*) AS total,
       COUNT(*) FILTER (WHERE late_delivery_risk) AS flagged_late,
       COUNT(*) FILTER (WHERE days_shipping_real > days_shipping_scheduled) AS actually_late
FROM orders
GROUP BY delivery_status;

-- Late rate by shipping mode (shipped orders only)
-- Finding: First Class is late 100% of the time; Standard Class is the most reliable at 39.8%
SELECT shipping_mode,
       COUNT(*) AS items,
       ROUND(COUNT(*) FILTER (WHERE days_shipping_real > days_shipping_scheduled) * 100.0 / COUNT(*), 1) AS late_pct
FROM orders
WHERE delivery_status <> 'Shipping canceled'
GROUP BY shipping_mode
ORDER BY late_pct DESC;

--First Class’s 100% late rate is a dataset
select days_shipping_scheduled, days_shipping_real, count(*) 
from orders where shipping_mode = 'First Class' and delivery_status <> 'Shipping canceled' 
group by days_shipping_scheduled, days_shipping_real; 

--late rate by region.
select order_region, count(*) as Items, round(count(*) filter (where days_shipping_real > days_shipping_scheduled) * 100.0 / COUNT(*), 1) AS late_pct 
 from  orders where delivery_status <> 'Shipping canceled'  
 group by order_region order by  late_pct DESC; 