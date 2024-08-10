<script lang="ts">
	export let variant: 'primary' | 'accent' = 'accent';

	let message = 'Mo se vede';

	setTimeout(() => {
		message = 'Stamo a lavora';
		setTimeout(() => {
			message = "Aoh, ce vo' tempo";
		}, 9000);
	}, 4000);
</script>

<div class="flex flex-col justify-center items-center h-30 p-10">
	<p class={`mt-4 text-${variant} text-xl`}>
		<strong>{message}</strong>
		<span class="dots">
			<span class="dot">.</span>
			<span class="dot">.</span>
			<span class="dot">.</span>
		</span>
	</p>
</div>

<style>
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
	}

	.dot {
		display: inline-block;
		animation: bounce 1.2s infinite;
	}

	.dot:nth-child(1) {
		animation-delay: 0s;
	}
	.dot:nth-child(2) {
		animation-delay: 0.2s;
	}
	.dot:nth-child(3) {
		animation-delay: 0.4s;
	}

	.text-primary {
		color: #041c2c;
	}

	.text-accent {
		color: #10987d;
	}
</style>
