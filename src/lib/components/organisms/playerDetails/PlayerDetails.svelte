<script lang="ts">
	import Loader from '$lib/components/atoms/Loader.svelte';
	import PlayerCard from '$lib/components/atoms/playerCard/PlayerCard.svelte';
	import { getStatsDataById } from '$lib/service/fantaicalcio/getStats';
	import { onMount } from 'svelte';

	export let player_id: number;
	export let season_id: number;
	export let team_id: number;

	let playerData;
	let opinion = '';

	let cardRow: any[] = [];

	onMount(async () => {
		if (player_id) {
			const data = await getStatsDataById(player_id, season_id, team_id);
			playerData = data;
			let playerStats = data?.player_statistic;

			cardRow = [
				{
					label: 'Presenze',
					value: playerStats?.games_appearences ? playerStats?.games_appearences : '0'
				},
				{
					label: 'Assist',
					value: playerStats?.goals_assists ? playerData?.goals_assists : '0'
				},
				{
					label: 'Goal',
					value: playerStats?.goals_total ? playerStats?.goals_total : '0'
				},
				{
					label: 'Media',
					value: playerStats?.rating ? playerStats?.rating.toFixed(2) : '0'
				},
				{
					label: 'Cartellini',
					subRows: [
						{
							label: '🟥',
							value: playerStats?.cards_red ? playerStats?.cards_red : '0'
						},
						{
							label: '🟨',
							value: playerStats?.cards_yellow ? playerStats?.cards_yellow : '0'
						}
					]
				}
			];
		}
	});
</script>

{#if player_id}
	<div class="player-details">
		{#if !playerData}
			<p><Loader /></p>
		{:else if playerData}
			<PlayerCard {playerData} showAiOpinion {cardRow} />
		{/if}

		<p>{opinion}</p>
	</div>
{/if}
