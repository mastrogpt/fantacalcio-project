<script lang="ts">
	import { fade } from 'svelte/transition';
	import { register } from 'swiper/element/bundle';
	import HeroSliderSlide from './partials/HeroSliderSlide.svelte';
	import { goto } from '$app/navigation';
	import calcio3d from '$lib/assets/calcio3d.png'
	import confrontoGiocatori from '$lib/assets/confrontoGiocatori.png'
	import articlesImg from '$lib/assets/articlesImg.jpg'
	import lineups from '$lib/assets/lineups.jpg'


	register();

	const data = [
		{
			title: 'Benvenuto su FantAIcalcio!',
			description: 'La piattaforma che ti aiuta a vincere divertendoti',
			buttonLabel: 'Chi siamo',
			buttonOnClick: () => goto("/about"),
			imageUrl: calcio3d,
			imageAlt: 'img 1'
		},
		{
			title: 'Confronta i giocatori',
			description: 'Usa i nostri dati e la nostra AI',
			buttonLabel: 'Vai ai giocatori',
			buttonOnClick: () => goto("#players"),
			imageUrl: confrontoGiocatori,
			imageAlt: 'img 2'
		},
		{
			title: 'Informati con gli AIrticoli',
			description: 'Articoli della nostra redaizione fatti apposta per te',
			buttonLabel: 'Leggi gli airticoli',
			buttonOnClick: () => goto("#articles"),
			imageUrl: articlesImg,
			imageAlt: 'img 3'
		},
		{
			title: 'Scopri le formazioni',
			description: 'I pronostici e le ultime',
			buttonLabel: 'Probabili formazioni',
			buttonOnClick: () => goto("#composition"),
			imageUrl: lineups,
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
