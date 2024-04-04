import { c as create_ssr_component } from "./ssr.js";
const Loader = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<div class="flex justify-center items-center h-30 p-10" data-svelte-h="svelte-1v3dpsy"><div class="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div></div>`;
});
export {
  Loader as L
};
