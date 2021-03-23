SELECT
    -- district features. Reference for translation: https://sorry.vse.cz/~berka/challenge/pkdd1999/berka.htm
    DISTINCT district_id,
    A2 AS district_name,
    A3 AS district_region,
    CONCAT(district.A2, ' (', district.A3, ')') AS district_name_region,
    A4 AS district_inhabitants,
    A10 AS district_urban_ratio,
    A11 AS district_avg_salary,
    A13 AS district_unemployment_rate,
    A14 AS district_enterpreneurs_per_thousand_inhabitants,
    1000 * A16 / A4 AS district_crimes_per_thousand_inhabitants
FROM
    district
ORDER BY
    district_id
