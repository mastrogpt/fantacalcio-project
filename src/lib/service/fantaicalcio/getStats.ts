import axios from 'axios';
import {PUBLIC_URL_API_BASEURL, PUBLIC_FANTAICALCIO_BASE_URL, PUBLIC_FANTAICALCIO_FANTA_PLAYERS_STATS } from '$env/static/public';
import type { Player } from '../lineUp';

export interface PlayerStats {
    captain: boolean;
    cards_red: number;
    cards_yellow: number;
    cards_yellowred: number;
    dribbles_attempts: number;
    dribbles_past: number | null;
    dribbles_success: number | null;
    duels_total: number;
    duels_won: number;
    fouls_committed: number;
    fouls_drawn: number;
    games_appearences: number;
    games_lineups: number;
    games_minutes: number;
    games_number: number | null;
    goals_assists: number;
    goals_conceded: number;
    goals_saves: number | null;
    goals_total: number;
    passes_accuracy: number;
    passes_key: number;
    passes_total: number;
    penalty_committed: number | null;
    penalty_missed: number;
    penalty_saved: number | null;
    penalty_scored: number;
    penalty_won: number | null;
    player_id: number;
    position: string;
    rating: number;
    season_id: number;
    shots_on: number;
    shots_total: number;
    substitutes_bench: number;
    substitutes_in: number;
    substitutes_out: number;
    tackles_blocks: number;
    tackles_interceptions: number;
    tackles_total: number;
    team_id: number;
    uuid: string;
}
/*
ALL PLAYERS STATS
*/
export interface PlayerCompleteStats {
    player: any;
    player_statistic: PlayerStats;
    
}


export interface StatsData {
	players: PlayerStats
}

export function getStatsData(player_id, season_id, team_id): Promise<PlayerCompleteStats> {
	return axios
		.get(PUBLIC_FANTAICALCIO_BASE_URL + PUBLIC_FANTAICALCIO_FANTA_PLAYERS_STATS, { params: { player_id: player_id, season_id: season_id, team_id : team_id} })
		.then((response) => {
			//console.log("RESPONSE FINAL IS", response)
			return response.data as PlayerCompleteStats;
		})
		.catch((error) => {
			console.error(error);
			throw error;
		});
}

export async function getStatsDataById(player_id: number, season_id: number, team_id: number): Promise<PlayerCompleteStats | undefined> {
	try {
		const playerStats = await getStatsData(player_id, season_id, team_id);
		console.log("Player stats are", playerStats)
		if (playerStats) {
			return playerStats;
		} else {
			throw new Error(`Player with ID ${player_id} not found.`);
		}
	} catch (error) {
		console.error(error);
		throw error;
	}
}

//TODO LAST 5
