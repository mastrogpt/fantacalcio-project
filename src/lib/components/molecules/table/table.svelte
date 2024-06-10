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

	export let data: { [key: string]: string | number | boolean }[] = [];
	export let columns: { [key: string]: string | number }[] = [];
	export let globalFilter = '';

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
		getCoreRowModel: getCoreRowModel(),
		globalFilterFn: fuzzyFilter,
		getFilteredRowModel: getFilteredRowModel(),
		onSortingChange: setSorting,
		getSortedRowModel: getSortedRowModel()
	});

	const table = createSvelteTable(options);

	const handleKeyUp = (e: any) => {
		$table.setGlobalFilter(String(e?.target?.value));
	};
</script>

<div class="p-2">
	<h2 class="text-center text-2xl font-bold mb-4 text-black">Dettagli giocatore</h2>

	<input
		type="text"
		placeholder="Global filter"
		class="border w-full p-1 mb-4"
		bind:value={globalFilter}
		on:keyup={handleKeyUp}
	/>

	<table class="w-full border-collapse table-fixed">
		<thead>
			{#each $table.getHeaderGroups() as headerGroup}
				<tr>
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
									{#if header.column.getIsSorted().toString() === 'asc'}
										🔼
									{:else if header.column.getIsSorted().toString() === 'desc'}
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
				<tr class="odd:bg-light even:bg-white">
					{#each row.getVisibleCells() as cell}
						<td class="px-4 py-2 border text-black">
							<svelte:component this={flexRender(cell.column.columnDef.cell, cell.getContext())} />
						</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
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

	tbody tr td {
		border: 0;
		border-bottom: solid 1px;
	}
</style>
