<script>
	import Siema from 'siema';
	import { onMount, createEventDispatcher } from 'svelte';

	export let loop = true;
	export let autoplay = 0;
	export let duration = 200;
	export let easing = 'ease-out';
	export let startIndex = 0;
	export let draggable = true;
	export let multipleDrag = true;
	export let controls = true;
	export let threshold = 20;
	export let rtl = false;
	let currentIndex = startIndex;

	let siema;
	let controller;
	let timer;
	const dispatch = createEventDispatcher();

	const perPage = {
		0: 1,
		768: 2,
		1024: 3,
		1440: 4
	};

	$: pips = controller ? controller.innerElements : [];
	$: currentPerPage = controller ? controller.perPage : perPage;
	$: totalDots = controller ? Math.ceil(controller.innerElements.length / currentPerPage) : [];

	onMount(() => {
		controller = new Siema({
			selector: siema,
			perPage: perPage,
			loop,
			duration,
			easing,
			startIndex,
			draggable,
			multipleDrag,
			threshold,
			rtl,
			onChange: handleChange
		});

		if (autoplay) {
			timer = setInterval(right, autoplay);
		}
		return () => {
			autoplay && clearInterval(timer);
			controller.destroy();
		};
	});

	function isDotActive(currentIndex, dotIndex) {
		if (currentIndex < 0) currentIndex = pips.length + currentIndex;
		return (
			currentIndex >= dotIndex * currentPerPage &&
			currentIndex < dotIndex * currentPerPage + currentPerPage
		);
	}

	function left() {
		controller.prev();
	}

	function right() {
		controller.next();
	}

	function go(index) {
		controller.goTo(index);
	}

	function pause() {
		clearInterval(timer);
	}

	function resume() {
		if (autoplay) {
			timer = setInterval(right, autoplay);
		}
	}

	function handleChange(event) {
		currentIndex = controller.currentSlide;
		dispatch('change', {
			currentSlide: controller.currentSlide,
			slideCount: controller.innerElements.length
		});
	}

	function resetInterval(node, condition) {
		function handleReset(event) {
			pause();
			resume();
		}

		if (condition) {
			node.addEventListener('click', handleReset);
		}

		return {
			destroy() {
				node.removeEventListener('click', handleReset);
			}
		};
	}
</script>

<div class="carousel">
	<div class="slides" bind:this={siema}>
		<slot />
	</div>

	{#if controls}
		<div class="navigation">
			<button class="left" on:click={left} use:resetInterval={autoplay} aria-label="left">
				&lsaquo;
			</button>

			<button class="right" on:click={right} use:resetInterval={autoplay} aria-label="right">
				&rsaquo;
			</button>
		</div>
	{/if}
</div>

<style>
	.carousel {
		position: relative;
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.carousel > div.slides {
		width: 95%;
	}

	.slides {
		width: 100%;
		overflow: hidden;
	}

	.slides > * {
		width: 350px;
		margin: 0 auto;
	}

	.navigation {
		position: absolute;
		top: 50%;
		transform: translateY(-50%);
		display: flex;
		justify-content: space-between;
		width: 100%;
		margin-top: 10px;
	}

	button {
		width: 40px;
		height: 40px;
		border: none;
		background-color: transparent;
		cursor: pointer;
		font-size: 24px;
		line-height: 1;
	}
	button:focus {
		outline: none;
	}

	@media (min-width: 768px) {
		.slides > * {
			margin: 0;
		}
	}
</style>
