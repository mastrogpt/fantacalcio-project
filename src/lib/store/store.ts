import { chat, type ChatInput } from '$lib/service/nuvBot';
import { marked } from 'marked';
import { writable, get } from 'svelte/store';

export const isChatOpen = writable(false);
export const messages = writable<Message[]>([]);
export const selectedRows = writable(new Set());
export const isPlayerCardOpen = writable(false);
export const threadId = writable<string | null>(null);


export function handleNuvBotChatOpening(open?: boolean) {
    if(open) {
        isChatOpen.set(open);
    }
    else {
        isChatOpen.update(value => !value);
    }
}

export function updateMessages(message: Message) {
    message.text = marked.parse(message.text) as string;
    messages.update(currentMessages => [...currentMessages, message]);
}


export function handlePlayerCardOpening() {
    isPlayerCardOpen.update(open => !open);
}

export function nuvbotChat(userMessage: ChatInput): Promise<string> {
    const currentThreadId = get(threadId);

    const payload: any = {
        message: userMessage.message,
    };

    if (currentThreadId) {
        payload.threadId = currentThreadId;
        payload.file = userMessage.file || undefined;
    }

    return chat(payload)
        .then(aiResponse => {
            threadId.set(aiResponse?.data?.id || null);
            updateMessages({ type: 'ai', text: aiResponse?.data?.output[0]?.text?.value });
            return aiResponse.data.output[0].text.value; 
        })
        .catch(error => {
            console.error("Error in nuvbotChat:", error);
            throw error; 
        });
}


export type Message = {
    text: string;
    type: string;
    id?: number;
    file?: string;
};
