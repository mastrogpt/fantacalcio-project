<script lang="ts">
	import Loader from '$lib/components/atoms/Loader.svelte';
	import Button from '$lib/components/atoms/button/button.svelte';
	import Modal from '$lib/components/atoms/modal/Modal.svelte';
	import Tab from '$lib/components/atoms/tab/Tab.svelte';
	import Table from '$lib/components/molecules/table/table.svelte';
	import { getPlayersList, getUnavailablePlayers } from '$lib/service/fantaicalcio/getPlayers';
	import { selectedRows, isPlayerCardOpen, handlePlayerCardOpening } from '$lib/store/store';
	import ComparePlayers from '../comparePlayers/ComparePlayers.svelte';
	import PlayerDetails from '../playerDetails/PlayerDetails.svelte';

	let player_id: number;
	let season_id: number;
	let team_id: number;

	let activeTab = 'all';
	let modalContent;

	let tabs = [
		{
			label: 'FantaBalùn',
			value: 'all'
		}
	];

	const playersCols = [
		{ accessorKey: 'name', header: 'Nome' },
		{ accessorKey: 'position', header: 'Ruolo' },
		{ accessorKey: 'team', header: 'Squadra' },
		{ accessorKey: 'available', header: 'Disponibile' }
	];

	const unavailableCols = [
		{ accessorKey: 'name', header: 'Nome' },
		{ accessorKey: 'team', header: 'Squadra' },
		{ accessorKey: 'role', header: 'Ruolo' },
		{ accessorKey: 'doubt', header: 'Dubbio' }
	];

	const toggleModal = (modalContentEnum: 'DETAILS' | 'COMPARE') => {
		handlePlayerCardOpening();

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
	};

	const clearSelection = () => {
		selectedRows.set(new Set());
	};

	function canSelectPlayer(player) {
		const currentSelections = Array.from($selectedRows);
		if (currentSelections.length === 0) {
			return true;
		}
		return currentSelections.every((row) => row.role === player.role);
	}
</script>

<div class="table-card container flex flex-col align-center justify-center">
	<div class="flex justify-between items-center gap-5 mb-5 flex-col md:flex-row">
		<h2 class="text-2xl font-bold mb-4 text-white">Lista giocatori</h2>
		<Tab {tabs} {activeTab} onTabClick={handleTabChange} />
	</div>
	<hr />
	<p class="my-5 px-10">
		Noi ti forniamo la lista dei giocatori, i dati e le <strong>
			statistiche più interessanti</strong
		>
		Tu decidi chi mandare in campo. Se hai dei dubbi, seleziona due calciatori e comparali. <br /> Magari
		ti confonderemo le idee!
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
						if (canSelectPlayer(row.original)) {
							player_id = row.original.id;
							season_id = row.original.season_id;
							team_id = row.original.team_id;
							toggleModal('DETAILS');
						} else {
							alert('Puoi selezionare solo giocatori con lo stesso ruolo.');
						}
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
						if (canSelectPlayer(row.original)) {
							player_id = row.original.id;
							toggleModal('DETAILS');
						} else {
							alert('Puoi selezionare solo giocatori con lo stesso ruolo.');
						}
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

{#if $isPlayerCardOpen}
	<Modal
		{toggleModal}
		{modalContent}
		modalProps={{
			player_id,
			season_id,
			team_id
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
