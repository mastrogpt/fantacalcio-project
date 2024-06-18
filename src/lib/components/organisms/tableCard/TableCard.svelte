<script lang="ts">
	import Loader from '$lib/components/atoms/Loader.svelte';
	import Modal from '$lib/components/atoms/modal/Modal.svelte';
	import Tab from '$lib/components/atoms/tab/Tab.svelte';
	import Table from '$lib/components/molecules/table/table.svelte';
	import { getPlayersList, getUnavailablePlayers } from '$lib/service/getPlayers';
	import { selectedRows } from '$lib/store/store';
	import PlayerDetails from '../playerDetails/PlayerDetails.svelte';

	let playerId: number | undefined = undefined;
	let showModal = false;
	let activeTab = 'all';

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
		{ accessorKey: 'playmaker', header: 'Playmaker' },
		{ accessorKey: 'role', header: 'Ruolo' },
		{ accessorKey: 'team', header: 'Squadra' },
		{ accessorKey: 'value', header: 'Valore' }
	];

	const unavailableCols = [
		{ accessorKey: 'team', header: 'Squadra' },
		{ accessorKey: 'name', header: 'Nome' },
		{ accessorKey: 'role', header: 'Ruolo' },
		{ accessorKey: 'doubt', header: 'Dubbio' }
	];

	const toggleModal = () => {
		showModal = !showModal;
	};

	const handleTabChange = (val: string) => {
		activeTab = val;
		console.log('Tab attivo:', activeTab);
	};

	const handleSelectedRows = () => {
		selectedRows.subscribe((rows) => {
			console.log('Selected rows:', rows);
		})();
	};

	$: handleSelectedRows;
</script>

<div class="table-card container flex flex-col align-center justify-center">
	<div class="flex justify-between items-center gap-5 mb-5">
		<h2 class="text-2xl font-bold mb-4 text-black">Dettagli giocatore</h2>

		<Tab {tabs} {activeTab} onTabClick={handleTabChange} />
	</div>

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
						toggleModal();
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
						toggleModal();
					}}
				/>
			{:catch error}
				<p style="color: red">{error.message}</p>
			{/await}
		{/if}
	</div>
</div>

{#if showModal}
	<Modal
		{toggleModal}
		modalContent={PlayerDetails}
		modalProps={{
			playerId
		}}
	/>
{/if}

<style>
	.table-card {
		background: linear-gradient(#10987d, #80b644);
		padding: 2rem;
		border-radius: 1rem;
	}

	.table-card-content {
		position: relative;
		width: 108%;
		left: -4%;
		background: rgb(var(--accent));
		border-radius: 1rem;
	}
</style>
