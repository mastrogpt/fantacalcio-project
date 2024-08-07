<script lang="ts">
	export let variant: 'primary' | 'accent' = 'primary';

	let message = 'Un attimo';

	setTimeout(() => {
		message = "Mo' t'o dico";
	}, 3000);
</script>

<div class="flex flex-col justify-center items-center h-30 p-10">
	<p class={`mt-4 text-${variant} ${message === 'Un attimo' ? 'ellipsis' : ''}`}>
		{message}<span class="dots"></span>
	</p>
</div>

<style>
	@keyframes ellipsis {
		0% {
			content: '.';
		}
		33% {
			content: '..';
		}
		66% {
			content: '...';
		}
		100% {
			content: '.';
		}
	}

	@keyframes bounce {
		0%,
		100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(-10px);
		}
	}

	.dots::after {
		content: '.';
		animation:
			ellipsis 1.5s steps(3, end) infinite,
			bounce 0.6s infinite;
	}

	.text-primary {
		color: #10987d;
	}

	.text-accent {
		color: #ffd700;
	}
</style>
