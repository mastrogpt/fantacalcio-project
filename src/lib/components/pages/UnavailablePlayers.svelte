<script lang="ts">
	import { onMount } from 'svelte';
	import { getUnavailablePlayers } from '$lib/service/getPlayers';
	import type { UnavailablePlayers } from '$lib/service/getPlayers';
	import Loader from '$lib/components/atoms/Loader.svelte';
	import ArrowDown from '$lib/components/atoms/icons/ArrowDown.svelte';
	import ArrowUp from '../atoms/icons/ArrowUp.svelte';

	interface Element {
		[key: string]: any;
	}
	let unavailabilityInfo: UnavailablePlayers[];

	let currentPage = 1;
	let pageSize = 11;
	let totalPages = 1;

	onMount(async () => {
		unavailabilityInfo = await getUnavailablePlayers();
		totalPages = Math.ceil(unavailabilityInfo.length / pageSize);
	});

	let sortBy = { col: 'team', ascending: true };

	$: sortUnavailable = (column: string) => {
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

		unavailabilityInfo = unavailabilityInfo.sort(sort);
	};

	$: paginatedunavailabilityInfo = unavailabilityInfo
		? unavailabilityInfo.slice((currentPage - 1) * pageSize, currentPage * pageSize)
		: [];
</script>

<div class="grid grid-cols-1 gap-2 lg:gap-8 mx-auto justify-center sm:w-auto">
	<div class="h-32 rounded-lg lg:col-span-2">
		<div class="overflow-x-auto rounded-t-lg">
			<h2 class="text-center mb-5">Gli indisponibili</h2>
			<div>
				{#if unavailabilityInfo && unavailabilityInfo.length > 0}
					<div class="overflow-x-auto">
						<table class="min-w-full divide-y-2 divide-gray-200 bg-white text-sm">
							<thead class="ltr:text-left rtl:text-right">
								<tr>
									<th
										on:click={() => sortUnavailable('team')}
										class="whitespace-nowrap p-2 font-medium text-primary font-bold text-xl text-left"
									>
										Squadra
									</th>
									<th
										on:click={() => sortUnavailable('name')}
										class="whitespace-nowrap p-2 font-medium text-primary font-bold text-xl text-left"
									>
										Nome
										{#if sortBy.ascending}
											<ArrowUp />
										{:else}
											<ArrowDown />
										{/if}
									</th>
									<th
										class="whitespace-nowrap p-2 font-medium text-primary font-bold text-xl text-left hidden sm:table-cell"
										>Info</th
									>
									<th
										on:click={() => sortUnavailable('role')}
										class="whitespace-nowrap p-2 font-medium text-primary font-bold text-xl text-left"
									>
										Ruolo
									</th>
									<th
										on:click={() => sortUnavailable('doubt')}
										class="whitespace-nowrap p-2 font-medium text-primary font-bold text-xl text-left"
									>
										Dubbio
									</th>
								</tr>
							</thead>
							<tbody class="divide-y divide-gray-200">
								{#each paginatedunavailabilityInfo as player}
									<tr class="border-b">
										<td class="whitespace-nowrap p-2 font-medium text-gray-900">{player.team}</td>
										<td class="whitespace-nowrap p-2 font-medium text-gray-900">{player.name}</td>
										<td
											class="whitespace-normal max-w-[200px] p-2 font-medium text-gray-900 hidden sm:table-cell"
											>{player.desc}</td
										>
										<td class="whitespace-nowrap p-2 font-medium text-gray-900">{player.role}</td>
										<td class="whitespace-nowrap p-2 font-medium text-gray-900">{player.doubt}</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>

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
				{:else}
					<Loader />
				{/if}
			</div>
		</div>
	</div>
</div>
