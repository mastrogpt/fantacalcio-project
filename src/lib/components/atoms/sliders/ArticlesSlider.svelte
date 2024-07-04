<script lang="ts">
	import { goto } from '$app/navigation';
	import { type IArticlesProps } from '$lib/service/getArticles';
	import { fade } from 'svelte/transition';
	import { register } from 'swiper/element/bundle';
	import ArticleSliderSlide from './partials/ArticleSliderSlide.svelte';

	register();

	export let data: IArticlesProps[] = [];

	const sliderContainerCommonProps = {
		'space-between': 50,
		pagination: false,
		'slides-per-view': 3,
		loop: true,
		autoplay: {
			delay: 3000,
			disableOnInteraction: true,
			pauseOnMouseEnter: true
		}
	};
</script>

<div class="flex flex-col gap-[50px]">
	{#if data?.length > 10}
		<!-- Primo slider con la prima metà degli articoli -->
		<swiper-container class="articles-slider-up" {...sliderContainerCommonProps} transition:fade>
			{#each data?.slice(0, data?.length / 2) as { title, subtitle, id, author, creation_date }, idx}
				<ArticleSliderSlide
					onClick={() => goto(`/articles/${id}`)}
					sliderData={{
						title,
						subtitle,
						author,
						creationDate: creation_date
					}}
				/>
			{/each}
		</swiper-container>

		<!-- Secondo slider con la seconda metà degli articoli -->
		<swiper-container
			class="articles-slider-bottom"
			{...sliderContainerCommonProps}
			autoplay={{
				...sliderContainerCommonProps.autoplay,
				reverseDirection: true
			}}
			transition:fade
		>
			{#each data?.slice(data?.length / 2) as { title, subtitle, id, author, creation_date }, idx}
				<ArticleSliderSlide
					onClick={() => goto(`/articles/${id}`)}
					sliderData={{
						title,
						subtitle,
						author,
						creationDate: creation_date
					}}
				/>
			{/each}
		</swiper-container>
	{:else}
		<!-- Slider singolo se gli articoli sono meno di 10 -->
		<swiper-container class="articles-slider-up" {...sliderContainerCommonProps} transition:fade>
			{#each data as { title, subtitle, id, author, creation_date }, idx}
				<ArticleSliderSlide
					onClick={() => goto(`/articles/${id}`)}
					sliderData={{
						title,
						subtitle,
						author,
						creationDate: creation_date
					}}
				/>
			{/each}
		</swiper-container>
	{/if}
</div>

<style>
	swiper-container {
		width: 90vw;
		height: 100%;
	}

	.swiper-wrapper {
		transition-timing-function: linear;
	}
</style>
