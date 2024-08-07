<script>
	export let alert = 'false';
</script>

{#if alert === 'true'}
	<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
		<g fill="none" fill-rule="evenodd">
			<path
				fill="#FF0000"
				d="M12 0c6.627 0 12 5.373 12 12s-5.373 12-12 12S0 18.627 0 12 5.373 0 12 0zm0 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zM9.707 9.707c.391.391.391 1.023 0 1.414L8.121 12l1.586 1.586c.391.391.391 1.023 0 1.414-.391.391-1.023.391-1.414 0L6.707 13.414c-.391-.391-.391-1.023 0-1.414L9.293 9.707c.195-.195.45-.293.707-.293s.512.098.707.293z"
			/>
		</g>
	</svg>
{:else}
	<svg
		class="w-6 h-6 fill-current text-gray-600"
		xmlns="http://www.w3.org/2000/svg"
		viewBox="0 0 24 24"
	>
		<path d="M0 0h24v24H0z" fill="none" />
		<path d="M7 10l5 5 5-5z" />
	</svg>
{/if}
