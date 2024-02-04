delete from public.pnl_reports where delivery_day = '{{ ds }}';

insert into public.pnl_reports
with source as (
	select 
		delivery_hour
		,delivery_day
		,count(id) as number_of_trades
	    ,sum(
	    	case
		    	when direction = 'sell' then quantity 
		    	else 0 end
		) as total_quantity_sold
	    ,sum(
	    	case
		    	when direction = 'buy' then quantity
		    	else 0 end
		) as total_quantity_bought
	    ,sum(
	    	case 
		    	when direction = 'sell' then quantity * price 
		    	when direction = 'buy' then -quantity * price 
		    	else 0 end
		) as pnl
	from
		trade
	where
		delivery_day = '{{ ds }}'
	group by
		delivery_hour, delivery_day
	order by
		delivery_hour
)
select 
    md5(delivery_hour::varchar || delivery_day::varchar) as id
	,delivery_hour
	,delivery_day
	,number_of_trades
	,total_quantity_sold
	,total_quantity_bought
	,pnl
	,sum(pnl) over() as total_pnl_for_the_day
from source
order by delivery_hour;