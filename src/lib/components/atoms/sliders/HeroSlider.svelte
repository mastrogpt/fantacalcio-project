<script lang="ts">
	import { fade } from 'svelte/transition';
	import { register } from 'swiper/element/bundle';
	import HeroSliderSlide from './partials/HeroSliderSlide.svelte';
	import { goto } from '$app/navigation';
	import logofanta200 from '$lib/assets/logofanta300.png';

	import fantabalun from '$lib/assets/fantabalun.png';
	import compare2 from '$lib/assets/compare2.png';
	import news from '$lib/assets/news.png';
	import { handleNuvBotChatOpening } from '$lib/store/store';

	register();

	const data = [
		{
			title: '<h2> FantaBalùn  &#x1F916 </h2> <h6>er Bot che ne sa un Bot-to </h6> ',
			description:
				'<p class="sm:text-sm text-base md:text-lg">Chiedi <strong> ciò che vuoi</strong>, come ad un amico al bar. Pareri, confronti tra calciatori. <strong>Allega lo screen </strong> di un messaggio in cui ti si propone uno scambio: BalùnBot ti dirà se conviene. No, <strong>non scola la pasta!</strong> </p>',
			imageUrl: logofanta200,
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
			title: 'Gli AI-rticoli &#x1F4F0',
			description: `Siamo pigri per scriverli noi. Per stare sempre sul pezzo, i nostri <strong> scraper generano articoli sulle ultime news </strong> <br> Ci servono per istruire Balùnbot, che sarà così in grado di consigliarti al meglio!`,
			buttonLabel: 'Leggi gli airticoli',
			buttonOnClick: () => goto('#articles'),
			imageUrl: news,
			imageAlt: 'img 3'
		},
		{
			title: `<h2>FantaBalùn! </h2> <h6> is Powered by Nuvolaris </h6></p>`,
			description: `
            <p>È importante <span style="font-size: 20px;"><strong>vincere</strong></span>, ma a volte puoi solo <span style="font-size: 20px;"><strong>imprecare</strong></span>. <br> Con noi farai
 <strong><span style="font-size: 20px;"> entrambe le cose!</span></strong></p>
            `,
			buttonLabel: 'Il progetto',
			buttonOnClick: () => goto('/about'),
			imageUrl: fantabalun,
			imageAlt: 'img 1'
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
		delay: 10000,
		disableOnInteraction: true,
		pauseOnMouseEnter: true
	}}
	coverflowEffect={{
		rotate: 150,
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
