select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

with all_values as (

    select
        result as value_field,
        count(*) as n_records

    from `chessthesis`.`chess_thesis`.`twicgames`
    group by result

)

select *
from all_values
where value_field not in (
    '1-0','0-1','1/2-1/2'
)



      
    ) dbt_internal_test