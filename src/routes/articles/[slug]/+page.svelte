<script lang="ts">
	import { goto } from '$app/navigation';
	import Loader from '$lib/components/atoms/Loader.svelte';
	import Carousel from '$lib/components/atoms/sliders/Carousel.svelte';
	import ArticleSliderSlide from '$lib/components/atoms/sliders/partials/ArticleSliderSlide.svelte';
	import { getArticlesList, type IArticlesProps } from '$lib/service/fantaicalcio/getArticles';

	export let data: IArticlesProps;

	// Function to format date
	function formatDate(isoDate: string, locale: string = 'it-IT'): string {
		const date = new Date(isoDate);
		const formattedDate = new Intl.DateTimeFormat(locale, {
			day: '2-digit',
			month: 'short',
			year: 'numeric',
		}).format(date);
		const formattedTime = new Intl.DateTimeFormat(locale, {
			hour: '2-digit',
			minute: '2-digit',
		}).format(date);
		return `${formattedDate} - ${formattedTime}`;
	}
</script>

<article class="flex flex-col justify-center items-center">
	<div class="article-bg" />

	<div class="article-content flex flex-col justify-center items-center gap-10">
		<div class="flex flex-col gap-3 article-title py-5 text-center">
			<small class="author">Scritto da {' '}{data?.author}</small>

			<h2 class="text-center mx-10">{data?.title}</h2>

			<small class="published-date">
				{formatDate(data?.creation_date, 'it-IT')}
			</small>
		</div>

		<div class="article-body container mx-10">
			<div class="article-body-text mx-20">
				{@html data?.content}
			</div>
		</div>
	</div>
</article>

<hr class="my-10" />

{#if data?.tag.length > 0}
	<div class="flex flex-col align-center justify-center text-center gap-2">
		<h6>TAGS:</h6>

		<div class="tags flex align-center justify-center gap-3 article-tags uppercase flex-wrap">
			{#each data.tag as tag}
				<button
					class="tag"
					on:click={() => goto('/articles/tags=' + tag.replaceAll(' ', '_').toLocaleLowerCase())}
				>
					#{tag}
				</button>
			{/each}
		</div>
	</div>
{/if}

<div class="flex flex-col justify-center items-center my-20">
	<h3>Altri AI-rticoli</h3>

	{#await getArticlesList()}
		<Loader />
	{:then data}
		<Carousel autoplay={2000}>
			{#each data as { id, author, creation_date, subtitle, title }, index (index)}
				<ArticleSliderSlide
					onClick={(e) => goto('/articles/' + e)}
					sliderData={{ id, author, creationDate: creation_date, subtitle, title }}
				/>
			{/each}
		</Carousel>
	{/await}
</div>

<style>
	.article-bg {
		display: flex;
		width: 100%;
		height: 50px;
	}

	.article-content {
		display: flex;
		width: 100%;
	}

	.article-title {
		width: 100%;
		max-width: 1250px;
	}

	.article-title small.author {
		opacity: 0.45;
		text-transform: uppercase;
		font-weight: bold;
	}

	.article-title h2 {
		font-size: 4rem;
		line-height: 4.5rem;
		text-transform: uppercase;
	}

	.article-body {
		width: 100%;
		max-width: 950px;
	}

	.article-body-text::first-letter {
		-webkit-initial-letter: 4 4;
		initial-letter: 4 4;
		color: rgb(var(--accent));
		font-weight: bold;
		margin-right: 0.75em;
	}

	.tags .tag {
		background: rgb(var(--primary));
		color: rgb(var(--white));
		font-weight: bold;
		border-radius: 0.5rem;
		padding: 0.35rem 1rem;
		opacity: 0.85;
		transition: all 250ms;
		cursor: pointer;
	}

	.tags .tag:hover {
		background: rgb(var(--primary));
		transform: scale(1.05);
		opacity: 1;
	}
</style>
