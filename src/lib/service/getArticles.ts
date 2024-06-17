import axios from 'axios';
import { PUBLIC_URL_AI_ARTICLES } from '$env/static/public';

export interface IArticlesProps {
	author: string;
	content: string;
	subtitle: string;
	title: string;
	category: string[];
	tag: string[];
	creationDate: string;
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
