import axios from 'axios';
import {
	PUBLIC_FANTAICALCIO_BASE_URL,
	PUBLIC_FANTAICALCIO_FANTA_PLAYERS_STATS
} from '$env/static/public';
import { roleMapping } from './getPlayers';
import type { Player } from './getPlayers';
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
	s: number;
	uuid: string;
}
/*
ALL PLAYERS STATS
*/
export interface ISliderDataProps {
	name: string;
}

export interface ITeamProps {
	apifootball_id: number;
	code: string;
	country: string;
	founded: number;
	id: number;
	logo: string;
	name: string;
	national: boolean;
	uuid: string;
	venue_address: string;
	venue_capacity: number;
	venue_city: string;
	venue_image: string;
	venue_name: string;
	venue_surface: string;
}

export interface PlayerCompleteStats {
	player?: Player;
	player_statistic?: PlayerStats;
	team?: ITeamProps;
}

export interface StatsData {
	players: PlayerStats;
}

export function getStatsData(player_id, season_id, team_id): Promise<PlayerCompleteStats> {
	return axios
		.get(PUBLIC_FANTAICALCIO_BASE_URL + PUBLIC_FANTAICALCIO_FANTA_PLAYERS_STATS, {
			params: { player_id: player_id, season_id: season_id, team_id: team_id }
		})
		.then((response) => {
			//console.log("RESPONSE FINAL IS", response)
			return response.data as PlayerCompleteStats;
		})
		.catch((error) => {
			console.error(error);
			throw error;
		});
}
export async function getStatsDataById(
	player_id: number,
	season_id: number,
	team_id: number,
	mapped?: boolean
): Promise<PlayerCompleteStats | undefined> {
	try {
		const playerStats = await getStatsData(player_id, season_id, team_id);

		if (mapped && playerStats.player_statistic?.position) {
			playerStats.player_statistic.position = roleMapping[playerStats.player_statistic.position] || playerStats.player_statistic.position;
		}

		const playerSpecs = Object.keys(playerStats?.player_statistic || {}).map((e) => ({
			label: getStatsDataByIdLabelMapper[e],
			value: getStatsDataByIdValueMapper(String(playerStats?.player_statistic?.[e]))
		}));

		if (mapped) {
			return {
				player: playerStats.player,
				player_statistic: playerSpecs.filter(({ label, value }) => label && value !== 'null'),
				team: playerStats.team?.name
			};
		}

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


const getStatsDataByIdLabelMapper = {
	captain: 'Capitano',
	cards_red: 'Cartellini rossi',
	cards_yellow: 'Cartellini gialli',
	dribbles_attempts: 'Dribbling tentati',
	dribbles_past: 'Dribbling subiti',
	dribbles_success: 'Dribbling riusciti',
	duels_total: 'Duelli totali',
	duels_won: 'Duelli vinti',
	fouls_committed: 'Falli',
	fouls_drawn: 'Falli subiti',
	games_appearences: 'Presenze',
	games_lineups: 'Presenze da titolare',
	games_minutes: 'Minuti di gioco',
	// games_number: "Partite vinte",
	goals_assists: 'Assist',
	goals_conceded: 'Goal concessi',
	goals_saves: 'Goal savati',
	goals_total: 'Goal totali',
	passes_accuracy: 'Passaggi riusciti',
	passes_key: 'Passaggi chiave',
	passes_total: 'Passaggi totali',
	penalty_committed: 'Rigori concessi',
	penalty_missed: 'Rigori sbagliati',
	penalty_saved: 'Rigori salvati',
	penalty_scored: 'Rigori segnati',
	penalty_won: 'Rigori procurati',
	position: 'Ruolo',
	rating: 'Valutazione',
	shots_on: 'Tiri in porta',
	shots_total: 'Tiri totali',
	// substitutes_bench: "Sostituzioni",
	substitutes_in: 'Sostituzioni In',
	substitutes_out: 'Sostituzioni Out',
	tackles_blocks: 'Contrasti',
	tackles_interceptions: 'Intercettazioni',
	tackles_total: 'Tackle totali'
};

const getStatsDataByIdValueMapper = (val: string) => {
	switch (val) {
		case 'true':
			return '✅';
		case 'false':
			return '❌';

		default:
			return val;
	}
};
