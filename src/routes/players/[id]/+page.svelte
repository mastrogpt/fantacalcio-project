<script lang="ts">
	import Loader from '$lib/components/atoms/Loader.svelte';
	import PlayerCard from '$lib/components/atoms/playerCard/PlayerCard.svelte';
	import ArticlesSlider from '$lib/components/atoms/sliders/ArticlesSlider.svelte';
	import { getArticlesList } from '$lib/service/fantaicalcio/getArticles';
	import { getStatsDataById, type PlayerCompleteStats } from '$lib/service/fantaicalcio/getStats';
	import { onMount } from 'svelte';

	let playerData: PlayerCompleteStats | undefined = undefined;

	onMount(async () => {
		const urlParams = new URLSearchParams(window.location.search);
		const player_id = Number(urlParams.get('player_id'));
		const season_id = Number(urlParams.get('season_id'));
		const team_id = Number(urlParams.get('team_id'));

		if (player_id) {
			const data = await getStatsDataById(player_id, season_id, team_id, true);

			playerData = data;
		}
	});

	const sleep = async (ms: number) => {
		return new Promise((resolve) => setTimeout(resolve, ms));
	};
</script>

<section class="flex flex-col items-center justify-center">
	<div
		class="container flex items-center justify-center flex-col flex-1 bg-primary my-10 rounded-[20px] gap-[20px]"
	>
		<div class="flex items-center justify-center max-w-[650px] w-[100%] gap-10 py-20 flex-wrap">
			<div class="flex">
				<PlayerCard imageUrl={playerData?.player?.photo} />
			</div>

			<div class="flex flex-col flex-1 gap-10">
				<h2 class="text-upper">{playerData?.player?.name}</h2>

				<div class="flex flex-1 gap-4 flex-wrap">
					<div
						class="flex flex-col flex-1 gap-[2px] min-w-[150px] text-center rounded-[10px] py-2 px-10 bg-accent"
					>
						<h5>Squadra</h5>
						<p>{playerData?.team}</p>
					</div>
					<div
						class="flex flex-col flex-1 gap-[2px] min-w-[150px] text-center rounded-[10px] py-2 px-10 bg-accent"
					>
						<h5>Data di nascita</h5>
						<p>{playerData?.player?.birth_date}</p>
						<small>
							{new Date().getFullYear() - new Date(playerData?.player?.birth_date).getFullYear()} anni
						</small>
					</div>
					<div
						class="flex flex-col flex-1 gap-[2px] min-w-[150px] text-center rounded-[10px] py-2 px-10 bg-accent"
					>
						<h5>Minuti giocati</h5>
						<p>
							{playerData?.player_statistic?.find((e) => e.label === 'Minuti di gioco').value}
							min
						</p>
					</div>
					<div
						class="flex flex-col flex-1 gap-[2px] min-w-[150px] text-center rounded-[10px] py-2 px-10 bg-accent"
					>
						<h5>Presenze</h5>
						{playerData?.player_statistic?.find((e) => e.label === 'Presenze').value}
					</div>
				</div>
			</div>
		</div>

		<div
			class="flex flex-col gap-[20px] border-[1px] border-accent w-[80%] rounded-[10px] p-[20px]"
		>
			<h4>Statistiche</h4>

			<hr />

			{#if playerData?.player_statistic}
				<div class="flex flex-wrap gap-[30px]">
					{#each playerData?.player_statistic as spec}
						<div
							class="flex flex-col flex-1 min-w-[200px] gap-[2px] text-center rounded-[10px] py-2 px-10 bg-accent"
						>
							<h5>{spec.label}</h5>
							<small>{spec.value}</small>
						</div>
					{/each}
				</div>
			{/if}
		</div>

		<hr />
	</div>

	<div class="flex flex-col gap-[10px] container">
		<h4>Articoli correlati</h4>

		<div class="flex my-10">
			{#await getArticlesList()}
				<Loader />
			{:then data}
				{#if data.filter((e) => e.tag.includes('Alessandro Aleotti')).length > 0}
					<ArticlesSlider data={data.filter((e) => e.tag.includes('Alessandro Aleotti'))} />
				{:else}
					<h5>Non ci sono notizie riguardanti {playerData?.player?.name}</h5>
				{/if}
			{/await}
		</div>
	</div>
</section>

<style>
</style>
