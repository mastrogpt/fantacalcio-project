<script lang="ts">
	import type { PlayersStats } from '$lib/service/getStats';

	export let data: PlayersStats;
</script>

<h1>{data.name}</h1>
<div>{data.team}</div>
