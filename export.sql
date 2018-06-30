\c bubble_tea;
\copy (SELECT * FROM bubble_tea_w_fips) TO './csv/bubble_tea.csv';
\copy (SELECT * FROM bubble_tea_w_hours) TO './csv/hours.csv';