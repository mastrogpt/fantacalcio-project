import { getArticlesList } from '$lib/service/fantaicalcio/getArticles';

export async function load({ params }: { params: { slug: number } }) {
	return getArticlesList().then((result) => result.find((e) => e.id === Number(params.slug)));
}
