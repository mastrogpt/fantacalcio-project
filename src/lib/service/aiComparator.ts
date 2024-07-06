import axios from 'axios';
import { PUBLIC_URL_AI_COMPARATOR  } from '$env/static/public';
import type { PlayersList } from './fantamaster/getPlayers';
import {getStatsDataById}  from '$lib/service/fantaicalcio/getStats'

/*
AI DESC
*/
export interface AiOutput {
    output: string;
}

export async function getAiComparison(input: PlayersList): Promise<string> {
    let playersDetails: any[] = [];
  
    for (const element of input) {
      try {
        let playerStats = await getStatsDataById(element.id, element.team_id, element.season_id);
        let playerDetail = {

          player_name: playerStats?.player.name,
          playmaker: playerStats?.player.playmaker,
          role: playerStats?.player.role,
          team: playerStats?.player.team,

          stats: playerStats?.player_statistic

        };
        playersDetails.push(playerDetail);
      } catch (error) {
        console.error(`Error fetching stats for player ID ${element.id}:`, error);
      }
    }
  
    try {

      const response = await axios.post<AiOutput>(PUBLIC_URL_AI_COMPARATOR, {
        'input': playersDetails
      });
      return response.data.output;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
