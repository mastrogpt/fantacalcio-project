import axios from 'axios';
import { PUBLIC_URL_AI_SINGLE_PLAYER  } from '$env/static/public';
import type { PlayerCompleteStats } from './fantaicalcio/getStats';


/*
ALL PLAYERS STATS
*/
export interface AiOutput {
    output: string;
}

export function getAiOpinionFromBackend(input: PlayerCompleteStats): Promise<string> {


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
