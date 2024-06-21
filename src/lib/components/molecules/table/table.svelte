<script lang="ts">
	import Button from '$lib/components/atoms/button/button.svelte';
	import { selectedRows } from '$lib/store/store';
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

	// Props
	export let data: any[] = [];
	export let columns: any[] = [];
	export let selectableRows: boolean = false;
	export let onRowClick: (data: any) => void;

	// Fuzzy filter for search
	const fuzzyFilter: FilterFn<any> = (row, columnId, value, addMeta) => {
		const itemRank = rankItem(row.getValue(columnId), value);
		addMeta({ itemRank });
		return itemRank.passed;
	};

	// Sorting state
	let sorting: SortingState = [];

	// Function to set sorting state
	const setSorting: OnChangeFn<SortingState> = (updater) => {
		if (typeof updater === 'function') {
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

	// Store for the data
	const dataStore = writable(data);

	// Options for the table
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
		getPaginationRowModel: getPaginationRowModel(),
		autoResetPageIndex: true,
		getCoreRowModel: getCoreRowModel(),
		globalFilterFn: fuzzyFilter,
		getFilteredRowModel: getFilteredRowModel(),
		onSortingChange: setSorting,
		getSortedRowModel: getSortedRowModel()
	});

	// Create the table instance
	const table = createSvelteTable(options);

	// Set the number of rows per page
	let pageSize = 10;
	$table.setPageSize(pageSize);

	// Handle global filter (search)
	const handleKeyUp = (e: any) => {
		$table.setGlobalFilter(String(e?.target?.value));
	};

	// Handle checkbox selection of rows
	const handleCheckboxChange = (row) => {
		selectedRows.update((rows) => {
			const newRows = new Set(rows);
			const foundRow = Array.from(newRows).find((r: any) => r.id === row.original.id);

			if (foundRow) {
				newRows.delete(foundRow);
			} else {
				if (newRows.size < 2) {
					newRows.add(row.original);
				}
			}

			return newRows;
		});
	};

	// Handle row click
	const handleRowClick = (row) => {
		if (onRowClick) return onRowClick(row);

		selectedRows.update((rows) => {
			const newRows = new Set(rows);
			const foundRow = Array.from(newRows).find((r: any) => r.id === row.original.id);

			if (foundRow) {
				newRows.delete(foundRow);
			} else {
				if (newRows.size < 2) {
					newRows.add(row.original);
				}
			}

			return newRows;
		});
	};

	// Function to update the table data
	export function updateData(newData) {
		dataStore.set(newData);
		options.update((opt) => ({ ...opt, data: newData }));
	}
</script>

<div class="p-2">
	<!-- Global filter (search) -->
	<div class="mb-4">
		<input
			type="text"
			placeholder="Search..."
			class="w-full px-4 py-2 border border-gray-300 rounded"
			on:keyup={handleKeyUp}
		/>
	</div>

	<!-- Table -->
	<table class="w-full border-collapse table-fixed">
		<thead>
			{#each $table.getHeaderGroups() as headerGroup}
				<tr>
					<!-- Empty header for checkboxes -->
					<th class="px-4 py-2 text-left border border-gray-300"></th>
					{#each headerGroup.headers as header}
						<th class="px-4 py-2 text-left border border-gray-300" colSpan={header.colSpan}>
							{#if !header.isPlaceholder}
								<!-- svelte-ignore a11y-click-events-have-key-events -->
								<!-- svelte-ignore a11y-no-static-element-interactions -->
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
					{#if selectableRows}
						<td class="px-4 py-2 border text-black flex items-center" on:click|stopPropagation>
							<input
								type="checkbox"
								on:change={() => handleCheckboxChange(row)}
								checked={Array.from($selectedRows).some((r) => r.id === row.original.id)}
								disabled={Array.from($selectedRows).length >= 2 &&
									!Array.from($selectedRows).some((r) => r.id === row.original.id)}
								class="mr-2"
							/>
						</td>
					{/if}

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
		<button on:click={() => $table.previousPage()} disabled={!$table.getCanPreviousPage()}
			>Prev</button
		>

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
		<button on:click={() => $table.nextPage()} disabled={!$table.getCanNextPage()}>Next</button>
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
