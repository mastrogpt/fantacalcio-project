<script lang="ts">
	import { getAiOpinionFromBackend } from '$lib/service/aiOpinion';
	import Loader from '$lib/components/atoms/Loader.svelte';
	import BackButton from '$lib/components/atoms/buttons/BackButton.svelte';
	import GreenButton from '$lib/components/atoms/buttons/GreenButton.svelte';
	import DisabledButton from '$lib/components/atoms/buttons/DisabledButton.svelte';
	import Person from '$lib/components/atoms/icons/Person.svelte';
	import Foot from '$lib/components/atoms/icons/Foot.svelte';
	import Ball from '$lib/components/atoms/icons/Ball.svelte';
	import Card from '$lib/components/atoms/icons/Card.svelte';
	import type { PlayerCompleteStats } from '$lib/service/fantaicalcio/getStats';

	export let data: {
		playerData: PlayerCompleteStats;
		playerName: string;
	};

	let aiOpinion: string;
	let aiOpinionWritingEffect: string;
	let isLoading = false;
	/**
	 * Functions util to show text with real effect
	 */
	async function showMessage() {
		for (let i = 0; i < aiOpinion.length; i++) {
			aiOpinionWritingEffect = aiOpinion.substring(0, i + 1);
			await sleep(30);
		}
	}
	function sleep(ms: number) {
		return new Promise((resolve) => setTimeout(resolve, ms));
	}
	/*
	 */

	async function getAiOpinion() {
		isLoading = true;
		aiOpinion = await getAiOpinionFromBackend(data.playerData);
		showMessage();
		isLoading = false;
	}
</script>

<div class="grid grid-cols-1 gap-4 lg:gap-8 mx-auto justify-center">
	<div class="h-32 rounded-lg bg-gray-200 lg:col-span-2">
		<div class="bg-gradient-to-r from-primary from-10% via-gray-200 via-30% to-gray-100 to-65%">
			<h2 class="text-center mb-5">
				<strong>{data.playerData?.name}</strong> -
				<strong class="text-primary">{data.playerData?.team}</strong>
			</h2>
			<div class="flex justify-end">
				<BackButton href="/players" text="Indietro" />
				{#if !aiOpinion && !isLoading}
					<GreenButton text="AIpinion" clickAction={getAiOpinion} />
				{:else if isLoading || aiOpinion}
					<DisabledButton text="AIpinion" />
				{/if}
			</div>
		</div>

		{#if data}
			<div class="overflow-x-auto">
				<table class="min-w-full divide-y-2 divide-gray-200 bg-white text-sm">
					<thead class="ltr:text-left rtl:text-right">
						<tr>
							<th class="whitespace-nowrap p-2 font-bold text-left"><Person /></th>
							<th class="whitespace-nowrap p-2 font-bold text-left"><Foot /></th>

							<th class="whitespace-nowrap p-2 font-medium text-primary text-xl font-bold text-left"
								><Ball /></th
							>
							<th class="whitespace-nowrap p-2 font-medium text-primary text-xl font-bold text-left"
								>Media</th
							>
							<th class="whitespace-nowrap p-2 font-medium text-primary text-xl font-bold text-left"
								>Fmedia</th
							>
							<th class="whitespace-nowrap p-2 font-medium text-primary text-xl font-bold text-left"
								><Card color="#ef4444" /></th
							>
							<th class="whitespace-nowrap p-2 font-medium text-primary text-xl font-bold text-left"
								><Card color="#facc15" /></th
							>
						</tr>
					</thead>
					<tbody>
						<tr class="border-b">
							<td class="whitespace-nowrap p-4 font-medium text-gray-900"
								>{data.playerData?.caps}</td
							>
							<td class="whitespace-nowrap p-4 font-medium text-gray-900"
								>{data.playerData?.assists}</td
							>
							<td class="whitespace-nowrap p-4 font-medium text-gray-900"
								>{data.playerData?.goals}</td
							>
							<td class="whitespace-nowrap p-4 font-medium text-gray-900"
								>{data.playerData?.markavg}</td
							>
							<td class="whitespace-nowrap p-4 font-medium text-gray-900"
								>{data.playerData?.fmarkavg}</td
							>
							<td class="whitespace-nowrap p-2 font-medium text-gray-900"
								>{data.playerData?.rcards}</td
							>
							<td class="whitespace-nowrap p-2 font-medium text-gray-900"
								>{data.playerData?.ycards}</td
							>
						</tr>
					</tbody>
				</table>
			</div>
		{/if}
		<div class="h-32 rounded-lg">
			{#if isLoading}
				<Loader />
			{/if}
			{#if aiOpinionWritingEffect && !isLoading}
				<div
					class="w-full overflow-auto bg-gradient-to-r from-gray-100 from-45% via-gray-200 to-primary p-[2px] mx-0.5 text-center"
				>
					{aiOpinionWritingEffect}
				</div>
			{/if}
		</div>
	</div>
</div>
