import axios from 'axios';
import { PUBLIC_URL_AI_LINEUP_OPINION  } from '$env/static/public';
import type { LineUp } from '../fantamaster/lineUp';


/*
LINEUP STATS
*/
export interface AiOutput {
    output: string;
}

export function getAiLineupOpinion(input: LineUp): Promise<string> {


    let dataToSend = input.fm;

    return axios
        .post<AiOutput>(PUBLIC_URL_AI_LINEUP_OPINION, {
            'input': dataToSend
        })
        .then((response) => {
            return response.data.output;
        })
        .catch((error) => {
            console.error(error);
            throw error;
        });
}
