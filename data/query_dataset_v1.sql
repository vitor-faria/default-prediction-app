SELECT
    -- aux columns
    loan.loan_id,
    loan.date AS loan_date,
    account.date AS account_date,

    -- loan features
    loan.amount AS loan_amount,
    loan.duration AS loan_duration,

    -- account, card and client features
    TIMESTAMPDIFF(month, account.date, loan.date) AS account_age_at_loan_months,
    TIMESTAMPDIFF(year, client.birth_date, loan.date) AS client_age_at_loan_years,
    COALESCE(card.type, 'no card') AS card_type,
    CASE
        WHEN card.card_id IS NULL THEN 0
        ELSE 1
    END AS has_card,

    -- district features. Reference for translation: https://sorry.vse.cz/~berka/challenge/pkdd1999/berka.htm
    CONCAT(district.A2, ' (', district.A3, ')') AS district_name_region,
    district.A4 AS district_inhabitants,
    district.A10 AS district_urban_ratio,
    district.A11 AS district_avg_salary,
    district.A13 AS district_unemployment_rate,
    district.A14 AS district_enterpreneurs_per_thousand_inhabitants,
    1000 * district.A16 / district.A4 AS district_crimes_per_thousand_inhabitants,
    (loan.amount / loan.duration) / district.A11 AS loan_salary_ratio,

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
LEFT JOIN
    card
ON
    disp.disp_id = card.disp_id AND card.issued <= loan.date
ORDER BY
    loan_id
