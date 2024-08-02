<script lang="ts">
	import { getStatsData } from '$lib/service/fantamaster/getStats';
	import { onMount } from 'svelte';
	import { nuvbotChat, selectedRows } from '$lib/store/store';
	import { handleNuvBotChatOpening, handlePlayerCardOpening } from '$lib/store/store';
	import SpeakingLoader from '$lib/components/atoms/SpeakingLoader.svelte';
	import type { ChatInput } from '$lib/service/nuvBot';

	const playersToCompare = [];
	let aiComparsion = '';
	let loading = false;
	let message: ChatInput;

	onMount(async () => {
		loading = true;
		const data = await getStatsData();

		$selectedRows.forEach((row, idx, array) => {
			playersToCompare.push(row);
		});

		message = {
			message: 'Mi fai un confronto tra questi due?' + JSON.stringify(playersToCompare)
		};

		aiComparsion = await nuvbotChat(message);

		loading = false;
		handleNuvBotChatOpening(true);

		handlePlayerCardOpening();
	});
</script>

{#if loading}
	<SpeakingLoader />
{/if}
