import axios from 'axios';
import { PUBLIC_URL_AI_COMPARATOR  } from '$env/static/public';


/*
AI DESC
*/
export interface AiOutput {
    output: string;
}

export function getAiComparison(input: object): Promise<string> {
    return axios
        .post<AiOutput>(PUBLIC_URL_AI_COMPARATOR, {
            
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
