<script lang="ts">
	import CardsSlider from '$lib/components/atoms/sliders/CardsSlider.svelte';
	import { getLineUp, type FootballMatch } from '$lib/service/lineUp';
	import { onMount } from 'svelte';

	let lineUp: FootballMatch | undefined = undefined;
	let selectOptions: string[] = [];
	let optionSelected: number = 0;
	let data: any[] = [];

	onMount(async () => {
		lineUp = await getLineUp();

		if (lineUp && Array.isArray(lineUp.lineups)) {
			lineUp.lineups.forEach((lineup) => {
				selectOptions.push(`${lineup.home} - ${lineup.away}`);
			});
		}

		data = lineUp.lineups[optionSelected].fm.away_lineup.map((e) => ({ title: e.player }));
	});
</script>

<div class="flex flex-col items-center justify-center gap-5">
	<h2>Giornata n.{lineUp?.day} di Serie A!</h2>

	{#if lineUp && Array.isArray(lineUp.lineups)}
		<div class="relative w-[250px]">
			<select
				bind:value={optionSelected}
				class="block appearance-none w-full bg-white border border-gray-300 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500 radious"
			>
				{#each selectOptions as lineup, index}
					<option value={index}>{lineup}</option>
				{/each}
			</select>
			<div
				class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700"
			>
				<svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
					<path
						d="M9.293 14.707a1 1 0 0 0 1.414 0l5-5a1 1 0 0 0-1.414-1.414L10 12.586l-4.293-4.293a1 1 0 1 0-1.414 1.414l5 5z"
					/>
				</svg>
			</div>
		</div>
	{/if}

	{#if lineUp && Array.isArray(lineUp.lineups)}
		<div class="flex justify-center items-center gap-6 w-[100%] flex-wrap">
			<div class="flex flex-col grow-1 items-center w-[45%] gap-6 min-w-[550px]">
				<h4>Formazione di casa: <b>{lineUp?.lineups[optionSelected].home}</b></h4>

				<CardsSlider
					sliderData={lineUp.lineups[optionSelected].fm.away_lineup.map((e) => {
						return { title: e.player };
					})}
				/>
			</div>

			<div class="flex flex-col grow-1 items-center w-[45%] gap-6">
				<h4>Formazione ospite: <b>{lineUp?.lineups[optionSelected].away}</b></h4>

				<CardsSlider
					sliderData={lineUp.lineups[optionSelected].fm.away_lineup.map((e) => {
						return { title: e.player };
					})}
				/>
			</div>
		</div>
	{/if}
</div>

<style></style>
