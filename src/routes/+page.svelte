<script lang="ts">
	import { goto } from '$app/navigation';
	import Loader from '$lib/components/atoms/Loader.svelte';
	import Carousel from '$lib/components/atoms/sliders/Carousel.svelte';
	import HeroSlider from '$lib/components/atoms/sliders/HeroSlider.svelte';
	import ArticleSliderSlide from '$lib/components/atoms/sliders/partials/ArticleSliderSlide.svelte';
	import JoinCta from '$lib/components/molecules/JoinCta.svelte';
	import TableCard from '$lib/components/organisms/tableCard/TableCard.svelte';
	import { getArticlesList } from '$lib/service/fantaicalcio/getArticles';
	import anime from 'animejs';
	import { onMount } from 'svelte';

	let heroTitle: HTMLHeadingElement;
	let heroSubtitle: HTMLHeadingElement;
	let heroSlider: HTMLDivElement;

	onMount(async () => {
		anime
			.timeline({ loop: false })
			.add({
				targets: heroTitle,
				translateY: [-50, 0],
				opacity: [0, 1],
				duration: 800,
				easing: 'easeOutExpo',
				delay: (el, i) => 500 + 30 * i
			})
			.add({
				targets: heroSubtitle,
				translateY: [50, 0],
				opacity: [0, 1],
				duration: 800,
				easing: 'easeOutExpo',
				delay: (el, i) => 800 + 30 * i
			})
			.add({
				targets: heroSlider,
				opacity: [0, 1],
				duration: 1000,
				easing: 'easeOutExpo',
				offset: '-=500'
			});
	});

	function animateOnScroll(target: Element): void {
		const observer: IntersectionObserver = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						anime({
							targets: entry.target,
							translateY: [100, 0],
							opacity: [0, 1],
							duration: 1000,
							easing: 'easeOutExpo'
						});
						observer.unobserve(entry.target);
					}
				});
			},
			{ threshold: 0.1 }
		);
		observer.observe(target);
	}
</script>

<section class="hero flex flex-col items-center justify-center text-center gap-4">
	<div bind:this={heroSlider} class="hero-slider">
		<HeroSlider />
	</div>
</section>
<section
	class="table-section flex align-center justify-center text-center my-10 py-20 gap-4"
	id="players"
>
	<TableCard />
</section>

<section
	id="articles"
	class="articles-section flex flex-col items-center justify-center text-center my-10 py-20 gap-4 bg-accent"
>
	<h2 class="text-2xl md:text-4xl font-semibold" use:animateOnScroll>AIrticoli più discussi</h2>

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
</section>

<!-- <section class="lineup-section flex flex-col text-center gap-5 py-5" id="composition">
	<TeamsComparator />
</section> -->

<section
	class="flex flex-col align-center justify-center items-center text-center my-10 gap-4 py-10"
>
	<div class="flex flex-col align-center justify-center items-center text-center gap-4">
		<h2 class="text-2xl md:text-4xl font-semibold" use:animateOnScroll>Collabora</h2>

		<p class="text-base md:text-lg">
			Fare il fantallenatore è stressante, fare il developer ancora di più, farle entrambe è da
			matti. <br />
			Se sei almeno una di queste due cose <JoinCta />
		</p>
	</div>
</section>

<style>
	.hero {
		height: calc(100vh - 100px);
		padding: 0 1rem;
	}

	.hero-slider {
		width: 100%;
		max-width: 1200px;
	}
</style>
