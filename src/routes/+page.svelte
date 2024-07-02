<script lang="ts">
	import { onMount } from 'svelte';
	import anime from 'animejs';
	import Button from '$lib/components/atoms/button/button.svelte';
	import ArticlesSlider from '$lib/components/atoms/sliders/ArticlesSlider.svelte';
	import HeroSlider from '$lib/components/atoms/sliders/HeroSlider.svelte';
	import Chatbot from '$lib/components/molecules/chatbot/Chatbot.svelte';
	import TableCard from '$lib/components/organisms/tableCard/TableCard.svelte';
	import TeamsComparator from '$lib/components/organisms/teamsComparator/TeamsComparator.svelte';
	import Loader from '$lib/components/atoms/Loader.svelte';
	import { getArticlesList } from '$lib/service/getArticles';

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
	class="articles-section flex flex-col items-center justify-center text-center my-10 py-20 gap-4 bg-accent"
>
	<h2 class="text-2xl md:text-4xl font-semibold" use:animateOnScroll>AIrticoli più discussi</h2>

	{#await getArticlesList()}
		<Loader />
	{:then data}
		<ArticlesSlider {data} />
	{/await}
</section>

<section
	class="table-section flex align-center justify-center text-center my-10 py-20 gap-4"
	id="players"
>
	<TableCard />
</section>

<section class="lineup-section flex flex-col text-center gap-5" id="composition">
	<TeamsComparator />
</section>

<section
	class="flex flex-col align-center justify-center items-center text-center my-10 gap-4 py-10"
>
	<div class="flex flex-col align-center justify-center items-center text-center gap-4">
		<h2 class="text-2xl md:text-4xl font-semibold" use:animateOnScroll>Collabora</h2>
		<p class="text-base md:text-lg">
			Fare il fantallenatore è stressante, fare il developer ancora di più, farle entrambe è da matti.  <br/>
			Se sei almeno una di queste due cose, non esitare a contattarci!
		</p>
		<Button label="Clicca qui" onClick={() => console.log('Button clicked')} />
	</div>
</section>



<!-- ><Chatbot /> -->



<style>
	.hero {
		height: calc(100vh - 100px);
		padding: 0 1rem;
	}

	.hero-slider {
		width: 100%;
		max-width: 1200px;
	}

	.decorative-ball {
		display: none;
	}

	@media (min-width: 768px) {
		.decorative-ball {
			display: block;
		}
	}
</style>
