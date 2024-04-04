

export const index = 2;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_page.svelte.js')).default;
export const imports = ["_app/immutable/nodes/2.d3bec9c4.js","_app/immutable/chunks/scheduler.ce710c66.js","_app/immutable/chunks/index.86f09419.js","_app/immutable/chunks/Loader.0c74833e.js","_app/immutable/chunks/public.ca8536a6.js"];
export const stylesheets = [];
export const fonts = [];
