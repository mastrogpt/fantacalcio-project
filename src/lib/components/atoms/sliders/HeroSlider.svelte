<script lang="ts">
	import { fade } from 'svelte/transition';
	import { register } from 'swiper/element/bundle';
	import HeroSliderSlide from './partials/HeroSliderSlide.svelte';
	import { goto } from '$app/navigation';
	import fantabalunbot from '$lib/assets/fantabalunbot.png';
	import fantabalun from '$lib/assets/fantabalun.png';
	import compare2 from '$lib/assets/compare2.png';
	import news from '$lib/assets/news.png';
	import { handleNuvBotChatOpening } from '$lib/store/store';

	register();

	const data = [
		{
			title: `<h2>Benvenuto su FantaBalùn! </h2> <h6> Powered by Nuvolaris </h6></p>`,
			description: `
            <p>È importante <span style="font-size: 20px;"><strong>vincere</strong></span>, ma a volte puoi solo <span style="font-size: 20px;"><strong>imprecare</strong></span>. <br> Con noi farai
 <strong><span style="font-size: 20px;"> entrambe le cose!</span></strong></p>
            `,
			buttonLabel: 'Il progetto',
			buttonOnClick: () => goto('/about'),
			imageUrl: fantabalun,
			imageAlt: 'img 1'
		},
		{
			title: 'Chiedilo al Bot &#x1F916',
			description:
				'<strong>Chiedi ciò che vuoi</strong>, come ad un amico al bar. Un parere, un confronto tra calciatori... Oppure, <strong>allega uno screen</strong> di un messaggio in cui un fantallenatore ti propone uno scambio.<br>Il bot sarà in grado di aiutarti!<br>No, <strong>non scola la pasta!</strong>&#x1F35D A questo non siamo ancora arrivati',
			imageUrl: fantabalunbot,
			buttonLabel: 'Chiedilo al bot',
			buttonOnClick: () => handleNuvBotChatOpening(true),
			imageAlt: 'img 4'
		},
		{
			title: 'Confronta i giocatori &#x2696',
			description:
				'Tanto alla fine sceglierai quello che avevi già in mente, però almeno così fingerai di averla <span style="font-size: 20px;"><strong>soppesata bene!</strong></span></p>',
			buttonLabel: 'Vai ai giocatori',
			buttonOnClick: () => goto('#players'),
			imageUrl: compare2,
			imageAlt: 'img 2'
		},
		{
			title: 'Leggi gli AIrticoli &#x1F4F0',
			description: `Siamo pigri per scriverli noi, ma vogliamo stare al passo! I nostri <strong>scraper generano articoli basandosi sulle ultime news</strong> <br>Sono precisi, anche se a volte potrebbero prendere un granchio. Come dici? Anche i giornalisti reali? &#x1F62D`,
			buttonLabel: 'Leggi gli airticoli',
			buttonOnClick: () => goto('#articles'),
			imageUrl: news,
			imageAlt: 'img 3'
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
		delay: 7000,
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
