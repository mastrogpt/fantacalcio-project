<script lang="ts">
	import Button from '../../button/button.svelte';

	export let sliderData: {
		title?: string;
		description?: string;
		buttonLabel?: string;
		buttonOnClick?: () => void;
		imageUrl?: string;
		imageAlt?: string;
	};
</script>

<swiper-slide class="max-[600px]:flex-col-reverse">
	<div class="flex flex-col text-left justify-start hero-text gap-10">
		<div class="flex flex-col gap-4">
			<h2>
				{sliderData?.title}
			</h2>

			<p>{sliderData?.description}</p>
		</div>

		{#if sliderData?.buttonLabel && Boolean(sliderData?.buttonOnClick)}
			<Button
				label={sliderData?.buttonLabel}
				onClick={sliderData?.buttonOnClick}
				variant="accent"
			/>
		{/if}
	</div>

	{#if sliderData?.imageUrl}
		<div class="hero-image">
			<img src={sliderData?.imageUrl} alt={sliderData?.imageAlt} loading="lazy" />
		</div>
	{/if}
</swiper-slide>

<style>
	swiper-slide {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		border-radius: 20px;
		overflow: hidden;
		background-position: center;
		background-size: cover;
		padding: 0 2rem;
	}

	swiper-slide .hero-text,
	swiper-slide .hero-image {
		display: flex;
		flex: 1;
	}

	swiper-slide .hero-image {
		align-items: center;
		justify-content: center;
	}

	swiper-slide img {
		display: block;
		object-fit: cover;
		height: 450px;
		border-radius: 20px;
	}
</style>
