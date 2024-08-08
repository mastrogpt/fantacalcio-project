<script lang="ts">
	export let variant: 'primary' | 'accent' = 'accent';

	let message = 'Mo se vede';

	setTimeout(() => {
		message = 'Stamo a lavora';
		setTimeout(() => {
			message = "Aoh, ce vo' tempo...";
		}, 9000);
	}, 4000);
</script>

<div class="flex flex-col justify-center items-center h-30 p-10">
	<p class={`mt-4 text-${variant}`}>
		<strong>{message}</strong>
		<span class="dots"></span>
	</p>
</div>

<style>
	@keyframes ellipsis {
		0% {
			visibility: visible;
		}
		25% {
			visibility: hidden;
		}
		50% {
			visibility: visible;
		}
		75% {
			visibility: hidden;
		}
		100% {
			visibility: visible;
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

	.dots {
		display: inline-block;
		animation: bounce 0.6s infinite;
	}

	.dots::after {
		content: '.';
		animation: ellipsis 1.5s infinite;
	}

	.text-primary {
		color: #041c2c;
	}

	.text-accent {
		color: #10987d;
	}
</style>
