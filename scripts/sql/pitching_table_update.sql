select player_id::text || '_' || team_id::text || '_' || season::text as player_team_season_id,
       player_id,
       season,
       link,
       team_id,
       sum(starts)                                                    as starts,
       sum(appearances)                                               as appearances,
       sum(flyouts)                                                   as flyouts,
       sum(groundouts)                                                as groundouts,
       sum(airouts)                                                   as airouts,
       sum(runs)                                                      as runs,
       sum(rbi)                                                       as rbi,
       sum(singles)                                                   as singles,
       sum(doubles)                                                   as doubles,
       sum(triples)                                                   as triples,
       sum(homeruns)                                                  as homeruns,
       sum(strikeouts)                                                as strikeouts,
       sum(walks)                                                     as walks,
       sum(intentional_walks)                                         as intentional_walks,
       sum(hits)                                                      as hits,
       sum(hbp)                                                       as hbp,
       sum(at_bats)                                                   as at_bats,
       case
           when (sum(at_bats) > 0) then sum(hits)::numeric / sum(at_bats)
           else null
           end                                                        as avg,
       case
           when (sum(at_bats) + sum(walks) + sum(hbp) + sum(sac_flies)) > 0 then
               (sum(hits) + sum(walks) + sum(hbp))::numeric /
               (sum(at_bats) + sum(walks) + sum(hbp) + sum(sac_flies))
           else null
           end                                                        as obp,
       case
           when sum(at_bats) > 0 then
               (sum(singles) + (sum(doubles) * 2) + (sum(triples) * 3) +
                (sum(homeruns) * 4))::numeric /
               sum(at_bats)
           else null end                                              as slg,
       -- ops calculate outside
       -- iso calculate outside
       sum(caught_stealing)                                           as caught_stealing,
       sum(stolen_bases)                                              as stolen_bases,
       -- ip
       sum(wins)                                                      as wins,
       sum(losses)                                                    as losses,
       sum(saves)                                                     as saves,
       sum(save_opportunities)                                        as save_opportunities,
       sum(holds)                                                     as holds,
       sum(blown_saves)                                               as blown_saves,
       sum(earned_runs)                                               as earned_runs,
       sum(batters_faced)                                             as batters_faced,
       sum(outs)                                                      as outs,
       sum(complete_games)                                            as complete_games,
       sum(shutouts)                                                  as shutouts,
       sum(pitch_count)                                               as pitch_count,
       sum(balls)                                                     as balls,
       sum(strikes)                                                   as strikes,
       sum(balks)                                                     as balks,
       sum(wild_pitches)                                              as wild_pitches,
       sum(pickoffs)                                                  as pickoffs,
       sum(pickoffs)                                                  as pickoffs,
-- runs per 9
-- homeruns per 9
       sum(inherited_runners)                                         as inherited_runners,
       sum(inherited_runners_scored)                                  as inherited_runners_scored,
       sum(catchers_int)                                              as catchers_int,
       sum(sac_bunts)                                                 as sac_bunts,
       sum(sac_flies)                                                 as sac_flies,
       sum(passed_ball)                                               as passed_ball,
       sum(popouts)                                                   as popouts,
       sum(lineouts)                                                  as lineouts,
       -- era
       -- whip
       -- k_per_9
       -- bb per 9
       -- k perc
       -- bb perc
       -- k perc minus bb perc
       case
           when (sum(at_bats) - sum(strikeouts) - sum(homeruns) + sum(sac_flies)) > 0 then
               (sum(hits) - sum(homeruns))::numeric /
               (sum(at_bats) - sum(strikeouts) - sum(homeruns) + sum(sac_flies))
           else null end                                              as babip
from games g
         inner join player_pitching pp on g.id = pp.game_id
group by season, player_id, link, team_id