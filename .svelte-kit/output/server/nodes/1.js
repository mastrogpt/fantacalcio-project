

export const index = 1;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_error.svelte.js')).default;
export const imports = ["_app/immutable/nodes/1.c6bdb1b5.js","_app/immutable/chunks/scheduler.ce710c66.js","_app/immutable/chunks/index.86f09419.js"];
export const stylesheets = [];
export const fonts = [];
