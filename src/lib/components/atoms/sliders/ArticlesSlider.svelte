<script lang="ts">
	import { register } from 'swiper/element/bundle';
	import { fade } from 'svelte/transition';
	import ArticleSliderSlide from './partials/ArticleSliderSlide.svelte';
	import { getArticlesList } from '$lib/service/getArticles';
	import Loader from '../Loader.svelte';

	register();

	const sliderContainerCommonProps = {
		'space-between': 50,
		pagination: false,
		'slides-per-view': 'auto',
		loop: true,
		autoplay: {
			delay: 3000,
			disableOnInteraction: true,
			pauseOnMouseEnter: true
		}
	};

	const slider1Slides = [
		{
			title: 'slide 1',
			subtitle: 'slide 1'
		},
		{
			title: 'slide 2',
			subtitle: 'slide 2'
		},
		{
			title: 'slide 3',
			subtitle: 'slide 3'
		},
		{
			title: 'slide 4',
			subtitle: 'slide 4'
		},
		{
			title: 'slide 5',
			subtitle: 'slide 5'
		}
	];

	const slider2Slides = [
		{
			title: 'slide 1',
			subtitle: 'slide 1'
		},
		{
			title: 'slide 2',
			subtitle: 'slide 2'
		},
		{
			title: 'slide 3',
			subtitle: 'slide 3'
		},
		{
			title: 'slide 4',
			subtitle: 'slide 4'
		},
		{
			title: 'slide 5',
			subtitle: 'slide 5'
		}
	];
</script>

{#await getArticlesList()}
	<Loader />
{:then articles}
	<div class="flex flex-col gap-[50px]">
		<swiper-container class="articles-slider-up" {...sliderContainerCommonProps} transition:fade>
			{#each articles as { title, subtitle }, idx}
				<ArticleSliderSlide
					sliderData={{
						title,
						subtitle,
						imageUrl: `https://picsum.photos/id/${234 + idx}/400/500`
					}}
				/>
			{/each}
		</swiper-container>

		<!-- <swiper-container
			class="articles-slider-bottom"
			{...sliderContainerCommonProps}
			autoplay={{
				...sliderContainerCommonProps.autoplay,
				reverseDirection: true
			}}
			transition:fade
		>
			{#each slider2Slides as sliderData}
				<ArticleSliderSlide {sliderData} />
			{/each}
		</swiper-container> -->
	</div>
{/await}

<style>
	swiper-container {
		width: 100vw;
		height: 100%;
	}

	.swiper-wrapper {
		transition-timing-function: linear;
	}
</style>
