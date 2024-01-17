SELECT last_name, COUNT(last_name) AS Frequency

FROM
	employees
GROUP BY
	last_name
ORDER BY
	Frequency desc;