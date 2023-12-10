 SELECT
            CAST(cashflow.dtcashflow AS CHAR) AS dtcashflow,
            CAST(cashflow.tchaflow  AS CHAR)  AS dtchaflow,
            status.description,
            cashflow.check_number,
            cashflow.valueflow,
            cashflow.centsflow,
            cashflow.percentflow,
            cashflow.valuepercentflow,
            cashflow.cents2flow,
            cashflow.valuewire,
            cashflow.totalflow,
            cashflow.totaltopay,
            customer.name
            FROM cashflow
            INNER JOIN customer ON cashflow.fk_idcustomer = customer.idcustomer
            LEFT JOIN status ON cashflow.fk_idstatus = status.idstatus
            WHERE cashflow.dtcashflow BETWEEN '2018-01-01' AND '2018-01-02'