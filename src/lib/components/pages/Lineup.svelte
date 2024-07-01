<script lang="ts">
	import Loader from '$lib/components/atoms/Loader.svelte';
	import type { FootballMatch, LineUp } from '$lib/service/lineUp';
	import { getLineUp } from '$lib/service/lineUp';
	import { onMount } from 'svelte';
	import { getAiLineupOpinion } from '$lib/service/aiLineup';
	import GreenButton from '../atoms/buttons/GreenButton.svelte';

	let fMatch: FootballMatch;
	let lineUps: string[] = [];
	let selectedLineUp: number;

	let allInfoAboutThisLineup: LineUp;

	let aiOpinionCharging = false;

	let aiOpinionDesc: string;

	onMount(async () => {
		fMatch = await getLineUp();
		if (fMatch && Array.isArray(fMatch.lineups)) {
			fMatch.lineups.forEach((lineup) => {
				lineUps.push(`${lineup.home} - ${lineup.away}`);
			});
			selectedLineUp = 0;
		}
	});

	async function handleAiOpinion() {
		aiOpinionCharging = true;
		aiOpinionDesc = await getAiLineupOpinion(fMatch.lineups[selectedLineUp]);

		aiOpinionCharging = false;
	}

	function endAiCompareFlux() {
		aiOpinionCharging = false;
		aiOpinionDesc = '';
	}
</script>

<div class="flex items-center justify-center">
	<div class="mx-auto">
		{#if !fMatch}
			<Loader />
		{/if}
		{#if fMatch && Array.isArray(fMatch.lineups)}
			<div class="flex flex-col items-center">
				<div>
					<h1 class="text-3xl font-bold text-primary mb-4">
						Giornata n.<strong>{fMatch.day}</strong> di Serie A!
					</h1>
				</div>
				<div class="p-4">
					<GreenButton text="I consigli dell'AI" clickAction={handleAiOpinion} />
				</div>
				<div class="relative">
					<select
						bind:value={selectedLineUp}
						class="block appearance-none w-full bg-white border border-gray-300 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500 radious"
					>
						{#each lineUps as lineup, index}
							<option value={index}>{lineup}</option>
						{/each}
					</select>
					<div
						class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700"
					>
						<svg
							class="fill-current h-4 w-4"
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 20 20"
						>
							<path
								d="M9.293 14.707a1 1 0 0 0 1.414 0l5-5a1 1 0 0 0-1.414-1.414L10 12.586l-4.293-4.293a1 1 0 1 0-1.414 1.414l5 5z"
							/>
						</svg>
					</div>
				</div>
			</div>
		{/if}
	</div>
</div>

{#if selectedLineUp != null}
	<div class="p-5">
		<div class="grid grid-cols-1 gap-4 lg:grid-cols-2 lg:gap-8">
			<div class="h-70 rounded-lg">
				<h2 class="text-dark">
					Formazione di casa: {fMatch.lineups[selectedLineUp].home}
				</h2>
				<div class="grid grid-cols-1 gap-4 lg:grid-cols-2 lg:gap-8">
					<div class="h-70 rounded-lg">
						<h3 class="text-xl font-bold text-primary">Giocatore</h3>
						{#each fMatch.lineups[selectedLineUp].fm.home_lineup as player}
							<li class="text-base text-primary">{player.player}</li>
						{/each}
					</div>
					<div class="h-70 rounded-lg hidden sm:block">
						<h3 class="text-xl font-bold text-primary">Probabilità</h3>
						{#each fMatch.lineups[selectedLineUp].fm.home_lineup as player}
							<li class="text-base text-primary">{player.prob}</li>
						{/each}
					</div>
				</div>
			</div>
			<div class="h-70 rounded-lg">
				<h2 class="text-dark">
					Formazione ospite: {fMatch.lineups[selectedLineUp].away}
				</h2>
				<div class="grid grid-cols-1 gap-4 lg:grid-cols-2 lg:gap-8">
					<div class="h-70 rounded-lg">
						<h3 class="text-xl font-bold text-primary">Giocatore</h3>
						{#each fMatch.lineups[selectedLineUp].fm.away_lineup as player}
							<li class="text-base text-primary">{player.player}</li>
						{/each}
					</div>
					<div class="h-70 rounded-lg hidden sm:block">
						<h3 class="text-xl font-bold text-primary">Probabilità</h3>
						{#each fMatch.lineups[selectedLineUp].fm.away_lineup as player}
							<li class="text-base text-primary">{player.prob}</li>
						{/each}
					</div>
				</div>
			</div>
		</div>
	</div>
{/if}

{#if aiOpinionCharging}
	<div
		class="fixed bg-gray-100 rounded-2xl border border-blue-100 inset-0 bg-opacity-90 z-50 bg-white p-4 shadow-lg sm:p-6 lg:p-8 overflow-y-auto"
		role="alert"
	>
		<Loader />
	</div>
{/if}
{#if !aiOpinionCharging && aiOpinionDesc}
	<div
		class="fixed bg-gray-100 rounded-2xl border border-blue-100 inset-0 bg-opacity-90 z-50 bg-white p-4 shadow-lg sm:p-6 lg:p-8 overflow-y-auto"
		role="alert"
	>
		<div
			class="flex mt-10 items-center gap-4 mt-10 bg-gradient-to-r from-gray-100 via-gray-200 to-gray-300"
		>
			<p class="text-2xl font-extrabold sm:text-lg text-primary justify-center text-center">
				I consigli dell'AI:
			</p>
		</div>

		<div class="grid grid-cols-1 overflow-y: auto">
			<p class="mt-4 text-xl text-primary bg-gray-100">
				{aiOpinionDesc}
			</p>

			<div class="mt-6">
				<GreenButton text="Ho capito" clickAction={endAiCompareFlux} />
			</div>
		</div>
	</div>
{/if}
