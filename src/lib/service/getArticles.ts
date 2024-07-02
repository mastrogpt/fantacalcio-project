import axios from 'axios';
import { PUBLIC_URL_AI_ARTICLES } from '$env/static/public';

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
		const response = await axios.get(PUBLIC_URL_AI_ARTICLES, {
			params: { model: 'article' }
		});
		return response.data?.map((articles: IArticlesProps[]) => articles);
	} catch (error) {
		console.error(error);
		throw error;
	}
}
