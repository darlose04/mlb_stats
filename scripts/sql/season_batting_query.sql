select player_id,
       season,
       name,
       link,
       team_id,
       games,
       flyouts,
       groundouts,
       airouts,
       runs,
       rbi,
       singles,
       doubles,
       triples,
       homeruns,
       strikeouts,
       walks,
       intentional_walks,
       hits,
       hbp,
       at_bats,
       plate_appearances,
       round(avg, 3)       avg,
       round(obp, 3)       obp,
       round(slg, 3)       slg,
       round(obp + slg, 3) ops,
       round(slg - avg, 3) iso,
       round(bb_perc, 3)   bb_perc,
       round(k_perc, 3)    k_perc,
       round(bb_per_k, 3)  bb_per_k,
       round(babip, 3)     babip,
       caught_stealing,
       stolen_bases,
       gidp,
       gitp,
       total_bases,
       lob,
       sac_bunts,
       sac_flies,
       catchers_int,
       pickoffs,
       popouts,
       lineouts
from (select player_id,
             season,
             name,
             link,
             team_id,
             count(*)               as games,
             sum(flyouts)           as flyouts,
             sum(groundouts)        as groundouts,
             sum(airouts)           as airouts,
             sum(runs)              as runs,
             sum(rbi)               as rbi,
             sum(singles)           as singles,
             sum(doubles)           as doubles,
             sum(triples)           as triples,
             sum(homeruns)          as homeruns,
             sum(strikeouts)        as strikeouts,
             sum(walks)             as walks,
             sum(intentional_walks) as intentional_walks,
             sum(hits)              as hits,
             sum(hbp)               as hbp,
             sum(at_bats)           as at_bats,
             sum(plate_appearances) as plate_appearances,
             case
                 when (sum(at_bats) > 0) then sum(hits)::numeric / sum(at_bats)
                 else null
                 end                as avg,
             case
                 when (sum(at_bats) + sum(walks) + sum(hbp) + sum(sac_flies)) > 0 then
                     (sum(hits) + sum(walks) + sum(hbp))::numeric /
                     (sum(at_bats) + sum(walks) + sum(hbp) + sum(sac_flies))
                 else null
                 end                as obp,
             case
                 when sum(at_bats) > 0 then
                     (sum(singles) + (sum(doubles) * 2) + (sum(triples) * 3) + (sum(homeruns) * 4))::numeric /
                     sum(at_bats)
                 else null end      as slg,
             -- ops calculate outside
             -- iso calculate outside
             case
                 when sum(plate_appearances) > 0 then sum(walks)::numeric / sum(plate_appearances)
                 else null end      as bb_perc,
             case
                 when sum(plate_appearances) > 0 then sum(strikeouts)::numeric / sum(plate_appearances)
                 else null end      as k_perc,
             case
                 when sum(strikeouts) > 0 then sum(walks)::numeric / sum(strikeouts)
                 when sum(walks) > 0 then 'Infinity'::numeric
                 else null end      as bb_per_k,
             case
                 when (sum(at_bats) - sum(strikeouts) - sum(homeruns) + sum(sac_flies)) > 0 then
                     (sum(hits) - sum(homeruns))::numeric /
                     (sum(at_bats) - sum(strikeouts) - sum(homeruns) + sum(sac_flies))
                 else null end      as babip,
             sum(caught_stealing)   as caught_stealing,
             sum(stolen_bases)      as stolen_bases,
             sum(gidp)              as gidp,
             sum(gitp)              as gitp,
             sum(total_bases)       as total_bases,
             sum(lob)               as lob,
             sum(sac_bunts)         as sac_bunts,
             sum(sac_flies)         as sac_flies,
             sum(catchers_int)      as catchers_int,
             sum(pickoffs)          as pickoffs,
             sum(popouts)           as popouts,
             sum(lineouts)          as lineouts
      from games g
               inner join player_batting pb on g.id = pb.game_id
      group by season, player_id, name, link, team_id)
