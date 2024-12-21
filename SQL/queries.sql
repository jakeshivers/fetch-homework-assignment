--What are the top 5 brands by receipts scanned for most recent month?
;with cte as (
    select b.barcode, brand_code, date_scanned::DATE AS date_scanned, count(ri.barcode) num_of_items
    from brands b
    join receipt_items ri
    on b.barcode = ri.barcode
    join receipts r
    on r.receipt_id = ri.receipt_id
    group by b.barcode, brand_code, date_scanned::DATE
    order by date_scanned desc, num_of_items desc
   
)

select *
from cte
limit 5



--When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?

--*** this question is broken as there is not a "accepted" value in the dataset. I'm going to assume "finished" means "accepted"

SELECT 
    reward_receipt_status,
    AVG(total_spent) AS avg_spend
FROM 
    receipts
WHERE 
    reward_receipt_status IN ('FINISHED', 'REJECTED')
GROUP BY 
    reward_receipt_status
ORDER BY 
    avg_spend DESC;


--When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?

--*** this question is broken as there is not a "accepted" value in the dataset. I'm going to assume "finished" means "accepted"
SELECT 
    reward_receipt_status,
    SUM(purchase_item_count) AS total_items_purchased
FROM 
    receipts
WHERE 
    reward_receipt_status IN ('FINISHED', 'REJECTED')
GROUP BY 
    reward_receipt_status
ORDER BY 
    total_items_purchased DESC;


-------------------Which brand has the most spend among users who were created within the past 6 months?
WITH max_user_date AS (
    SELECT 
        MAX(created_date) AS max_created_date
    FROM 
        users
),
recent_users AS (
    SELECT 
        user_id
    FROM 
        users
    WHERE 
        created_date >= (
            SELECT max_created_date - INTERVAL '6 months'
            FROM max_user_date
        )
),
user_receipts AS (
    SELECT 
        r.receipt_id,
        r.total_spent,
        ri.barcode
    FROM 
        receipts r
    JOIN 
        recent_users u ON r.user_id = u.user_id
    JOIN 
        receipt_items ri ON r.receipt_id = ri.receipt_id
),
brand_spend AS (
    SELECT 
        b.name AS brand_name,
        SUM(ur.total_spent) AS total_spend
    FROM 
        user_receipts ur
    JOIN 
        brands b ON ur.barcode = b.barcode
    GROUP BY 
        b.name
)
SELECT 
    brand_name, 
    total_spend
FROM 
    brand_spend
ORDER BY 
    total_spend DESC
LIMIT 1;

-----Which brand has the most transactions among users who were created within the past 6 months?
WITH max_user_date AS (
    SELECT 
        MAX(created_date) AS max_created_date
    FROM 
        users
),
recent_users AS (
    SELECT 
        user_id
    FROM 
        users
    WHERE 
        created_date >= (
            SELECT max_created_date - INTERVAL '6 months'
            FROM max_user_date
        )
),
user_transactions AS (
    SELECT 
        ri.barcode,
        COUNT(r.receipt_id) AS transaction_count
    FROM 
        receipts r
    JOIN 
        recent_users u ON r.user_id = u.user_id
    JOIN 
        receipt_items ri ON r.receipt_id = ri.receipt_id
    GROUP BY 
        ri.barcode
),
brand_transactions AS (
    SELECT 
        b.name AS brand_name,
        SUM(ut.transaction_count) AS total_transactions
    FROM 
        user_transactions ut
    JOIN 
        brands b ON ut.barcode = b.barcode
    GROUP BY 
        b.name
)
SELECT 
    brand_name, 
    total_transactions
FROM 
    brand_transactions
ORDER BY 
    total_transactions DESC
LIMIT 1;
