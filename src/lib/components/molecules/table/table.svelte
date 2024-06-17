<script lang="ts">
	import { rankItem } from '@tanstack/match-sorter-utils';
	import type { FilterFn, OnChangeFn, SortingState, TableOptions } from '@tanstack/svelte-table';
	import {
		createSvelteTable,
		flexRender,
		getCoreRowModel,
		getFilteredRowModel,
		getPaginationRowModel,
		getSortedRowModel
	} from '@tanstack/svelte-table';
	import { writable } from 'svelte/store';

	export let data = [];
	export let columns = [];
	export let onRowClick: (data: any) => void;

	const fuzzyFilter: FilterFn<any> = (row, columnId, value, addMeta) => {
		const itemRank = rankItem(row.getValue(columnId), value);
		addMeta({ itemRank });
		return itemRank.passed;
	};

	let sorting: SortingState = [];

	const setSorting: OnChangeFn<SortingState> = (updater) => {
		if (updater instanceof Function) {
			sorting = updater(sorting);
		} else {
			sorting = updater;
		}
		options.update((old) => ({
			...old,
			state: {
				...old.state,
				sorting
			}
		}));
	};

	// Make data reactive
	const dataStore = writable(data);

	const options = writable<TableOptions<{ [key: string]: string }>>({
		data,
		columns,
		state: {
			sorting
		},
		filterFns: {
			fuzzy: fuzzyFilter
		},
		enableMultiRowSelection: true,
		getPaginationRowModel: getPaginationRowModel(), // Enable pagination
		autoResetPageIndex: true, // Automatically update pagination when data or page size changes
		getCoreRowModel: getCoreRowModel(),
		globalFilterFn: fuzzyFilter,
		getFilteredRowModel: getFilteredRowModel(),
		onSortingChange: setSorting,
		getSortedRowModel: getSortedRowModel()
	});

	const table = createSvelteTable(options);

	let pageSize = 10; // number of rows to show
	$table.setPageSize(pageSize);

	const handleKeyUp = (e: any) => {
		$table.setGlobalFilter(String(e?.target?.value));
	};

	const selectedRows = writable(new Set());

	const handleCheckboxChange = (rowId) => {
		selectedRows.update((rows) => {
			const newRows = new Set(rows);
			if (newRows.has(rowId)) {
				newRows.delete(rowId);
			} else {
				if (newRows.size < 2) {
					newRows.add(rowId);
				}
			}
			return newRows;
		});
	};

	const handleRowClick = (row) => {
		const rowId = row.id;

		if (Boolean(onRowClick)) return onRowClick(row);

		selectedRows.update((rows) => {
			const newRows = new Set(rows);
			if (newRows.has(rowId)) {
				newRows.delete(rowId);
			} else {
				if (newRows.size < 2) {
					newRows.add(rowId);
				}
			}
			return newRows;
		});
	};

	const clearSelection = () => {
		selectedRows.set(new Set());
	};

	// Function to update data reactively
	export function updateData(newData) {
		dataStore.set(newData);
		options.update((opt) => ({ ...opt, data: newData }));
	}
</script>

<div class="p-2">
	<h2 class="text-center text-2xl font-bold mb-4 text-black">Dettagli giocatore</h2>

	<!-- Filtro globale -->
	<div class="mb-4">
		<input
			type="text"
			placeholder="Cerca..."
			class="w-full px-4 py-2 border border-gray-300 rounded"
			on:keyup={handleKeyUp}
		/>
	</div>

	<table class="w-full border-collapse table-fixed">
		<thead>
			{#each $table.getHeaderGroups() as headerGroup}
				<tr>
					<th class="px-4 py-2 text-left border border-gray-300"></th>
					<!-- Empty header for the compare icon -->
					{#each headerGroup.headers as header}
						<th class="px-4 py-2 text-left border border-gray-300" colSpan={header.colSpan}>
							{#if !header.isPlaceholder}
								<div
									class="cursor-pointer select-none"
									on:click={header.column.getToggleSortingHandler()}
								>
									<svelte:component
										this={flexRender(header.column.columnDef.header, header.getContext())}
									/>
									{#if header.column.getIsSorted() === 'asc'}
										🔼
									{:else if header.column.getIsSorted() === 'desc'}
										🔽
									{/if}
								</div>
							{/if}
						</th>
					{/each}
				</tr>
			{/each}
		</thead>

		<tbody>
			{#each $table.getRowModel().rows as row}
				<tr class="odd:bg-light even:bg-white cursor-pointer" on:click={() => handleRowClick(row)}>
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<!-- svelte-ignore a11y-no-static-element-interactions -->
					<td class="px-4 py-2 border text-black flex items-center" on:click|stopPropagation>
						<input
							type="checkbox"
							on:change={() => handleCheckboxChange(row.id)}
							checked={$selectedRows.has(row.id)}
							disabled={$selectedRows.size >= 2 && !$selectedRows.has(row.id)}
							class="mr-2"
						/>
					</td>

					{#each row.getVisibleCells() as cell}
						<td class="px-4 py-2 border text-black">
							<svelte:component this={flexRender(cell.column.columnDef.cell, cell.getContext())} />
						</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>

	<!-- Pagination Controls -->
	<div class="flex justify-center mt-4">
		<button on:click={() => $table.previousPage()} disabled={!$table.getCanPreviousPage()}>
			Prev
		</button>

		{#if $table.getPageCount() > 5}
			<button
				on:click={() => $table.setPageIndex(0)}
				class:font-bold={$table.getState().pagination.pageIndex === 0}
			>
				1
			</button>
			{#if $table.getState().pagination.pageIndex > 2}
				<span>...</span>
			{/if}

			{#each Array(5)
				.fill(0)
				.map((_, i) => $table.getState().pagination.pageIndex - 2 + i)
				.filter((i) => i > 0 && i < $table.getPageCount() - 1) as pageIndex}
				<button
					on:click={() => $table.setPageIndex(pageIndex)}
					class:font-bold={$table.getState().pagination.pageIndex === pageIndex}
				>
					{pageIndex + 1}
				</button>
			{/each}

			{#if $table.getState().pagination.pageIndex < $table.getPageCount() - 3}
				<span>...</span>
			{/if}
			<button
				on:click={() => $table.setPageIndex($table.getPageCount() - 1)}
				class:font-bold={$table.getState().pagination.pageIndex === $table.getPageCount() - 1}
			>
				{$table.getPageCount()}
			</button>
		{:else}
			{#each Array($table.getPageCount())
				.fill(0)
				.map((_, i) => i) as pageIndex}
				<button
					on:click={() => $table.setPageIndex(pageIndex)}
					class:font-bold={$table.getState().pagination.pageIndex === pageIndex}
				>
					{pageIndex + 1}
				</button>
			{/each}
		{/if}
		<button on:click={() => $table.nextPage()} disabled={!$table.getCanNextPage()}> Next </button>
	</div>

	<!-- Selected Rows -->
	<div class="mt-4">
		<h3 class="text-xl font-bold mb-2">Elementi selezionati:</h3>
		{#if $selectedRows.size === 0}
			<p>Nessun elemento selezionato.</p>
		{:else}
			<ul>
				{#each Array.from($selectedRows) as rowId}
					{#each $table.getRowModel().rows as row}
						{#if row.id === rowId}
							<li>{JSON.stringify(row.original)}</li>
						{/if}
					{/each}
				{/each}
			</ul>
			<button class="mt-2 px-4 py-2 bg-red-500 text-white rounded" on:click={clearSelection}>
				Pulisci selezione
			</button>
		{/if}
	</div>
</div>

<style>
	table,
	thead tr,
	tbody tr,
	thead tr th {
		background-color: transparent;
		border: 0;
	}

	thead tr {
		margin-bottom: 20px;
	}

	thead tr th {
		font-size: 1rem;
	}

	tbody {
		border-bottom: 1px solid lightgray;
	}

	tbody tr {
		height: 50px;
		border-bottom: solid 1px;
	}

	tbody tr td {
		border: 0;
	}

	button {
		width: 25px;
		margin: 0 5px;
		background-color: transparent;
		cursor: pointer;
	}

	button:disabled {
		cursor: not-allowed;
		opacity: 0.5;
	}

	.font-bold {
		font-weight: bold;
	}
</style>
