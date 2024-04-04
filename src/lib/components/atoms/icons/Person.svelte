<script>
	let showInfo = false;

	function toggleInfo() {
		showInfo = !showInfo;
	}
</script>

<div class="relative" on:mouseenter={toggleInfo} on:mouseleave={toggleInfo} role="tooltip">
	<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="#1b81a5" class="w-6 h-6">
		<path
			d="M10 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM3.465 14.493a1.23 1.23 0 0 0 .41 1.412A9.957 9.957 0 0 0 10 18c2.31 0 4.438-.784 6.131-2.1.43-.333.604-.903.408-1.41a7.002 7.002 0 0 0-13.074.003Z"
		/>
	</svg>
	{#if showInfo}
		<div class="absolute bottom-0 left-0 bg-gray-800 text-white p-2 rounded-lg text-xs font-bold">
			Numero di presenze
		</div>
	{/if}
</div>
