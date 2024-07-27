<!-- ChatMessage.svelte -->
<script>
	import * as marked from 'marked';
	import { onMount } from 'svelte';

	import AiWidgetIcon from './AiWidgetIcon.svelte';
	import UserWidgetIcon from './UserWidgetIcon.svelte';

	export let message;

	let formattedMessage = '';

	onMount(() => {
		formattedMessage = marked.parse(message.text);
	});
</script>

<div class="flex gap-3 my-4 text-gray-600 text-sm flex-1">
	{#if message.type === 'ai'}
		<span
			class="relative flex shrink-0 overflow-hidden rounded-full w-8 h-8 bg-gray-100 border p-1"
		>
			<AiWidgetIcon />
		</span>
		<p class="leading-relaxed font-bold text-gray-700">AI</p>
	{:else if message.type === 'user'}
		<span
			class="relative flex shrink-0 overflow-hidden rounded-full w-8 h-8 bg-gray-100 border p-1"
		>
			<UserWidgetIcon />
		</span>
		<p class="leading-relaxed font-bold text-gray-700">You</p>
	{/if}
	{#if formattedMessage}
		<p class="leading-relaxed">{@html formattedMessage}</p>
	{/if}
</div>
