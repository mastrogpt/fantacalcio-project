<script lang="ts">
	import PlayerCard from '$lib/components/atoms/playerCard/PlayerCard.svelte';
	import { getAiOpinionFromBackend } from '$lib/service/aiOpinion';
	import { getStatsDataById } from '$lib/service/getStats';
	import { openChatWithMessage } from '$lib/store/store';
	import { onMount } from 'svelte';

	export let playerId: number | undefined;
	let playerData;
	let opinion = '';

	const openAIpinion = async () => {
		const message = await getAiOpinionFromBackend(playerData);

		console.log('🔎 [PlayerDetails][message] =>', message);
		openChatWithMessage(message);
	};

	onMount(async () => {
		if (playerId) {
			const data = await getStatsDataById(playerId);
			playerData = data;
		}
	});
</script>

{#if playerId}
	<div class="player-details">
		{#if !playerData}
			<p>Caricamento...</p>
		{:else if playerData}
			<PlayerCard {playerData} />

			<!-- <div class="header">
				<h2>{playerData?.name}</h2>
			</div>

			<div class="details">
				<p><strong>Caps:</strong> {playerData?.caps}</p>
				<p><strong>Assists:</strong> {playerData?.assists}</p>
				<p><strong>Goals:</strong> {playerData?.goals}</p>
				<p><strong>Markavg:</strong> {playerData?.markavg}</p>
				<p><strong>Fmarkavg:</strong> {playerData?.fmarkavg}</p>
				<p><strong>Rcards:</strong> {playerData?.rcards}</p>
				<p><strong>Ycards:</strong> {playerData?.ycards}</p>

			</div>

			<div class="actions gap-5">
				<Button label="Compara" onClick={() => console.log('Compare clicked')} />

				<Button label="Aipinion" onClick={openAIpinion} />
			</div> -->
		{/if}

		<p>{opinion}</p>
	</div>
{/if}
