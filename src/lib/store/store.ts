import { marked } from 'marked';
import { writable } from 'svelte/store';
export const isChatOpen = writable(false);
export const messages = writable<Message[]>([]);
export const selectedRows = writable(new Set());
export const isPlayerCardOpen = writable(false);

export function openChat() {
	isChatOpen.update(value => !value);
}

export function openChatWithAIMessage(aiMessage: Message) {
	updateMessages(aiMessage)
	isChatOpen.update(value => !value);
}

export function updateMessages(message: Message) {
	
	message.text = marked.parse(message.text) as string;

	messages.update(currentMessages => [...currentMessages, message]);
}

export function handlePlayerCardOpening() {
	isPlayerCardOpen.update(open => !open);
}

export type Message = {
	text: string;
	type: string;
	id ?: number;
	file?: string;
};
  