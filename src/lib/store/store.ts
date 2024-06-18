import { writable } from 'svelte/store';

export const chatMessage = writable('');
export const isChatOpen = writable(false);

export const selectedRows = writable(new Set());

export function openChatWithMessage(message) {
	chatMessage.set(message);
	isChatOpen.set(true);
}
