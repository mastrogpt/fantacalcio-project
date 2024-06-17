<script lang="ts">
	import { fade } from 'svelte/transition';
	import { register } from 'swiper/element/bundle';
	import HeroSliderSlide from './partials/HeroSliderSlide.svelte';

	register();

	const data = [
		{
			title: 'Titolo 1',
			description: 'Descrzione 1',
			buttonLabel: 'Bottone 1',
			buttonOnClick: () => console.log,
			imageUrl: 'asd',
			imageAlt: 'img 1'
		},
		{
			title: 'Titolo 2',
			description: 'Descrzione 2',
			buttonLabel: 'Bottone 2',
			buttonOnClick: () => console.log,
			imageUrl: 'asd',
			imageAlt: 'img 2'
		},
		{
			title: 'Titolo 3',
			description: 'Descrzione 3',
			buttonLabel: 'Bottone 3',
			buttonOnClick: () => console.log,
			imageUrl: 'asd',
			imageAlt: 'img 3'
		},
		{
			title: 'Titolo 4',
			description: 'Descrzione 4',
			buttonLabel: 'Bottone 4',
			buttonOnClick: () => console.log,
			imageUrl: 'asd',
			imageAlt: 'img 4'
		}
	];
</script>

<swiper-container
	class="swiper-hero"
	pagination={{
		dynamicBullets: true,
		clickable: true
	}}
	effect="coverflow"
	centeredSlides={true}
	slides-per-view="auto"
	autoplay={{
		delay: 5000,
		disableOnInteraction: true,
		pauseOnMouseEnter: true
	}}
	coverflowEffect={{
		rotate: 100,
		stretch: 0,
		depth: 100,
		modifier: 1,
		slideShadows: false
	}}
	transition:fade
>
	{#each data as sliderData}
		<HeroSliderSlide {sliderData} />
	{/each}

	<!-- <swiper-slide class="max-[600px]:flex-col-reverse">
		<div class="flex flex-col text-left justify-start hero-text gap-10">
			<div class="flex flex-col gap-4">
				<h2>
					Benvenuto su br
					<b class="text-accent">FantaAICalcio</b>
				</h2>

				<p>Il tuo assistente AI per il fantacalcio.</p>
			</div>

			<Button label="scopri Chi siamo!" onClick={console.log} variant="accent" />
		</div>

		<div class="hero-image">
			<img src="https://swiperjs.com/demos/images/nature-3.jpg" alt="descrizione" loading="lazy" />
		</div>
	</swiper-slide> -->
</swiper-container>

<style>
	.swiper-hero {
		width: 100%;
		height: 80vh;
	}

	swiper-container {
		width: 100%;
		padding-bottom: 50px;
	}
</style>
