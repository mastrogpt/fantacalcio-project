<script lang="ts">
	export let sliderData: {
		imageUrl?: string;
		imageAlt?: string;
		title?: string;
		subtitle?: string;
	} = {};
	export let onClick: () => void;
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
<swiper-slide on:click={onClick}>
	<img src={sliderData?.imageUrl} alt={sliderData?.imageAlt} />

	<div class="text-wrapper flex flex-col gap-2">
		<h4 class="font-bold">{sliderData.title}</h4>

		<small>{sliderData.subtitle}</small>
	</div>
</swiper-slide>

<style>
	swiper-slide {
		position: relative;
		text-align: center;
		font-size: 18px;
		background: #fff;
		display: flex;
		justify-content: stretch;
		align-items: flex-end;
		width: 350px;
		height: 300px;
		border: solid 1px;
		border-radius: 20px;
		overflow: hidden;
		transition: all 250ms ease-out;
		cursor: pointer;
	}

	swiper-slide:hover {
		transform: scale(0.95);
	}

	swiper-slide img {
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		right: 0;
		display: flex;
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	swiper-slide h4 {
		font-size: 1.25rem;
		line-height: 1.75rem;
	}

	swiper-slide .text-wrapper {
		opacity: 1;
		position: relative;
		text-align: left;
		background: rgba(var(--white), 0.85);
		z-index: 10;
		flex: 1;
		padding: 1rem;
		transition: all 350ms ease-out;
	}

	swiper-slide .text-wrapper {
		transform: translateY(50px);
		transition: all 350ms ease-out;
	}

	swiper-slide .text-wrapper small {
		opacity: 0;
		transform: translateY(40px);
		transition: all 350ms ease-out;
	}

	swiper-slide:hover .text-wrapper {
		transform: translateY(0);
		background: rgba(var(--white), 1);
	}

	swiper-slide:hover .text-wrapper small {
		opacity: 1;
		transform: translateY(0);
	}
</style>
