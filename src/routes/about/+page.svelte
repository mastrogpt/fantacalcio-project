<script lang="ts">
	import aboutImage from '$lib/assets/about.png';
	import Loader from '$lib/components/atoms/Loader.svelte';
	import JoinCta from '$lib/components/molecules/JoinCta.svelte';
	import { getAiPresentationFromBackend } from '$lib/service/ai/aiPresentation';
	import { onMount } from 'svelte';

	let aiPresentation: string;
	let aiPresentationWritingEffect: string = '';
	let isLoading = false;

	async function showMessage() {
		for (let i = 0; i < aiPresentation.length; i++) {
			aiPresentationWritingEffect = aiPresentation.substring(0, i + 1);
			await sleep(25);
		}
	}

	function sleep(ms: number) {
		return new Promise((resolve) => setTimeout(resolve, ms));
	}

	async function getAiPresentation() {
		isLoading = true;
		aiPresentation = await getAiPresentationFromBackend();
		showMessage();
		isLoading = false;
	}

	onMount(async () => {
		await getAiPresentation();
	});
</script>

<div class="min-h-screen flex flex-col items-center justify-center p-5">
	<div class="max-w-4xl w-full p-8">
		<h2 class="text-5xl font-bold text-dark mb-6">Chi siamo 👋🏻</h2>

		<hr class="mb-6" />

		<div class="text-section mb-8">
			<h2 class="text-3xl font-semibold mb-4">La nostra passione</h2>

			<p class="text-lg">
				Siamo sviluppatori di software, amanti del calcio, delle statistiche e delle innovazioni.
			</p>
		</div>

		<div class="flex flex-col items-center md:flex-row">
			<div class="text-section w-[100%] md:w-[60%]">
				<h2 class="text-3xl font-semibold mb-4">Il nostro progetto</h2>

				<p class="text-lg mb-4">
					Attraverso questo progetto, vogliamo offrire ai Fantallenatori di tutta Italia un
					consigliere fidato, un AI che somigli all'amico a cui chiedere consiglio il giovedì sera
					davanti ad una birra su che calciatore schierare o su chi comprare all'asta.
				</p>
			</div>

			<div class="w-[85%] md:w-[40%]">
				<img src={aboutImage} alt="About Us" class=" h-auto rounded-lg" />
			</div>
		</div>
		<div class="text-section mb-8">
			<h2 class="text-3xl font-semibold mb-4">La nostra filosofia</h2>

			<p class="text-lg mb-4">
				L'amico che ne sa, ma che non pretende di aver sempre ragione, perché il fantacalcio è arte
				e improvvisazione, oltre che strategia. E noi, oltre i buoni consigli, vogliamo portare
				fortuna!
			</p>
		</div>
		<div class="text-section mb-8 italic">
			<p class="text-lg">
				Usiamo Nuvolaris come piattaforma, il serverless come filosofia. Se vuoi unirti a noi,<br />

				<JoinCta />
			</p>
		</div>

		<hr />

		<h2 class="text-3xl font-semibold mb-4 mt-4">Chi è MastroGPT?</h2>

		<div class="mt-4">
			{#if aiPresentation}
				<p>{aiPresentationWritingEffect}</p>
			{:else}
				<Loader />
			{/if}
		</div>
		<div
			class="bubble-container absolute inset-0 flex justify-center items-center pointer-events-none"
		></div>
	</div>
</div>

<style>
	.min-h-screen {
		min-height: 100vh;
	}

	.max-w-4xl {
		max-width: 64rem;
	}

	.bubble-container {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		overflow: hidden;
	}
</style>
