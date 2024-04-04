import * as universal from '../entries/pages/stats/_playerId_/_page.ts.js';

export const index = 6;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/stats/_playerId_/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/stats/[playerId]/+page.ts";
export const imports = ["_app/immutable/nodes/6.c27dd72f.js","_app/immutable/chunks/getStats.7adf5db8.js","_app/immutable/chunks/public.ca8536a6.js","_app/immutable/chunks/scheduler.ce710c66.js","_app/immutable/chunks/index.86f09419.js","_app/immutable/chunks/Loader.0c74833e.js","_app/immutable/chunks/BackButton.e6ae24c9.js","_app/immutable/chunks/GreenButton.31f8d7a6.js"];
export const stylesheets = [];
export const fonts = [];
