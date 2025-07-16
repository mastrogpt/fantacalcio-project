import { getApiHost } from '$lib/store/store';
import axios from 'axios';

export interface ChatInput {
	message: string;
	file?: any;
	threadId?: string;
}

export async function chat(input: ChatInput): Promise<any> {
	
	const apiUrl = 'https://nuvolaris.org/api/v1/web/' + getApiHost() + '/chatwidget/chat';
	const headers = {
		'Content-Type': 'application/json'
	};

	const requestData = {
		message: input.message || 'Che ne pensi?',
		...(input.threadId && { thread_id: input.threadId }),
		...(input.file && { attachments: input.file })
	};

	try {
		const response = await axios.post(apiUrl, requestData, { headers });
		return response;
	} catch (error) {
		console.error('Error:', error);
		throw error;
	}
}
