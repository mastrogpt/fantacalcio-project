import axios from 'axios';
import {PUBLIC_FANTAICALCIO_BASE_URL, PUBLIC_ENDPOINT_FANTA_PLAYERS_ALL_SERIE_A } from '$env/static/public';

/*
ALL PLAYERS
*/
export interface Player {
    id: number;
    name: string;
    playmaker: boolean;
    position: string;
    team: string;
    photo: string;
    cards_red: string;
    cards_yellow: string;
    available: string;
    season_id: number;
    team_id: number;
}

export interface PlayersList extends Array<Player> {}

export async function getPlayersList(): Promise<PlayersList> {

    let apiHost = window.location.hostname.split('.')[0];
    console.log("API HOST IS " + apiHost)
    if(!apiHost || !apiHost.includes('fantabalun')) {
        apiHost = 'fantatest'
    }
    
    let finalUrl = PUBLIC_FANTAICALCIO_BASE_URL + apiHost + PUBLIC_ENDPOINT_FANTA_PLAYERS_ALL_SERIE_A
    
    try {
        const response = await axios.get(finalUrl, {
            params: { current_serie_a_players: 'true' }
        });
        
        return response.data.map((player: any) => ({
            id: player.id,
            name: player.name,
            team: player.team,
            photo: player.photo,
            cards_red: player.cards_red,
            cards_yellow: player.cards_yellow,
            available: player?.injured ? 'F' : 'Y',
            team_id: player?.team_id,
            season_id: player?.season_id,
            position: roleMapping[player.position] || player.position, 
           
        }));
    } catch (error) {
        console.error(error);
        throw error;
    }
}

export const roleMapping: { [key: string]: string } = {
    'Attacker': 'Attaccante',
    'Defender': 'Difensore',
    'Midfielder': 'Centrocampista',
    'Goalkeeper': 'Portiere'
};