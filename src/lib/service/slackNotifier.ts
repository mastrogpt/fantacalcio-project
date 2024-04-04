import axios from 'axios';
import { PUBLIC_URL_SLACK_NOTIFY } from '$env/static/public';

export function sendMessage(userMessage: string): Promise<any> {
	const headers = {
		'Content-Type': 'application/json'
	};
	const data = {
		input: userMessage
	};

	return axios.post(PUBLIC_URL_SLACK_NOTIFY, data, { headers });
}
