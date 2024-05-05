import axios from 'axios';
import { PUBLIC_URL_API_BASEURL } from '$env/static/public';

export interface PlayerInjured {
    desc: string;
    player: string;
}

export interface PlayerLatest {
    away_score: number;
    away_team: string;
    gameweek: number;
    home_score: number;
    home_team: string;
    result: string;
}

export interface Player {
    index: number;
    player: string;
    prob: number;
    sources: {
        milano: string;
        roma: string;
        sky: string;
    };
}

export interface PlayerUncertain {
    player1: string;
    player2: string;
    prob1: number;
    prob2: number;
}

export interface News {
    api_url: string;
    categories: string[];
    color: string;
    date: string;
    image: string;
    source: string;
    thumbnail: string;
    title: string;
    url: string;
}

export interface LineUp {
    away: string;
    away_banned: { desc: string; player: string }[];
    away_indoubt: { desc: string; player: string }[];
    away_injured: PlayerInjured[];
    away_latest: PlayerLatest[];
    date: string;
    fm: {
        away_bench: Player[];
        away_lineup: Player[];
        away_mod: string;
        away_uncertain: PlayerUncertain[];
        has_probs: boolean;
        home_bench: Player[];
        home_lineup: Player[];
        home_mod: string;
        home_uncertain: PlayerUncertain[];
    };
    home: string;
    home_banned: { desc: string; player: string }[];
    home_indoubt: { desc: string; player: string }[];
    home_injured: PlayerInjured[];
    home_latest: PlayerLatest[];
    news: News;
}



export interface FootballMatch {
    
    date: string;
    fm: {
        away_mod: string;
        has_probs: boolean;
        home_mod: string;
    };
    last_updated: string;
    lineups: LineUp[];
    day: number;
}

export function getLineUp(): Promise<FootballMatch> {
    return axios
        .get(PUBLIC_URL_API_BASEURL, {params: {"module":"fantamaster", "action": "lineups"}})
        .then((response) => {
            return response.data.data})
        .catch((error) => {
            console.error(error);
            throw error;
        });
}