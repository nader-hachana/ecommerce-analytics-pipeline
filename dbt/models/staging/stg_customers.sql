-- customer_id is generated per order, not per person; customer_unique_id is the real customer
select
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state

from {{ source('olist_raw', 'olist_customers_dataset') }}
