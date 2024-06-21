<script lang="ts">
	import { getAiOpinionFromBackend } from '$lib/service/aiOpinion';
	import type { PlayersStats } from '$lib/service/getStats';
	import Button from '../button/button.svelte';
	import Loader from '../Loader.svelte';

	interface ICardRowProps {
		label?: string;
		value?: string;
	}

	export let showAiOpinion: boolean = false;
	export let playerData: PlayersStats | undefined = undefined;
	export let cardRow: { label?: string; value?: string; subRows?: ICardRowProps[] }[] = [];

	let aiOpinion: string;
	let aiOpinionWritingEffect: string;
	let isLoading = false;

	const getAiOpinion = async () => {
		if (!playerData) return;

		isLoading = true;
		aiOpinion = await getAiOpinionFromBackend(playerData);
		showMessage();
		isLoading = false;
	};

	const showMessage = async () => {
		for (let i = 0; i < aiOpinion.length; i++) {
			aiOpinionWritingEffect = aiOpinion.substring(0, i + 1);
			await sleep(30);
		}
	};

	const sleep = async (ms: number) => {
		return new Promise((resolve) => setTimeout(resolve, ms));
	};

	console.log('🔎 [PlayerCard][playerData] =>', playerData);
</script>

<div class="player-card flex flex-col w-[300px]">
	<div class="card-title py-2">{playerData?.name}</div>

	<div class="card-profile-img grow-1">
		<img src="" alt={playerData?.name} />
	</div>

	<div class="card-stats flex flex-col">
		{#each cardRow as card}
			<div class="flex grow card-row">
				<span class="flex w-[50%] px-3 py-1">{card?.label}</span>

				{#if card?.subRows && card?.subRows?.length > 0}
					<span class="flex w-[50%] px-3 py-1 gap-2">
						{#each card?.subRows as subRow}
							<div class="flex grow">{subRow?.label}</div>

							<div class="flex grow">{subRow?.value}</div>
						{/each}
					</span>
				{:else}
					<span class="flex w-[50%] px-3 py-1">{card?.value}</span>
				{/if}
			</div>
		{/each}
	</div>
</div>

{#if showAiOpinion}
	<div class="flex flex-col justify-center items-center mt-5 w-[300px] gap-2">
		<h5>Vuoi un parere?</h5>

		<p>Chiedi una AIPinion</p>

		{#if !aiOpinion && !isLoading}
			<Button label="AIpinion" onClick={getAiOpinion} />
		{/if}

		{#if isLoading}
			<Loader />
		{/if}

		{#if aiOpinionWritingEffect && !isLoading}
			<hr />

			<div class="aipinion-text flex flex-col w-full p-[2px] mt-3 text-center gap-2">
				{aiOpinionWritingEffect}
			</div>
		{/if}
	</div>
{/if}

<style>
	.player-card {
		border: solid 2px rgb(var(--primary));
		border-radius: 1rem;
		overflow: hidden;
		font-family: 'Francois One', sans-serif;
	}

	.player-card .card-title {
		background: rgb(var(--primary));
	}

	.card-stats {
		width: 100%;
	}

	.card-profile-img {
		display: flex;
		width: 100%;
		min-height: 150px;
	}

	.card-profile-img img {
		display: flex;
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.card-stats span {
		border-top: solid 1px rgb(var(--primary));
	}

	.card-stats span:nth-child(even) {
		border-left: solid 1px rgb(var(--primary));
	}

	.card-row .card {
		min-width: 8px;
		min-height: 12px;
		border-radius: 3px;
	}

	.card-row .card-red {
		background: #f00;
	}

	.card-row .card-yellow {
		background: rgb(234, 255, 0);
	}

	.aipinion-text {
		max-height: 200px;
		overflow: auto;
	}
</style>
