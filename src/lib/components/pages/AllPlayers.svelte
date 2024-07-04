<script lang="ts">
	import { onMount } from 'svelte';
	import { getPlayersList } from '$lib/service/fantaicalcio/getPlayers';
	import type { PlayersList } from '$lib/service/fantaicalcio/getPlayers';
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

	onMount(async () => {
		players = await getPlayersList();
		totalPages = Math.ceil(players.length / pageSize);
	});

	let sortBy = { col: 'team', ascending: true };

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

<svelte:head>
	<title>MastroGPT - Fantamaster</title>
	<meta name="og:title" content="MastroGPT" />
</svelte:head>

<div class="m-4">
	<div class="grid grid-cols-1 gap-4 lg:gap-8 mx-auto justify-center sm:w-auto">
		<div class="h-32 rounded-lg lg:col-span-2">
			<h2 class="text-center mb-5">Tutti i giocatori</h2>
			{#if players}
				<div class="overflow-x-auto">
					<table class="min-w-full divide-y-2 divide-gray-200 bg-white text-sm sm:w-auto">
						<thead class="ltr:text-left rtl:text-right">
							<tr>
								<th
									class="whitespace-nowrap p-2 font-medium text-primary font-bold text-xl text-left"
									on:click={() => sortAll('name')}
								>
									<span>Name</span>
									{#if sortBy.ascending}
										<ArrowUp />
									{:else}
										<ArrowDown />
									{/if}
								</th>

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
									>Disponibile</th
								>
							</tr>
						</thead>
						<tbody class="divide-y divide-gray-200">
							{#each paginatedPlayers as player}
								<tr class="border-b">
									<td class="whitespace-nowrap p-2 font-medium text-gray-900">{player?.name}</td>

									<td class="whitespace-nowrap p-2 font-medium text-gray-900">{player?.position}</td
									>
									<td class="whitespace-nowrap p-2 font-medium text-gray-900">{player?.team}</td>
									<td class="whitespace-nowrap p-2 font-medium text-gray-900"
										>{player?.available}</td
									>

									<td class="whitespace-nowrap p-2 font-medium text-gray-900">
										<GreenButton href="/stats/{player.id}" text="Dati" />
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
							on:click={() => (currentPage = Math.min(totalPages, currentPage + 1))}
							>Next &gt;</button
						>
					</div>
				</div>
			{:else}
				<Loader />
			{/if}
		</div>
	</div>
</div>
