<script lang="ts">
	export let variant: 'primary' | 'accent' = 'primary';
</script>

<div class="flex justify-center items-center h-30 p-10">
	<div class={`animate-spin rounded-full h-10 w-10 border-b-2 border-${variant}`}></div>
</div>
