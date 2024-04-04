import { c as create_ssr_component, v as validate_component } from "../../../chunks/ssr.js";
import { L as Loader } from "../../../chunks/Loader.js";
const Comparator = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<div class="grid grid-cols-1 gap-4 lg:gap-8 mx-auto justify-center sm:w-auto"><div class="h-32 rounded-lg lg:col-span-2"><h2 class="text-2xl text-primary font-bold text-center mb-5" data-svelte-h="svelte-8hihhe">Tutti i giocatori</h2> ${`${validate_component(Loader, "Loader").$$render($$result, {}, {}, {})}`}</div> ${``} ${``}</div>`;
});
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `${validate_component(Comparator, "Comparator").$$render($$result, {}, {}, {})}`;
});
export {
  Page as default
};
