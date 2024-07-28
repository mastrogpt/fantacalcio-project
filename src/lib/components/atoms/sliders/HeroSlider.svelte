<script lang="ts">
	import { fade } from 'svelte/transition';
	import { register } from 'swiper/element/bundle';
	import HeroSliderSlide from './partials/HeroSliderSlide.svelte';
	import { goto } from '$app/navigation';
	import calcio3d from '$lib/assets/calcio3d.png';
	import confrontoGiocatori from '$lib/assets/confrontoGiocatori.png';
	import articlesImg from '$lib/assets/articlesImg.jpg';
	import lineups from '$lib/assets/lineups.jpg';
	import { openChatWithMessage } from '$lib/store/store';

	register();

	const data = [
		{
			title: 'Benvenuto su FantaBalùn! &#x26BD',
			description: `
            <p>Anche se è importante vincere, a volte puoi solo imprecare. Qui dentro, 
 <strong><span style="font-size: 24px;"> farai entrambe le cose !</span></strong></p>
            `,
			buttonLabel: 'Il progetto',
			buttonOnClick: () => goto('/about'),
			imageUrl: calcio3d,
			imageAlt: 'img 1'
		},
		{
			title: 'Chiedilo ar Bot &#x1F916',
			description:
				'<strong> Chiedigli quello che ti pare </strong>, come faresti con un amico al bar &#x1F37A <br> Chiedi un parere su un calciatore o un confronto tra due calciatori <br> Oppure, <strong> allega uno screenshot </strong> di una conversazione in cui un fantallenatore ti offre uno scambio. <br> FantaBalunbot sarà in grado di capire come aiutarti a vincere! <br> No, <strong> non scola la pasta </strong>  &#x1F35D A questo non ci siamo ancora arrivati.',
			imageUrl: lineups,
			buttonLabel: 'Chiedilo ar bot',
			buttonOnClick: () => openChatWithMessage(),
			imageAlt: 'img 4'
		},
		{
			title: 'Confronta i giocatori &#x2696',
			description:
				'Tanto alla fine sceglierai quello che avevi già in mente, però almeno così fingerai di averla soppesata bene',
			buttonLabel: 'Vai ai giocatori',
			buttonOnClick: () => goto('#players'),
			imageUrl: confrontoGiocatori,
			imageAlt: 'img 2'
		},
		{
			title: 'Informati con gli AIrticoli &#x1F4F0',
			description:
				'Siamo molto pigri per scrivere ogni giorno, ma vogliamo comunque stare al passo. I nostri scraper automatici generano articoli di attualità basandosi sulle ultime notizie. Non dar loro retta, a volte non  ci azzeccano. Come? Nemmeno i giornalisti veri? Ah no?',
			buttonLabel: 'Leggi gli airticoli',
			buttonOnClick: () => goto('#articles'),
			imageUrl: articlesImg,
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
