import { writable } from 'svelte/store';

export const chatMessage = writable('');
export const isChatOpen = writable(false);

export const selectedRows = writable(new Set());

export function openChatWithMessage() {
	console.log("STORE GO");
	isChatOpen.update(value => !value);
}