<script lang="ts">
	export let sliderData: {
		title?: string;
		subtitle?: string;
		author?: string;
		creationDate?: string;
	} = {};

	export let onClick: () => void;
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
<swiper-slide class="mx-[20px]" on:click={onClick}>
	<div class="article-card">
		<div class="text-wrapper">
			<h4 class="article-title font-bold">{sliderData?.title}</h4>

			<p class="article-subtitle">{sliderData?.subtitle}</p>

			<small class="article-meta">
				Di {sliderData?.author} il {new Date(sliderData?.creationDate || '').toLocaleDateString()}
			</small>
		</div>
	</div>
</swiper-slide>

<style>
	swiper-slide {
		position: relative;
		display: flex;
		justify-content: center;
		align-items: center;
		width: 350px;
		height: 300px;
		border-radius: 20px;
		overflow: hidden;
		transition: all 250ms ease-out;
		cursor: pointer;
		background: var(--card-bg-gradient);
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	}

	@media screen and (max-width: 768px) {
		swiper-slide {
			width: 92%;
		}
	}

	swiper-slide:hover {
		transform: scale(0.95);
		background: var(--card-hover-gradient);
	}

	.article-card {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		width: 100%;
		height: 100%;
		padding: 20px;
		background: rgba(255, 255, 255, 0.9);
		border-radius: 20px;
		transition:
			background 0.3s,
			transform 0.3s;
	}

	.text-wrapper {
		text-align: center;
	}

	.article-title {
		color: var(--main-text-color);
		margin-bottom: 10px;
	}

	.article-subtitle {
		color: var(--main-text-color);
		margin-bottom: 15px;
	}

	.article-meta {
		color: var(--main-text-color);
	}
</style>
