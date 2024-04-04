import axios from 'axios';
import { PUBLIC_URL_STATS  } from '$env/static/public';


/*
ALL PLAYERS STATS
*/
export interface PlayersStats {
    assists: number;
    caps: number;
    fmarkavg: number;
    goals: number;
    gotgoals: number;
    id: number;
    last5: {
        assists: number;
        caps: number;
        fmarkavg: number;
        goals: number;
        gotgoals: number;
        markavg: number;
        mpenalties: number;
        owngoals: number;
        penalties: number;
        rcards: number;
        spenalties: number;
        ycards: number;
    };
    markavg: number;
    mpenalties: number;
    name: string;
    owngoals: number;
    penalties: number;
    playmaker: boolean;
    rcards: number;
    role: string;
    spenalties: number;
    team: string;
    value: number;
    ycards: number;
}

export interface StatsData {
    players: PlayersStats[];
}

export function getStatsData(): Promise<PlayersStats[]> {
    return axios
        .get<StatsData>(PUBLIC_URL_STATS)
        .then((response) => {
            return response.data.players;
        })
        .catch((error) => {
            console.error(error);
            throw error;
        });
}

export async function getStatsDataById(id: number): Promise<PlayersStats | undefined> {
    try {
        const allPlayers = await getStatsData();
        const player = allPlayers.find((p) => p.id == id);
        if (player) {
            return player;
        } else {
            throw new Error(`Player with ID ${id} not found.`);
        }
    } catch (error) {
        console.error(error);
        throw error;
    }
}

//TODO LAST 5 