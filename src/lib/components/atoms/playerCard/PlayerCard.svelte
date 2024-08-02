<script lang="ts">
	import type { PlayerCompleteStats } from '$lib/service/fantaicalcio/getStats';
	import Button from '../button/button.svelte';
	import imgFallback from '$lib/assets/player-img-fallback.jpeg';
	import { marked } from 'marked';
	import { goto } from '$app/navigation';
	import { handleNuvBotChatOpening, handlePlayerCardOpening, nuvbotChat } from '$lib/store/store';
	import type { Message } from '$lib/store/store';
	import SpeakingLoader from '../SpeakingLoader.svelte';
	import type { ChatInput } from '$lib/service/nuvBot';

	interface ICardRowProps {
		label?: string;
		value?: string;
	}

	export let showAiOpinion: boolean = false;
	export let playerData: PlayerCompleteStats | undefined = undefined;
	export let name: string = '';
	export let imageUrl: string = '';
	export let cardRow: { label?: string; value?: string; subRows?: ICardRowProps[] }[] = [];
	export let redirect: boolean = false;
	export let player_id: number | undefined = undefined;
	export let season_id: number | undefined = undefined;
	export let team_id: number | undefined = undefined;

	let aiOpinion: string;
	let aiOpinionWritingEffect: string | Promise<string>;
	let isLoading = false;

	let aiMessage: Message;
	let userMessage: ChatInput;

	const getAiOpinion = async () => {
		if (!playerData) return;

		isLoading = true;
		userMessage = {
			message: ('mi dai un parere su questo calciatore? ' + JSON.stringify(playerData)) as string
		};
		aiOpinion = await nuvbotChat(userMessage);
		handlePlayerCardOpening();

		aiMessage = {
			text: aiOpinion,
			type: 'ai'
		};

		handleNuvBotChatOpening(true);
		isLoading = false;
	};

	const showMessage = async () => {
		for (let i = 0; i < aiOpinion.length; i++) {
			aiOpinionWritingEffect = marked.parse(aiOpinion.substring(0, i + 1));
			await sleep(30);
		}
	};

	const sleep = async (ms: number) => {
		return new Promise((resolve) => setTimeout(resolve, ms));
	};

	const goToPlayerhandler = () => {
		if (!playerData) return;

		const data = {
			player_id: String(player_id),
			season_id: String(season_id),
			team_id: String(team_id)
		};

		const searchParams = new URLSearchParams(data);

		goto(`/players/${playerData?.player?.id}?` + searchParams);
	};
</script>

<div class="player-card flex flex-col w-[300px]">
	{#if name}
		<div class="card-title py-2">{name}</div>
	{/if}

	<div class="card-profile-img">
		<img src={imageUrl || imgFallback} alt={name} />
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

{#if redirect}
	<div class="mt-5">
		<Button label="Vai al dettaglio" onClick={goToPlayerhandler} />
	</div>
{/if}

{#if showAiOpinion}
	<div class="flex flex-col justify-center items-center mt-5 w-[300px] gap-2">
		<h5>Vuoi un parere?</h5>

		<p class="text-2xl">👇🏻</p>

		{#if !aiOpinion && !isLoading}
			<Button label="AIpinion" onClick={getAiOpinion} />
		{/if}

		{#if isLoading}
			<SpeakingLoader />
		{/if}

		{#if aiOpinionWritingEffect && !isLoading}
			<hr />

			<div class="aipinion-text flex flex-col w-full p-[2px] mt-3 text-center gap-2">
				{@html aiOpinionWritingEffect}
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
		justify-content: center;
		align-items: center;
		object-fit: cover;
	}

	.card-profile-img img {
		max-width: 100%;
		width: 100%;
	}

	.card-stats span {
		border-top: solid 1px rgb(var(--primary));
	}

	.card-stats span:nth-child(even) {
		border-left: solid 1px rgb(var(--primary));
	}

	.aipinion-text {
		max-height: 200px;
		overflow: auto;
	}
</style>
