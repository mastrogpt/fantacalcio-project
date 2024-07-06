<script lang="ts">
	import { goto } from '$app/navigation';
	import Button from '$lib/components/atoms/button/button.svelte';
	import Loader from '$lib/components/atoms/Loader.svelte';
	import Table from '$lib/components/molecules/table/table.svelte';
	import { getPlayersList } from '$lib/service/fantaicalcio/getPlayers';
	import { flexRender } from '@tanstack/svelte-table';

	const columns = [
		{ accessorKey: 'name', header: 'Nome' },
		{ accessorKey: 'playmaker', header: 'Playmaker' },
		{ accessorKey: 'role', header: 'Ruolo' },
		{ accessorKey: 'team', header: 'Squadra' },
		{ accessorKey: 'value', header: 'Valore' },
		{
			accessorKey: 'action',
			header: '',
			cell: (ctx) =>
				flexRender(Button, {
					label: 'CIAO',
					variant: 'accent',
					onClick: () => goto(`/players/${ctx.row.original.id}`)
				})
		}
	];
</script>

<svelte:head>
	<title>MastroGPT - Fantamaster</title>
	<meta name="og:title" content="MastroGPT" />
</svelte:head>

<section class="py-10 flex flex-column items-center justify-center">
	<div class="container">
		<h2 class="text-center mb-5">Tutti i giocatori</h2>

		<div class="overflow-x-auto">
			{#await getPlayersList()}
				<p><Loader /></p>
			{:then data}
				<Table {data} {columns} />
			{:catch error}
				<p style="color: red">{error.message}</p>
			{/await}
		</div>
	</div>
</section>

<style></style>
