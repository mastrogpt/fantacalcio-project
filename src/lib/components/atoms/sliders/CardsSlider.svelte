<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { register } from 'swiper/element/bundle';
	import PlayerCard from '../playerCard/PlayerCard.svelte';
	import type { ISliderDataProps, PlayerCompleteStats } from '$lib/service/fantaicalcio/getStats';

	onMount(() => {
		register();
	});

	export let sliderData: ISliderDataProps[];
</script>

<swiper-container class="cards-slider" effect="cards" transition:fade>
	{#each sliderData as { name }}
		<swiper-slide>
			<PlayerCard {name} />
		</swiper-slide>
	{/each}
</swiper-container>

<style>
	swiper-container {
		width: 240px;
		height: auto;
		padding-bottom: 50px;
	}

	swiper-slide {
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 18px;
		font-weight: bold;
		color: #000;
		background: #fff;
	}
</style>
