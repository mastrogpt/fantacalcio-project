<script lang="ts">
	export let tabs: { value: string; label: string }[] = [];
	export let activeTab: string = '';
	export let onTabClick: (val: string) => void;

	const handleClick = (val: string) => {
		activeTab = val;
	};
</script>

<div class="tab-container flex">
	{#each tabs as tab}
		<div
			class="tab {activeTab === tab.value ? 'active' : 'inactive'}"
			on:click={() => onTabClick(tab.value)}
		>
			{tab.label}
		</div>
	{/each}
</div>

<style>
	.tab-container {
		border: solid 2px rgb(var(--accent));
		border-radius: 1rem;
		overflow: hidden;
	}

	.tab {
		padding: 8px 16px;
		cursor: pointer;
		font-weight: bold;
		text-transform: uppercase;
		width: 100%;
		height: 100%;
	}

	.active {
		background-color: rgb(var(--accent));
		color: rgb(var(--primary));
	}

	.inactive {
		color: #fff;
	}
</style>
