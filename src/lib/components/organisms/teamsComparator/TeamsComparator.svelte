<script lang="ts">
	import Select from '$lib/components/atoms/select/Select.svelte';
	import CardsSlider from '$lib/components/atoms/sliders/CardsSlider.svelte';
	import { getLineUp, type FootballMatch } from '$lib/service/lineUp';
	import { onMount } from 'svelte';

	let lineUp: FootballMatch | undefined = undefined;
	let selectOptions: { value: string; label: string }[] = [];
	let selectedOption: string = '';
	let data: any[] = [];

	onMount(async () => {
		lineUp = await getLineUp();

		if (lineUp && Array.isArray(lineUp.lineups)) {
			selectOptions = lineUp.lineups.map((lineup, index) => ({
				value: String(index),
				label: `${lineup.home} - ${lineup.away}`
			}));

			if (selectOptions.length > 0) {
				selectedOption = selectOptions[0].value;
				updateData(Number(selectedOption));
			}
		}
	});

	function handleSelectChange(event: CustomEvent) {
		selectedOption = event.detail.value;
		updateData(Number(selectedOption));
	}

	function updateData(optionIndex: number) {
		data = lineUp?.lineups[optionIndex].fm.away_lineup.map((e) => ({ title: e.player })) || [];
	}
</script>

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

				<CardsSlider
					sliderData={lineUp?.lineups[Number(selectedOption)].fm.home_lineup.map((e) => {
						return { title: e.player };
					})}
				/>
			</div>

			<div class="flex flex-col grow items-center w-2/5 gap-6">
				<h4>Formazione ospite: <b>{lineUp?.lineups[Number(selectedOption)].away}</b></h4>

				<CardsSlider
					sliderData={lineUp?.lineups[Number(selectedOption)].fm.away_lineup.map((e) => {
						return { title: e.player };
					})}
				/>
			</div>
		</div>
	{/if}
</div>
