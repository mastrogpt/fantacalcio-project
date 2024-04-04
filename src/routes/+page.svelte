<script lang="ts">
	import Loader from '$lib/components/atoms/Loader.svelte';
	import { getAiPresentationFromBackend } from '$lib/service/aiPresentation';
	import { onMount } from 'svelte';
	import football from '$lib/assets/football.png';
	import footballVertical from '$lib/assets/footballVertical.png';

	let aiPresentation: string;
	let aiPresentationWritingEffect: string;
	let isLoading = false;

	/**
	 * Functions util to show text with real effect
	 */
	async function showMessage() {
		for (let i = 0; i < aiPresentation.length; i++) {
			aiPresentationWritingEffect = aiPresentation.substring(0, i + 1);
			await sleep(25);
		}
	}
	function sleep(ms: number) {
		return new Promise((resolve) => setTimeout(resolve, ms));
	}
	/*
	 */

	async function getAiPresentation() {
		isLoading = true;
		aiPresentation = await getAiPresentationFromBackend();
		showMessage();
		isLoading = false;
	}

	onMount(async () => {
		await getAiPresentation();
	});
</script>

<div>
	<div class="w-full mt-2 bg-gray-900 h-96">
		<div class="relative h-full sm:block">
			<img
				alt=""
				src={footballVertical}
				class="absolute inset-0 w-full h-120 object-cover block lg:hidden"
			/>

			<img
				alt=""
				src={football}
				class="absolute inset-0 w-full h-120 object-cover hidden lg:block"
			/>

			<div
				class="m-4 p-2 absolute flex items-center justify-center lg:w-2/5 sm:w-3/5 bg-opacity-85 bg-gray-900 rounded-lg"
			>
				{#if aiPresentation}
					<p class="mt-2 text-l text-white font-extrabold lg:text-base sm:text-sm">
						{aiPresentationWritingEffect}
					</p>
				{:else}
					<Loader />
				{/if}
			</div>
		</div>
	</div>
</div>
