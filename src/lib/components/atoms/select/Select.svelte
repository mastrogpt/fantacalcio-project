<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let options: { value: string; label: string }[] = [];
	export let selectedValue: string = '';
	export let label: string = '';
	export let id: string = '';
	export let name: string = '';

	const dispatch = createEventDispatcher();

	function handleChange(event) {
		selectedValue = event.target.value;
		dispatch('change', { value: selectedValue });
	}
</script>

<div class="relative w-64">
	<label for={id} class="block text-sm font-medium text-gray-700">{label}</label>

	<select
		{id}
		{name}
		bind:value={selectedValue}
		class="block appearance-none w-full bg-transparent border border-2 border-primary text-gray-700 py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:border-gray-500 focus:border-3"
		on:change={handleChange}
	>
		{#each options as option}
			<option value={option.value}>{option.label}</option>
		{/each}
	</select>

	<div
		class="pointer-events-none absolute inset-y-0 right-0 top-5 flex items-center px-2 text-gray-700"
	>
		<svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
			<path
				d="M9.293 14.707a1 1 0 0 0 1.414 0l5-5a1 1 0 0 0-1.414-1.414L10 12.586l-4.293-4.293a1 1 0 1 0-1.414 1.414l5 5z"
			/>
		</svg>
	</div>
</div>
