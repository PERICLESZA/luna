SELECT customer.name, cashflow.fk_idcustomer, count(*) FROM cashflow
INNER JOIN customer ON cashflow.fk_idcustomer = customer.idcustomer
GROUP BY fk_idcustomer
ORDER BY count(*) desc