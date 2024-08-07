<script lang="ts">
	import Button from '$lib/components/atoms/button/button.svelte';
	import Loader from '$lib/components/atoms/Loader.svelte';
	import Select from '$lib/components/atoms/select/Select.svelte';
	import CardsSlider from '$lib/components/atoms/sliders/CardsSlider.svelte';
	import { getAiLineupOpinion } from '$lib/service/ai/aiLineup';
	import type { ISliderDataProps } from '$lib/service/fantaicalcio/getStats';
	import { getLineUp, type FootballMatch } from '$lib/service/fantamaster/lineUp';
	import { marked } from 'marked';
	import { onMount } from 'svelte';

	let lineUp: FootballMatch | undefined = undefined;
	let selectOptions: { value: string; label: string }[] = [];
	let selectedOption: string = '';
	let homeLineup: ISliderDataProps[] = [];
	let awayLineup: ISliderDataProps[] = [];
	let aiOpinionLoading = false;
	let aiOpinionDesc: string = '';
	let aiPresentationWritingEffect: string = '';
	let isLineUpLoading = false;

	onMount(async () => {
		isLineUpLoading = true;
		lineUp = await getLineUp();

		if (lineUp && Array.isArray(lineUp.lineups)) {
			selectOptions = lineUp.lineups.map((lineup, index) => ({
				value: String(index),
				label: `${lineup.home} - ${lineup.away}`
			}));

			if (selectOptions.length > 0) {
				selectedOption = selectOptions[0].value;
				updateLineups(Number(selectedOption));
			}
		}

		isLineUpLoading = false;
	});

	async function updateLineups(optionIndex: number) {
		homeLineup = lineUp?.lineups[optionIndex].fm.home_lineup.map((e) => ({ name: e.player })) || [];
		awayLineup = lineUp?.lineups[optionIndex].fm.away_lineup.map((e) => ({ name: e.player })) || [];
		aiPresentationWritingEffect = ''; // Reset AI presentation text
	}

	async function handleAiOpinion() {
		aiOpinionLoading = true;
		aiOpinionDesc = await getAiLineupOpinion((lineUp?.lineups || [])[Number(selectedOption)]);
		await showMessage(aiOpinionDesc);
		aiOpinionLoading = false;
	}

	async function showMessage(description: string) {
		for (let i = 0; i < description.length; i++) {
			aiPresentationWritingEffect = marked.parse(description.substring(0, i + 1));
			await sleep(25);
		}
	}

	function sleep(ms: number) {
		return new Promise((resolve) => setTimeout(resolve, ms));
	}

	function handleSelectChange(event: CustomEvent) {
		selectedOption = event.detail.value;
		aiPresentationWritingEffect = ''; // Reset AI presentation text
		updateLineups(Number(selectedOption));
	}
</script>

{#if isLineUpLoading}
	<Loader />
{:else}
	<div class="flex flex-col items-center justify-center gap-5">
		<h2>Giornata n.{lineUp?.day} di Serie A!</h2>

		{#if lineUp && Array.isArray(lineUp.lineups)}
			<Select
				options={selectOptions}
				label="Seleziona squadre"
				id="match-select"
				name="match"
				bind:selectedValue={selectedOption}
				on:change={handleSelectChange}
			/>
		{/if}

		{#if lineUp && Array.isArray(lineUp.lineups)}
			<div class="flex justify-center items-center gap-6 w-full flex-wrap">
				<div class="flex flex-col grow items-center w-2/5 gap-6 min-w-[550px]">
					<h4>Formazione di casa: <b>{lineUp?.lineups[Number(selectedOption)].home}</b></h4>

					<CardsSlider sliderData={homeLineup} />
				</div>

				<div class="flex flex-col grow items-center w-2/5 gap-6">
					<h4>Formazione ospite: <b>{lineUp?.lineups[Number(selectedOption)].away}</b></h4>

					<CardsSlider sliderData={awayLineup} />
				</div>
			</div>
		{/if}

		<div class="flex flex-col items-center justify-center gap-10 max-w-screen-lg">
			{#if aiOpinionLoading && !aiPresentationWritingEffect}
				<Loader />
			{:else}
				<Button label="I consigli dell'AI" onClick={handleAiOpinion} />
			{/if}

			{#if aiPresentationWritingEffect}
				<p>{@html aiPresentationWritingEffect}</p>
			{/if}
		</div>
	</div>
{/if}
