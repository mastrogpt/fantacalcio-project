<!-- Chat.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { chat, notifySlack } from '$lib/service/assistantApi';
	import MinimizedIcon from './MinimizedIcon.svelte';
	import MaximizeIcon from './MaximizeIcon.svelte';
	import ChatMessage from './ChatMessage.svelte';
	import MessageIcon from './MessageIcon.svelte';
	import Loader from '../atoms/Loader.svelte';
	import Button from '../atoms/button/button.svelte';

	let messages: { type: string; text: string; id: number }[] = [];
	let userMessage: string = '';
	let isLoading = false;
	let isMinimized = true;
	let lastMessageIsUser = true;

	const regexEmail = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/;

	function handleKeyPress(event: { key: string }) {
		if (event.key === 'Enter' && !isLoading) {
			postMessage();
		}
	}

	async function postMessage() {
		lastMessageIsUser = true;
		if (regexEmail.test(userMessage)) {
			isLoading = true;
			const aiResponse = await chat(
				"user has sent its email, maybe he need assistance. Tell him that we'll provide it as soon as possible. Use user language. User message is: " +
					userMessage
			);
			isLoading = false;
			await notifySlack('Someone sent this message from nuvolaris widget: ' + userMessage);
			messages = [...messages, { type: 'ai', text: aiResponse, id: messages.length }];
			lastMessageIsUser = false;
			userMessage = '';

			showMessage();
			return;
		}
		messages = [...messages, { type: 'user', text: userMessage, id: messages.length }];

		isLoading = true;
		const aiResponse = await chat(userMessage);

		isLoading = false;
		messages = [...messages, { type: 'ai', text: aiResponse, id: messages.length }];
		lastMessageIsUser = false;
		userMessage = '';

		showMessage();
	}

	onMount(() => {
		showMessage();
		messages = [
			...messages,
			{
				type: 'ai',
				text: "Benvenuto! 🤓 Te serve 'n consiglio pe' l'asta? Voi fa' 'na chiacchierata? Dimme 'n po'!",
				id: messages.length
			}
		];
	});

	async function showMessage() {
		// Scroll to bottom
		const chatContainer = document.getElementById('chat-container');
		if (chatContainer) {
			chatContainer.scrollTop = chatContainer.scrollHeight;
		}
	}

	function toggleMinimize() {
		isMinimized = !isMinimized;
	}
</script>

{#if !isMinimized}
	<div
		id="chat-container"
		class="fixed bottom-4 right-4 bg-white p-2 rounded-lg border border-[#e5e7eb] shadow z-20
    w-[90vw] h-[70vh] sm:w-[80vw] sm:h-[60vh] md:w-[60vw] md:h-[50vh] lg:w-[440px] lg:h-[534px]"
	>
		<button class="absolute top-2 right-2" on:click={toggleMinimize}>
			{#if isMinimized}
				<MaximizeIcon />
			{:else}
				<MinimizedIcon />
			{/if}
		</button>

		<div class="flex flex-col space-y-1.5 pb-6">
			<h2 class="font-semibold text-lg tracking-tight">🌧️ 🖥️ 🌩️</h2>
			<p class="text-sm text-[#6b7280] leading-3"><strong> Hi from MastroGPT 👋</strong></p>
		</div>

		<!-- Chat Messages -->
		<div
			class="pr-2 h-[calc(70vh-140px)] sm:h-[calc(60vh-140px)] md:h-[calc(50vh-140px)] lg:h-[374px] overflow-auto"
		>
			{#each messages as message}
				<ChatMessage {message} />
			{/each}
			{#if lastMessageIsUser && isLoading}
				<Loader />
			{/if}
		</div>

		<div class="mt-2 flex flex-row items-center space-y-2 sm:space-y-0 sm:space-x-2">
			<input
				type="text"
				class="flex-1 border rounded-md px-2 py-2 focus:outline-none focus:ring focus:border-blue-300"
				placeholder="Type your message..."
				bind:value={userMessage}
				on:keypress={handleKeyPress}
			/>
			<Button variant="accent" label="Submit" onClick={postMessage} />
		</div>
	</div>
{/if}

{#if isMinimized}
	<div id="chat-container" class="fixed bottom-4 right-4 p-6 rounded-lg w-[30px] h-[30px] z-20">
		<button class="absolute bottom-4 right-4" on:click={toggleMinimize}>
			<MessageIcon />
		</button>
	</div>
{/if}
