<script lang="ts">
	import { onMount } from 'svelte';
	import { getPlayersList } from '$lib/service/getPlayers';
	import { getAiComparison } from '$lib/service/aiComparator';
	import { getStatsDataById } from '$lib/service/getStats';

	import type { PlayersList } from '$lib/service/getPlayers';
	import Loader from '$lib/components/atoms/Loader.svelte';
	import ArrowDown from '$lib/components/atoms/icons/ArrowDown.svelte';
	import ArrowUp from '../atoms/icons/ArrowUp.svelte';
	import GreenButton from '../atoms/buttons/GreenButton.svelte';

	interface Element {
		[key: string]: any;
	}
	let players: PlayersList;
	let currentPage = 1;
	let pageSize = 11;
	let totalPages = 1;

	let firstPlayer: any;
	let secondPlayer: any;

	let showAiComparatorBox = false;
	let aiOpinionCharging = false;
	let aiComparisonDescription: string;

	let comparisonConcluded = false;

	onMount(async () => {
		players = await getPlayersList();
		totalPages = Math.ceil(players.length / pageSize);
	});

	let sortBy = { col: 'team', ascending: true };
	let showModalCompare = false;

	function compareGetFirst(player1: object) {
		comparisonConcluded = false;
		firstPlayer = player1;
		showModalCompare = true;
	}

	function compareGetSecond(player2: object) {
		secondPlayer = player2;
		showModalCompare = false;
		askAiOpinion();
	}

	function endAiCompareFlux() {
		comparisonConcluded = true;
		firstPlayer = null;
		secondPlayer = null;
		aiOpinionCharging = false;
		showAiComparatorBox = false;
	}

	async function askAiOpinion() {
		showAiComparatorBox = true;
		aiOpinionCharging = true;

		let input = Array.of(
			await getStatsDataById(firstPlayer.id),
			await getStatsDataById(secondPlayer.id)
		);
		aiComparisonDescription = await getAiComparison(input);
		aiOpinionCharging = false;
	}

	$: sortAll = (column: string) => {
		if (sortBy.col == column) {
			sortBy.ascending = !sortBy.ascending;
		} else {
			sortBy.col = column;
			sortBy.ascending = true;
		}

		let sortModifier = sortBy.ascending ? 1 : -1;

		const sort = (a: Element, b: Element) => {
			const aValue = a[column];
			const bValue = b[column];

			if (aValue < bValue) {
				return -1 * sortModifier;
			} else if (aValue > bValue) {
				return 1 * sortModifier;
			} else {
				return 0;
			}
		};

		players = players.sort(sort);
	};

	$: paginatedPlayers = players
		? players.slice((currentPage - 1) * pageSize, currentPage * pageSize)
		: [];
</script>

<div class="grid grid-cols-1 gap-4 lg:gap-8 mx-auto justify-center sm:w-auto">
	<div class="h-32 rounded-lg lg:col-span-2">
		<h2 class="text-2xl text-primary font-bold text-center mb-5">Tutti i giocatori</h2>
		{#if players}
			<div class="overflow-x-auto">
				<table class="min-w-full divide-y-2 divide-gray-200 bg-white text-sm">
					<thead class="ltr:text-left rtl:text-right">
						<tr>
							<th
								on:click={() => sortAll('name')}
								class="whitespace-nowrap p-2 font-medium text-primary font-bold text-xl text-left"
								>Nome
								{#if sortBy.ascending}
									<ArrowUp />
								{:else}
									<ArrowDown />
								{/if}
							</th>
							<th
								class="whitespace-nowrap p-2 font-medium text-primary text-xl font-bold text-left hidden sm:table-cell"
								>Playmaker</th
							>
							<th
								class="whitespace-nowrap p-2 font-medium text-primary font-bold text-xl text-left hidden sm:table-cell"
								>Ruolo</th
							>
							<th
								on:click={() => sortAll('team')}
								class="whitespace-nowrap p-2 font-medium text-primary font-bold text-xl text-left"
								>Squadra</th
							>
							<th
								on:click={() => sortAll('value')}
								class="whitespace-nowrap p-2 font-medium text-primary font-bold text-xl text-left hidden sm:table-cell"
								>Valore</th
							>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200">
						{#each paginatedPlayers as player}
							<tr class="border-b">
								<td class="whitespace-nowrap p-2 font-medium text-gray-900">{player.name}</td>
								<td class="whitespace-nowrap p-2 font-medium text-gray-900 hidden sm:table-cell"
									>{player.playmaker ? 'Yes' : 'No'}</td
								>
								<td class="whitespace-nowrap p-2 font-medium text-gray-900 hidden sm:table-cell"
									>{player.role}</td
								>
								<td class="whitespace-nowrap p-2 font-medium text-gray-900">{player.team}</td>
								<td class="whitespace-nowrap p-2 font-medium text-gray-900 hidden sm:table-cell"
									>{player.value}</td
								>
								<td class="whitespace-nowrap p-2 font-medium text-gray-900">
									<GreenButton clickAction={() => compareGetFirst(player)} text="Compara" />
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
				<div class="flex justify-center mt-4 font-bold text-primary">
					<button class="mr-2" on:click={() => (currentPage = Math.max(1, currentPage - 1))}
						>&lt; Previous</button
					>
					<button
						class="ml-2"
						on:click={() => (currentPage = Math.min(totalPages, currentPage + 1))}>Next &gt;</button
					>
				</div>
			</div>
		{:else}
			<Loader />
		{/if}
	</div>

	{#if showModalCompare}
		<div
			class="fixed bg-gray-100 rounded-2xl border border-blue-100 inset-0 bg-opacity-80 z-50 bg-white p-4 shadow-lg sm:p-6 lg:p-8"
			role="alert"
		>
			<div class="flex items-center gap-4">
				<p class="font-medium text-2xl text-primary font-semibold sm:text-lg">
					Con chi vuoi comparare <strong>{firstPlayer.name}</strong> ?
				</p>
			</div>

			<div class="overflow-x-auto">
				<table class="min-w-full divide-y-2 divide-gray-200 bg-gray-200 text-sm">
					<thead class="ltr:text-left rtl:text-right">
						<tr>
							<th
								on:click={() => sortAll('name')}
								class="whitespace-nowrap p-2 font-medium text-primary font-bold text-xl text-left"
								>Nome</th
							>
							<th
								class="whitespace-nowrap p-2 font-medium text-primary text-xl font-bold text-left hidden sm:table-cell"
								>Playmaker</th
							>

							<th
								on:click={() => sortAll('team')}
								class="whitespace-nowrap p-2 font-medium text-primary font-bold text-xl text-left"
								>Squadra</th
							>
							<th
								on:click={() => sortAll('value')}
								class="whitespace-nowrap p-2 font-medium text-primary font-bold text-xl text-left hidden sm:table-cell hidden sm:table-cell hidden sm:table-cell"
								>Valore</th
							>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200">
						{#each paginatedPlayers as player}
							{#if player.role == firstPlayer.role && player.name != firstPlayer.name}
								<tr class="border-b">
									<td class="whitespace-nowrap p-2 font-medium text-gray-900">{player.name}</td>
									<td class="whitespace-nowrap p-2 font-medium text-gray-900 hidden sm:table-cell"
										>{player.playmaker ? 'Yes' : 'No'}</td
									>

									<td class="whitespace-nowrap p-2 font-medium text-gray-900">{player.team}</td>
									<td class="whitespace-nowrap p-2 font-medium text-gray-900 hidden sm:table-cell"
										>{player.value}</td
									>
									<td class="whitespace-nowrap p-2 font-medium text-gray-900">
										<GreenButton clickAction={() => compareGetSecond(player)} text="Conferma" />
									</td>
								</tr>
							{/if}
						{/each}
					</tbody>
				</table>
				<div class="flex justify-center mt-4 font-bold text-primary">
					<button class="mr-2" on:click={() => (currentPage = Math.max(1, currentPage - 1))}
						>&lt; Previous</button
					>
					<button
						class="ml-2"
						on:click={() => (currentPage = Math.min(totalPages, currentPage + 1))}>Next &gt;</button
					>
				</div>
			</div>
		</div>
	{/if}

	{#if showAiComparatorBox && !comparisonConcluded}
		<div
			class="fixed bg-gray-100 rounded-2xl border border-blue-100 inset-0 bg-opacity-90 z-50 bg-white p-4 shadow-lg sm:p-6 lg:p-8 overflow-y-auto"
			role="alert"
		>
			{#if aiOpinionCharging}
				<Loader />
			{:else}
				<div
					class="flex mt-10 items-center gap-4 mt-10 bg-gradient-to-r from-gray-100 via-gray-200 to-gray-300"
				>
					<p class="text-2xl font-extrabold sm:text-lg text-primary justify-center text-center">
						Il verdetto dell'AI:
					</p>
				</div>

				<div class="grid grid-cols-1 overflow-y: auto">
					<p class="mt-4 text-xl text-primary bg-gray-100">
						{aiComparisonDescription}
					</p>

					<div class="mt-6">
						<GreenButton text="Ho capito" clickAction={endAiCompareFlux} />
					</div>
				</div>
			{/if}
		</div>
	{/if}
</div>
