# Analysis

Real numbers pulled from the mart tables. Canceled and unavailable orders are excluded.

## Revenue by category

The data has a gap worth knowing. 2016 only has 312 orders, basically the first few weeks. The file also cuts off in September 2018, just one order that month. So the real usable range is January 2017 through August 2018.

Comparing the same months across both years, almost every category grew. Two didn't: home_confort stayed flat, and market_place dropped by about half, though it's a small category to begin with. The biggest gainers were health_beauty (up 211%, about €247k to €770k) and watches_gifts (up 243%, about €206k to €708k). bed_bath_table, sports_leisure, and computers_accessories stayed the largest categories in both years, growing steadily rather than spiking.

## Repeat purchases

Only 3.0% of customers placed more than one order (2,854 out of 95,028, counted by the real customer id, not the per-order one). This barely changes by region. Big states like SP, RJ, and MG sit in the same 2.6-3.4% range as smaller ones. Most people here buy once and don't come back.

## Delivery delay and review scores

A clear pattern. Orders delivered early get scores around 4.2-4.3. The moment a delivery is late, scores drop hard, and keep dropping the later it gets.

| Delivery timing | Orders | Avg. score |
|---|---|---|
| 2+ weeks early | 41,866 | 4.32 |
| Early | 46,302 | 4.27 |
| On the estimated day | 1,280 | 4.03 |
| Late, up to a week | 3,600 | 2.71 |
| Late, over a week | 2,782 | 1.70 |

About 6.8% of orders arrive late overall. A few sellers are much worse than that. Among sellers with at least 50 orders, the worst run 17-29% late, two to four times the average. One seller in SP (107 orders) runs 17% late with a 2.39 average score, one of the lowest in the dataset.
