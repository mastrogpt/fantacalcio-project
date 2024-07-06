import axios from 'axios';
import { PUBLIC_URL_AI_PRESENTATION } from '$env/static/public';


/*
AI WELCOME MESSAGE
*/
export interface AiOutput {
    output: string;
}

export function getAiPresentationFromBackend(): Promise<string> {
    return axios
        .get<AiOutput>(PUBLIC_URL_AI_PRESENTATION, {
            
        })
        .then((response) => {
            return response.data.output;
        })
        .catch((error) => {
            console.error(error);
            throw error;
        });
}
