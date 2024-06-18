<script lang="ts">
	import Button from '$lib/components/atoms/button/button.svelte';
	import ArticlesSlider from '$lib/components/atoms/sliders/ArticlesSlider.svelte';
	import HeroSlider from '$lib/components/atoms/sliders/HeroSlider.svelte';
	import Chatbot from '$lib/components/molecules/chatbot/Chatbot.svelte';
	import TableCard from '$lib/components/organisms/tableCard/TableCard.svelte';
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

<section class="hero flex flex-col items-center justify-center text-center gap-10">
	<div bind:this={heroSlider} class="hero-slider">
		<HeroSlider />
	</div>
</section>

<section
	class="articles-section flex flex-col items-center justify-center text-center my-20 gap-10 bg-accent py-20"
>
	<h2 class="text-4xl font-semibold" use:animateOnScroll>Articoli più discussi</h2>

	<ArticlesSlider />
</section>

<section class="table-secction flex align-center justify-center text-center my-20 gap-10 py-20">
	<TableCard />
</section>

<section
	class="flex flex-col align-center justify-center items-center text-center my-20 gap-10 py-20"
>
	<div
		class="flex flex-col align-center justify-center items-center text-center my-20 gap-10 py-20 container"
	>
		<h2 class="text-4xl font-semibold" use:animateOnScroll>Collabora</h2>

		<p>
			Lorem ipsum, dolor sit amet consectetur adipisicing elit. Molestiae, debitis sint. Incidunt
			cumque cum necessitatibus, optio tempore eos reprehenderit similique placeat hic porro amet
			atque sint voluptas molestias quasi vitae.
		</p>

		<Button label="Clicca qui" onClick={console.log} />
	</div>
</section>

<Chatbot />

<style>
	.hero {
		height: calc(100vh - 100px);
	}

	.hero-slider {
		width: 100%;
		max-width: 1200px;
	}
</style>
