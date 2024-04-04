

export const index = 5;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/lineup/_page.svelte.js')).default;
export const imports = ["_app/immutable/nodes/5.1a6ecb7e.js","_app/immutable/chunks/scheduler.ce710c66.js","_app/immutable/chunks/index.86f09419.js","_app/immutable/chunks/each.e59479a4.js","_app/immutable/chunks/Loader.0c74833e.js","_app/immutable/chunks/public.ca8536a6.js","_app/immutable/chunks/GreenButton.31f8d7a6.js"];
export const stylesheets = [];
export const fonts = [];
