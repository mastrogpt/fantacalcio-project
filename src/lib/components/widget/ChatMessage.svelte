<!-- ChatMessage.svelte -->
<script>
	import * as marked from 'marked';
	import { onMount } from 'svelte';

	import AiWidgetIcon from './AiWidgetIcon.svelte';
	import UserWidgetIcon from './UserWidgetIcon.svelte';

	export let message;

	let formattedMessage = '';
	let imageMessage = '';

	onMount(() => {
		formattedMessage = marked.parse(message.text);
		imageMessage = message?.file;
	});
</script>

<div class="flex flex-col gap-3 my-4 text-gray-600 text-sm flex-1 shadow-sm">
	{#if message.type === 'ai'}
		<div class="flex itemx-center gap-2">
			<span
				class="relative flex shrink-0 overflow-hidden rounded-full w-8 h-8 bg-gray-100 border p-1"
			>
				<AiWidgetIcon />
			</span>
			<p class="leading-relaxed font-bold text-[#de6d1c]">AI</p>
		</div>
	{:else if message.type === 'user'}
		<div class="flex itemx-center gap-2">
			<span
				class="relative flex shrink-0 overflow-hidden rounded-full w-8 h-8 bg-gray-100 border p-1"
			>
				<UserWidgetIcon />
			</span>
			<p class="leading-relaxed font-bold text-primary">Tu</p>
		</div>
	{/if}

	{#if formattedMessage}
		{#if imageMessage}
			<div class="flex flex-col">
				<img src={imageMessage} class="object-contain h-20 w-auto mx-auto" alt="Preview" />

				<p class="leading-relaxed">{@html formattedMessage}</p>
			</div>
		{:else}
			<p class="leading-relaxed">{@html formattedMessage}</p>
		{/if}
	{/if}
</div>
