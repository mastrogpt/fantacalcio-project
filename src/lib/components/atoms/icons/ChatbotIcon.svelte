<script lang="ts">
	export let onClick: () => void;
</script>

<svg
	class="bot-icon"
	xmlns="http://www.w3.org/2000/svg"
	viewBox="0 0 24 24"
	fill="none"
	stroke="currentColor"
	stroke-width="2"
	stroke-linecap="round"
	stroke-linejoin="round"
	on:click={onClick}
>
	<circle cx="12" cy="12" r="10"></circle>
	<line x1="12" y1="16" x2="12" y2="12"></line>
	<line x1="12" y1="8" x2="12.01" y2="8"></line>
</svg>

<style>
	.bot-icon {
		position: fixed;
		bottom: 20px;
		right: 20px;
		width: 60px;
		height: 60px;
		cursor: pointer;
		transition: transform 0.3s ease-in-out;
		z-index: 1000;
	}

	.bot-icon:hover {
		transform: scale(1.1);
	}
</style>
