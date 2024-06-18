<script lang="ts">
	import ArticlesSlider from '$lib/components/atoms/sliders/ArticlesSlider.svelte';
	import type { IArticlesProps } from '$lib/service/getArticles.js';

	export let data: IArticlesProps;

	console.log('🔎 [+page][data] =>', data);
</script>

<article class="flex flex-col justify-center items-center">
	<div class="article-bg" />

	<div class="article-content flex flex-col justify-center items-center gap-10">
		<div class="article-title bg-accent py-5">
			<h2 class="text-center mx-10">{data?.title}</h2>
		</div>

		<div class="article-body container mx-10">
			<p class="article-body-text mx-20">
				{data?.content}
			</p>
		</div>
	</div>
</article>

<div class="flex flex-col justify-center items-center my-20">
	<h3>Altri articoli</h3>

	<div class="flex my-10">
		<ArticlesSlider />
	</div>
</div>

<style>
	.article-bg {
		display: flex;
		width: 100%;
		height: 250px;
		background: url('https://picsum.photos/id/234/400/500');
		background-size: cover;
		background-repeat: no-repeat;
	}

	.article-content {
		display: flex;
		width: 100%;
	}

	.article-title {
		width: 100%;
	}

	.article-body-text::first-letter {
		-webkit-initial-letter: 4 4;
		initial-letter: 4 4;
		color: rgb(var(--accent));
		font-weight: bold;
		margin-right: 0.75em;
	}
</style>
