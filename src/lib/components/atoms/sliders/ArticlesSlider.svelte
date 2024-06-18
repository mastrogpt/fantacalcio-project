<script lang="ts">
	import { register } from 'swiper/element/bundle';
	import { fade } from 'svelte/transition';
	import ArticleSliderSlide from './partials/ArticleSliderSlide.svelte';
	import { getArticlesList } from '$lib/service/getArticles';
	import Loader from '../Loader.svelte';
	import { goto } from '$app/navigation';

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
</script>

{#await getArticlesList()}
	<Loader />
{:then articles}
	<div class="flex flex-col gap-[50px]">
		<!-- svelte-ignore a11y-no-static-element-interactions -->
		<swiper-container class="articles-slider-up" {...sliderContainerCommonProps} transition:fade>
			{#each articles as { title, subtitle, id }, idx}
				<ArticleSliderSlide
					onClick={() => goto(`/articles/${id}`)}
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
