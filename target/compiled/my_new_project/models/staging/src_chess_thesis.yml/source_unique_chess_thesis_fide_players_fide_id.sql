
    
    

with dbt_test__target as (
  
  select fide_id as unique_field
  from `chessthesis`.`chess_thesis`.`fide_players`
  where fide_id is not null
  
)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


