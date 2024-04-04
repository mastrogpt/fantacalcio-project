import * as universal from '../entries/pages/_layout.ts.js';

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_layout.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/+layout.ts";
export const imports = ["_app/immutable/nodes/0.f9ba4adc.js","_app/immutable/chunks/scheduler.ce710c66.js","_app/immutable/chunks/index.86f09419.js","_app/immutable/chunks/singletons.0b7c80a0.js","_app/immutable/chunks/GreenButton.31f8d7a6.js","_app/immutable/chunks/BackButton.e6ae24c9.js","_app/immutable/chunks/public.ca8536a6.js"];
export const stylesheets = ["_app/immutable/assets/0.4b9a1b15.css"];
export const fonts = [];
