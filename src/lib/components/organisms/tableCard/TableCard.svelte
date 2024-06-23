<script lang="ts">
	import Loader from '$lib/components/atoms/Loader.svelte';
	import Button from '$lib/components/atoms/button/button.svelte';
	import Modal from '$lib/components/atoms/modal/Modal.svelte';
	import Tab from '$lib/components/atoms/tab/Tab.svelte';
	import Table from '$lib/components/molecules/table/table.svelte';
	import { getPlayersList, getUnavailablePlayers } from '$lib/service/getPlayers';
	import { selectedRows } from '$lib/store/store';
	import ComparePlayers from '../comparePlayers/ComparePlayers.svelte';
	import PlayerDetails from '../playerDetails/PlayerDetails.svelte';

	let playerId: number | undefined = undefined;
	let showModal = false;
	let activeTab = 'all';
	let modalContent;

	let tabs = [
		{
			label: 'Tutti',
			value: 'all'
		},
		{
			label: 'Indisponibili',
			value: 'unavailable'
		}
	];

	const playersCols = [
		{ accessorKey: 'name', header: 'Nome' },
		{ accessorKey: 'role', header: 'Ruolo' },
		{ accessorKey: 'team', header: 'Squadra' },
		{ accessorKey: 'value', header: 'Valore' }
	];

	const unavailableCols = [
		{ accessorKey: 'name', header: 'Nome' },
		{ accessorKey: 'team', header: 'Squadra' },
		{ accessorKey: 'role', header: 'Ruolo' },
		{ accessorKey: 'doubt', header: 'Dubbio' }
	];

	const toggleModal = (modalContentEnum: 'DETAILS' | 'COMPARE') => {
		showModal = !showModal;

		switch (modalContentEnum) {
			case 'DETAILS':
				return (modalContent = PlayerDetails);
			case 'COMPARE':
				return (modalContent = ComparePlayers);

			default:
				break;
		}
	};

	const handleTabChange = (val: string) => {
		activeTab = val;
		console.log('Tab attivo:', activeTab);
	};

	// Function to clear selection
	const clearSelection = () => {
		selectedRows.set(new Set());
	};
</script>

<div class="table-card container flex flex-col align-center justify-center">
	<div class="flex justify-between items-center gap-5 mb-5">
		<h2 class="text-2xl font-bold mb-4 text-black">Dettagli giocatore</h2>

		<Tab {tabs} {activeTab} onTabClick={handleTabChange} />
	</div>

	<hr />

	<p class="my-5 px-10">
		Lorem, ipsum dolor sit amet consectetur adipisicing elit. Animi maiores esse maxime corrupti
		assumenda nam natus sunt fugiat dolores? Veritatis assumenda cum asperiores ipsa esse excepturi
		aperiam, illum dolorem fugiat!
	</p>

	<div class="table-card-content">
		{#if activeTab === 'all'}
			{#await getPlayersList()}
				<Loader />
			{:then data}
				<Table
					{data}
					columns={playersCols}
					selectableRows
					onRowClick={(row) => {
						playerId = row.original.id;
						toggleModal('DETAILS');
					}}
				/>
			{:catch error}
				<p style="color: red">{error.message}</p>
			{/await}
		{:else}
			{#await getUnavailablePlayers()}
				<Loader />
			{:then data}
				<Table
					{data}
					columns={unavailableCols}
					onRowClick={(row) => {
						playerId = row.original.id;
						toggleModal('DETAILS');
					}}
				/>
			{:catch error}
				<p style="color: red">{error.message}</p>
			{/await}
		{/if}
	</div>

	{#if Array.from($selectedRows).length > 0}
		<div class="mt-4">
			<h3 class="text-xl font-bold mb-2">Giocatori selezionati:</h3>

			{#if Array.from($selectedRows).length === 0}
				<p>Non hai s.</p>
			{:else if Array.from($selectedRows).length === 2}
				<ul>
					{#each Array.from($selectedRows) as row}
						<li>{row.name}</li>
					{/each}
				</ul>

				<div class="flex flex-col gap-5 justify-center items-center my-2">
					<Button
						label="Cancella selezione"
						outline
						noBorder
						size="small"
						onClick={clearSelection}
					/>

					<Button
						label="Compara"
						size="small"
						variant="accent"
						onClick={() => toggleModal('COMPARE')}
					/>
				</div>
			{:else}
				<ul>
					{#each Array.from($selectedRows) as row}
						<li>{row.name}</li>
					{/each}
				</ul>

				<Button label="Cancella selezione" outline noBorder onClick={clearSelection} />
			{/if}
		</div>
	{/if}
</div>

{#if showModal}
	<Modal
		{toggleModal}
		{modalContent}
		modalProps={{
			playerId
		}}
	/>
{/if}

<style>
	.table-card {
		width: 80%;
		background: linear-gradient(#10987d, #80b644);
		padding: 2rem;
		border-radius: 1rem;
	}

	.table-card-content {
		position: relative;
		width: 112%;
		left: -6%;
		padding: 1rem;
		background: rgb(var(--accent));
		border-radius: 1rem;
	}
</style>
