SELECT
    -- aux columns
    loan.loan_id,
    loan.date AS loan_date,
    account.date AS acc_date,

    -- loan features
    loan.amount AS loan_amount,
    loan.duration AS loan_duration,

    -- account and client features
    TIMESTAMPDIFF(year, account.date, NOW()) AS acc_age,
    TIMESTAMPDIFF(year, client.birth_date, NOW()) AS client_age,
    client.gender AS client_gender,

    -- district features
    district.A2 AS district_name,
    district.A3 AS district_region,
    district.A4 AS district_inhabitants,
    district.A11 AS district_avg_salary,

    -- target
    CASE
        WHEN loan.status IN ('A', 'C') THEN 0
        WHEN loan.status IN ('B', 'D') THEN 1
    END AS bad_payer
FROM
    loan
LEFT JOIN
    account
ON
    loan.account_id = account.account_id
LEFT JOIN
    disp
ON
    (account.account_id = disp.account_id and disp.type = 'owner')
LEFT JOIN
    client
ON
    disp.client_id = client.client_id
LEFT JOIN
    district
ON
    account.district_id = district.district_id