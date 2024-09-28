import axios from 'axios';
import { PUBLIC_FANTAICALCIO_BASE_URL, PUBLIC_ENDPOINT_AI_ARTICLES } from '$env/static/public';

export interface IArticlesProps {
	author: string;
	content: string;
	subtitle: string;
	id: number;
	title: string;
	category: string[];
	tag: string[];
	creation_date: string;
}

export async function getArticlesList(): Promise<IArticlesProps[]> {
	try {

		let apiHost = window.location.hostname.split('.')[0];
		console.log("API HOST IS art" + apiHost)
		if(!apiHost || !apiHost.includes('fantabalun')) {
			apiHost = 'fantatest'
		}
		const response = await axios.get(PUBLIC_FANTAICALCIO_BASE_URL + apiHost + PUBLIC_ENDPOINT_AI_ARTICLES, {
			params: { model: 'article', limit : 150 }
		});
		return response.data?.map((articles: IArticlesProps[]) => articles);
	} catch (error) {
		console.error(error);
		throw error;
	}
}
