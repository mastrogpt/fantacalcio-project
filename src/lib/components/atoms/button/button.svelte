<script lang="ts">
	import { onMount } from 'svelte';
	import anime from 'animejs';

	export let variant: 'primary' | 'accent' = 'primary';
	export let label: string;
	export let type: 'button' | 'reset' | 'submit' | null | undefined = 'button';
	export let onClick: () => void;

	let button: HTMLButtonElement;

	onMount(() => {
		anime({
			targets: button,
			scale: [0.8, 1],
			opacity: [0, 1],
			duration: 250,
			easing: 'easeOutElastic(1, .8)'
		});
	});

	function handleMouseEnter() {
		anime({
			targets: button,
			scale: 1.05,
			duration: 25,
			easing: 'easeOutExpo'
		});
	}

	function handleMouseLeave() {
		anime({
			targets: button,
			scale: 1,
			duration: 25,
			easing: 'easeOutExpo'
		});
	}

	function handleClick() {
		if (!Boolean(onClick)) return;

		anime({
			targets: button,
			scale: 0.95,
			duration: 25,
			easing: 'easeOutExpo'
		});

		return onClick();
	}
</script>

<button
	bind:this={button}
	class={`btn ${variant}`}
	on:click={handleClick}
	on:mouseenter={handleMouseEnter}
	on:mouseleave={handleMouseLeave}
	{type}
	aria-label={label}
>
	<h6>
		{label}
	</h6>
</button>

<style>
	.btn {
		text-transform: uppercase;
		padding: 1rem 2rem;
		border-radius: 0.5rem;
		cursor: pointer;
		outline: none;
		border: none;
		white-space: nowrap;
		width: min-content;
		transition:
			transform 250ms ease,
			box-shadow 250ms ease;
		background: rgb(var(--accent));
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	}

	.btn:focus {
		box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.5);
	}

	.btn.primary {
		background-color: rgb(var(--primary));
		border-color: rgb(var(--primary));
		color: rgb(var(--white));
	}

	.btn.accent {
		background-color: rgb(var(--accent));
		border-color: rgb(var(--accent));
		color: rgb(var(--dark));
	}
</style>
