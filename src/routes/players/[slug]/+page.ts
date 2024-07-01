import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { getStatsDataById } from '$lib/service/getStats';

// export const load: PageLoad = ({ params }) => {
// 	if (params.slug === '14469') {
// 		return { title: 'Hello world!', content: 'Welcome to our blog. Lorem ipsum dolor sit amet...' };
// 	}

// 	return error(404, 'Not found');
// };

export const load: PageLoad = ({ params }) => {
	if (!params.slug) return error(404, 'Not found');

	return getStatsDataById(Number(params.slug)).then((data) => data);
};
