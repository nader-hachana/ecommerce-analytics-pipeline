-- grain: one row per order line item (order_id, order_item_id).
-- order_total_payment_value and review_score are order-level attributes repeated across
-- every item in the same order, sum(price) or sum(price + freight_value) is the right way
-- to get item-level revenue, don't sum order_total_payment_value across an order's items.

with order_items as (
    select * from {{ ref('stg_order_items') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

-- an order can have multiple payment rows (split payments), aggregate to one row per order first
payments_per_order as (
    select
        order_id,
        sum(payment_value) as order_total_payment_value,
        count(*) as order_payment_count
    from {{ ref('stg_order_payments') }}
    group by order_id
),

primary_payment_type as (
    select order_id, payment_type
    from {{ ref('stg_order_payments') }}
    qualify row_number() over (partition by order_id order by payment_value desc) = 1
),

-- an order can have more than one review, keep the most recently answered one
latest_review as (
    select order_id, review_score
    from {{ ref('stg_order_reviews') }}
    qualify row_number() over (
        partition by order_id
        order by review_answer_timestamp desc, review_creation_date desc
    ) = 1
)

select
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    c.customer_unique_id,

    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    date_diff(
        date(o.order_delivered_customer_date),
        date(o.order_estimated_delivery_date),
        day
    ) as delivery_delay_days,

    oi.price,
    oi.freight_value,

    pp.order_total_payment_value,
    pp.order_payment_count,
    ppt.payment_type as order_primary_payment_type,

    lr.review_score

from order_items oi
left join orders o on oi.order_id = o.order_id
left join customers c on o.customer_id = c.customer_id
left join payments_per_order pp on oi.order_id = pp.order_id
left join primary_payment_type ppt on oi.order_id = ppt.order_id
left join latest_review lr on oi.order_id = lr.order_id
