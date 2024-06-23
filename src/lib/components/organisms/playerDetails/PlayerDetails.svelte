<script lang="ts">
	import PlayerCard from '$lib/components/atoms/playerCard/PlayerCard.svelte';
	import { getAiOpinionFromBackend } from '$lib/service/aiOpinion';
	import { getStatsDataById } from '$lib/service/getStats';
	import { openChatWithMessage } from '$lib/store/store';
	import { onMount } from 'svelte';

	export let playerId: number | undefined;
	let playerData;
	let opinion = '';

	let cardRow: any[] = [];

	const openAIpinion = async () => {
		const message = await getAiOpinionFromBackend(playerData);

		console.log('🔎 [PlayerDetails][message] =>', message);
		openChatWithMessage(message);
	};

	onMount(async () => {
		if (playerId) {
			const data = await getStatsDataById(playerId);
			playerData = data;
			cardRow = [
				{
					label: 'Presenze',
					value: playerData?.caps
				},
				{
					label: 'Assist',
					value: playerData?.assists
				},
				{
					label: 'Goal',
					value: playerData?.markavg
				},
				{
					label: 'Media',
					value: playerData?.fmarkavg
				},
				{
					label: 'Cartellini',
					subRows: [
						{
							label: '🟥',
							value: playerData?.rcards
						},
						{
							label: '🟨',
							value: playerData?.ycards
						}
					]
				}
			];
		}
	});
</script>

{#if playerId}
	<div class="player-details">
		{#if !playerData}
			<p>Caricamento...</p>
		{:else if playerData}
			<PlayerCard {playerData} showAiOpinion {cardRow} />
		{/if}

		<p>{opinion}</p>
	</div>
{/if}
