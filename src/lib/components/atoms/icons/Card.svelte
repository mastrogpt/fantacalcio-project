<script>
	let showInfo = false;

	function toggleInfo() {
		showInfo = !showInfo;
	}
	export let color = 'black';
</script>

<div class="relative" on:mouseenter={toggleInfo} on:mouseleave={toggleInfo} role="tooltip">
	<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill={color} class="w-5 h-5">
		<path
			d="M5.25 3A2.25 2.25 0 0 0 3 5.25v9.5A2.25 2.25 0 0 0 5.25 17h9.5A2.25 2.25 0 0 0 17 14.75v-9.5A2.25 2.25 0 0 0 14.75 3h-9.5Z"
		/>
	</svg>
	{#if showInfo}
		<div class="absolute bottom-0 left-0 bg-gray-800 text-white p-2 rounded-lg text-xs font-bold">
			Cartellini
		</div>
	{/if}
</div>
