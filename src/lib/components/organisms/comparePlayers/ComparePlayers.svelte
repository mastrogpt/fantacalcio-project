<script lang="ts">
	import { getAiComparison } from '$lib/service/ai/aiComparator';
	import { getStatsData } from '$lib/service/fantamaster/getStats';
	import { onMount } from 'svelte';
	import { selectedRows, type Message } from '$lib/store/store';
	import { openChatWithAIMessage, handlePlayerCardOpening } from '$lib/store/store';
	import SpeakingLoader from '$lib/components/atoms/SpeakingLoader.svelte';

	const playersToCompare = [];
	let aiComparsion = '';
	let loading = false;
	let message: Message;

	onMount(async () => {
		loading = true;
		const data = await getStatsData();

		$selectedRows.forEach((row, idx, array) => {
			playersToCompare.push(row);
		});

		aiComparsion = await getAiComparison(playersToCompare);

		message = {
			text: aiComparsion,
			type: 'ai'
		};

		loading = false;
		openChatWithAIMessage(message);

		handlePlayerCardOpening();
	});
</script>

{#if loading}
	<SpeakingLoader />
{/if}
