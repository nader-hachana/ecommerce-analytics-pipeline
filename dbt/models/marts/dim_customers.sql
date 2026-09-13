-- grain: one row per customer_unique_id (the real person, not the per-order customer_id).
-- 122 customers have more than one recorded location; this keeps the location tied to
-- their most recent order rather than picking one arbitrarily.

with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

ranked as (
    select
        c.customer_unique_id,
        c.customer_zip_code_prefix,
        c.customer_city,
        c.customer_state,
        o.order_purchase_timestamp,
        row_number() over (
            partition by c.customer_unique_id
            order by o.order_purchase_timestamp desc
        ) as rn
    from customers c
    left join orders o on c.customer_id = o.customer_id
)

select
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
from ranked
where rn = 1
