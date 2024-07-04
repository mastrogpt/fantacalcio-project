import axios from 'axios';
import {PUBLIC_URL_API_BASEURL, PUBLIC_FANTAICALCIO_BASE_URL, PUBLIC_FANTAICALCIO_FANTA_PLAYERS_ALL_SERIE_A } from '$env/static/public';

/*
ALL PLAYERS
*/
interface Player {
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
    //value: number;
}

export interface PlayersList extends Array<Player> {}

export async function getPlayersList(): Promise<PlayersList> {
    
    var finalUrl = PUBLIC_FANTAICALCIO_BASE_URL + PUBLIC_FANTAICALCIO_FANTA_PLAYERS_ALL_SERIE_A
    
    try {
        const response = await axios.get(finalUrl, {
            params: { current_serie_a_players: 'true' }
        });
        console.log("players are", response.data)
        return response.data.map((player: any) => ({
            id: player.id,
            name: player.name,
            team: player.team,
            photo: player.photo,
            cards_red: player.cards_red,
            cards_yellow: player.cards_yellow,
            position: player?.position,
            available: player?.injured ? 'F' : 'Y',
            team_id: player?.team_id,
            season_id: player?.season_id
            //value: player.value
        }));
    } catch (error) {
        console.error(error);
        throw error;
    }
}

/*
UNAVAILABLE PLAYERS
*/
export interface UnavailablePlayers {
    team: string;
    role: string;
    desc: string;
    name: string;
    type: string;
    source_desc: string;
    next_day: string;
    doubt: boolean;
}

export interface UnavailabilityInfo {
    day: string;
    unavailable: UnavailablePlayers[];
}

export function getUnavailablePlayers(): Promise<UnavailablePlayers[]> {
    return axios
        .get(PUBLIC_URL_API_BASEURL, { params: { module: 'fantamaster', action: 'unavailable' } })
        .then((response) => {
            return response.data.data.unavailable.map((player: any) => ({
                team: player.team,
                role: player.role,
                desc: player.desc,
                name: player.name,
                type: player.type,
                source_desc: player.source_desc,
                next_day: player.next_day,
                doubt: player.doubt
            }));
        })
        .catch((error) => {
            console.error(error);
            throw error;
        });
}

