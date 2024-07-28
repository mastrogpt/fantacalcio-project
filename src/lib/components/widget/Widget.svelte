<script lang="ts">
	import { onMount } from 'svelte';
	import { chat } from '$lib/service/nuvBot';
	import MinimizedIcon from './MinimizedIcon.svelte';
	import MaximizeIcon from './MaximizeIcon.svelte';
	import ChatMessage from './ChatMessage.svelte';
	import MessageIcon from './MessageIcon.svelte';
	import Loader from '../atoms/Loader.svelte';
	import Button from '../atoms/button/button.svelte';
	import UploadIcon from './UploadIcon.svelte';

	let messages: { type: string; text: string; id: number; file?: string }[] = [];
	let userMessage: string = '';
	let isLoading = false;
	let isMinimized = true;
	let lastMessageIsUser = true;
	let threadId = '';

	let files: FileList | null = null;
	let filePreview: string | null = null;

	const regexEmail = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/;

	$: if (files && files.length > 0) {
		filePreview = URL.createObjectURL(files[0]);
	} else {
		filePreview = null;
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter' && !isLoading) {
			postMessage();
		}
	}

	async function postMessage() {
		lastMessageIsUser = true;

		const message = {
			type: 'user',
			text: userMessage,
			id: messages.length,
			file: filePreview
		};

		messages = [...messages, message];
		isLoading = true;

		let fileBase64 = '';

		if (files && files.length > 0) {
			fileBase64 = await toBase64(files[0]);
		}

		const payload = {
			message: userMessage,
			file: fileBase64
		};

		const aiResponse = await chat(payload, threadId);
		threadId = aiResponse?.data?.id;

		isLoading = false;
		messages = [
			...messages,
			{ type: 'ai', text: aiResponse?.data?.output[0]?.text?.value, id: messages.length }
		];
		lastMessageIsUser = false;
		userMessage = '';
		files = null;
		filePreview = null;

		showMessage();
	}

	function toBase64(file: File): Promise<string> {
		return new Promise((resolve, reject) => {
			const reader = new FileReader();
			reader.readAsDataURL(file);
			reader.onload = () => resolve(reader.result as string);
			reader.onerror = (error) => reject(error);
		});
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

	function showMessage() {
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
		class="flex flex-col fixed bottom-4 right-4 bg-white p-2 rounded-lg border border-[#e5e7eb] shadow z-20
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
			<p class="text-sm text-[#6b7280] leading-3"><strong> Ciao da FantaCarcio! 👋</strong></p>
		</div>

		<!-- Chat Messages -->
		<div class="pr-2 flex-1 overflow-auto">
			{#each messages as message}
				<ChatMessage {message} />
			{/each}
			{#if lastMessageIsUser && isLoading}
				<Loader />
			{/if}
		</div>

		<div class="mt-2 flex items-center space-y-2 sm:space-y-0 sm:space-x-2 w-[100%]">
			<div class="flex flex-col w-[100%] gap-2">
				{#if filePreview}
					<img src={filePreview} class="object-contain h-20 w-auto mx-auto" alt="Preview" />
				{/if}

				<div class="flex flex-1 w-[100%] gap-1 items-center justify-center">
					<input
						accept="image/png, image/jpeg"
						bind:files
						id="upload-file"
						name="upload-file"
						type="file"
						placeholder=""
						class="min-h-0 min-w-0 h-0 w-0 overflow-hidden"
					/>

					<label for="upload-file">
						<UploadIcon />
					</label>

					<input
						type="text"
						class="flex-1 border rounded-md px-2 py-2 focus:outline-none focus:ring focus:border-blue-300"
						placeholder="Scrivi il tuo messaggio..."
						bind:value={userMessage}
						on:keypress={handleKeyPress}
					/>

					<Button size="small" variant="accent" label="Submit" onClick={postMessage} />
				</div>
			</div>
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
