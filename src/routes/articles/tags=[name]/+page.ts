import { getArticlesList, type IArticlesProps } from '$lib/service/getArticles';

export async function load({ params }: { params: { name: string } }) {
	const articles: IArticlesProps[] = await getArticlesList();
	const normalizedParam = params.name.replaceAll(' ', '_').toLocaleLowerCase();
	const filteredArticles = articles.filter((article) =>
		article.tag.some((tag) => tag.replaceAll(' ', '_').toLocaleLowerCase() === normalizedParam)
	);

	return { params, filteredArticles };
}
