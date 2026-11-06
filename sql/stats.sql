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