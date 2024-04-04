import axios from 'axios';
import { PUBLIC_URL_AI_SINGLE_PLAYER  } from '$env/static/public';
import type { PlayersStats } from './getStats';


/*
ALL PLAYERS STATS
*/
export interface AiOutput {
    output: string;
}

export function getAiOpinionFromBackend(input: PlayersStats): Promise<string> {
    return axios
        .post<AiOutput>(PUBLIC_URL_AI_SINGLE_PLAYER, {
            'input': input
        })
        .then((response) => {
            return response.data.output;
        })
        .catch((error) => {
            console.error(error);
            throw error;
        });
}
