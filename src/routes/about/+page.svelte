<script lang="ts">
	import fantabalun from '$lib/assets/fantabalun.png';
	import JoinCta from '$lib/components/molecules/JoinCta.svelte';
</script>

<div class="min-h-screen flex flex-col items-center justify-center p-5">
	<div class="max-w-4xl w-full p-8 shadow-lg rounded-lg">
		<div class="mb-8">
			<h2 class="text-3xl font-semibold mb-4">La nostra passione</h2>

			<p class="text-lg">
				Siamo sviluppatori di software, amanti del calcio, delle statistiche e delle innovazioni.
			</p>
		</div>

		<div class="flex flex-col items-center md:flex-row mb-8">
			<div class="w-full md:w-3/5">
				<h3 class="text-3xl font-semibold mb-4">Il nostro progetto</h3>

				<p class="text-lg mb-4">
					Offrire ai Fantallenatori un consigliere, un AI che somigli all'amico a cui chiedere
					consiglio il giovedì sera davanti ad una birra su che calciatore schierare o su chi
					comprare all'asta.
					<br />
					L'attuale versione, presenta la bozza della nostra vera e propria prima release. Prossimamente,
					sarà disponibile una piattaforma con varie funzionalità tra cui:
					<br />
					<li>
						<strong>Statistiche calciatori comprese di grafici</strong> raggruppati per gruppo di giornate
					</li>
					<li>Valutazione Rosa: <strong>carichi la tua rosa e ti generiamo uno score</strong></li>
					<br />
					<li>
						Voice suggestions: se le immagini e i testi non bastano, potrai <strong
							>chiedere al FantaBalùnBot consigli direttamente a voce!</strong
						>
					</li>
					<br />
					<li>
						<strong>Statistiche dettagliate dei team </strong>
					</li>
				</p>
			</div>

			<div class="w-full md:w-2/5 flex justify-center">
				<img src={fantabalun} alt="About Us" class="h-auto rounded-lg shadow-lg" />
			</div>
		</div>

		<div class=" mb-8">
			<h4 class="text-3xl font-semibold mb-4">La nostra filosofia</h4>

			<p class="text-lg mb-4">
				L'amico che ne sa, ma che non pretende di aver sempre ragione, perché il fantacalcio è arte
				e improvvisazione, oltre che strategia. E noi, oltre ai buoni consigli, vogliamo portare
				fortuna!
			</p>
		</div>

		<div class="text-section mb-8 italic text-center">
			<p class="text-lg">
				Usiamo Nuvolaris come piattaforma, il serverless come filosofia. Se vuoi unirti a noi<br />

				<JoinCta />
			</p>
		</div>
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
