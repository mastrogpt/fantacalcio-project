<script lang="ts">
	import Loader from '$lib/components/atoms/Loader.svelte';
	import { getAiComparison } from '$lib/service/aiComparator';
	import { getStatsData, getStatsDataById } from '$lib/service/getStats';
	import { selectedRows } from '$lib/store/store';
	import { onMount } from 'svelte';

	const playersToCompare = [];
	let aiComparsion = '';
	let loading = false;

	onMount(async () => {
		loading = true;
		const data = await getStatsData();

		$selectedRows.forEach((row, idx, array) => {
			playersToCompare.push(row);
		});

		aiComparsion = await getAiComparison(playersToCompare);

		loading = false;
	});
</script>

{#if loading}
	<Loader />
{:else}
	<div class="flex flex-col gap-5 text-center max-w-xl">
		<h3>Il verdetto dell'AI</h3>

		<p>
			{aiComparsion}
		</p>
	</div>
{/if}
