-- Finding: demand is stable at 11–12K units/month from Jan 2015 to Sep 2017.
-- From Oct 2017, items drop ~60%, categories shrink from 24 to 8–14,
-- and from Nov 2017 every item has quantity 1. Treat Oct 2017 onward as a recording change;
-- forecast on Jan 2015 – Sep 2017 only.

--total quantity ordered in each month, in date order
select DATE_TRUNC('month', order_date) AS Month, Sum(quantity) as Units from orders group by month order by month;

--the number of order items and the number of distinct categories for each month, in date order
select DATE_TRUNC('month', order_date) AS Month, count(order_item_id) as Items, COUNT(DISTINCT category_name) as Category from orders group by month order by month;