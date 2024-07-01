<script lang="ts">
	import { goto } from '$app/navigation';
	import Loader from '$lib/components/atoms/Loader.svelte';
	import type { IArticlesProps } from '$lib/service/getArticles';

	export let data: { params: { name: string }; filteredArticles: IArticlesProps[] };

	let { params, filteredArticles } = data;
	let isLoading: boolean = false;
	let error: string | null = null;

	function navigateToArticle(articleId: number) {
		goto(`/articles/${articleId}`);
	}
</script>

<div class="container mx-auto p-4 my-20">
	<h1 class="text-3xl font-bold mb-4 text-center text-white pb-10">
		Articoli con il tag "{params.name}"
	</h1>

	{#if isLoading}
		<Loader />
	{:else if error}
		<div class="text-red-500">{error}</div>
	{:else if filteredArticles?.length > 0}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-static-element-interactions -->
			{#each filteredArticles as article}
				<div
					class="article-card bg-white rounded-lg shadow-md overflow-hidden cursor-pointer"
					on:click={() => navigateToArticle(article?.id)}
				>
					<div class="p-6">
						<h2 class="text-2xl font-bold mb-2">{article?.title}</h2>
						<p class="text-gray-600 mb-4">{article?.subtitle}</p>
						<p class="text-sm text-gray-500 mb-2">
							Di {article?.author} il {new Date(article?.creation_date || '').toLocaleDateString()}
						</p>
						<p class="text-sm text-blue-600">{params.name}</p>
					</div>
				</div>
			{/each}
		</div>
	{:else}
		<div class="text-gray-500 text-center">Nessun articolo trovato per il tag specificato.</div>
	{/if}
</div>

<style>
	.article-card {
		transition:
			transform 0.3s,
			box-shadow 0.3s;
	}
	.article-card:hover {
		transform: translateY(-10px);
		box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
	}
</style>
