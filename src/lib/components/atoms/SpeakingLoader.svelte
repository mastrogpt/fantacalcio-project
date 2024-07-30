<script lang="ts">
	export let variant: 'primary' | 'accent' = 'primary';

	let message = 'un attimo...';

	setTimeout(() => {
		message = 'ci sto pensando';
	}, 3000);
</script>

<div class="flex flex-col justify-center items-center h-30 p-10">
	<div class={`animate-spin rounded-full h-10 w-10 border-b-2 border-${variant}`}></div>
	<p class="mt-4 text-${variant}">{message}</p>
</div>

