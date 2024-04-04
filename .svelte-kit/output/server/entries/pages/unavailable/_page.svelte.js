import { c as create_ssr_component, v as validate_component } from "../../../chunks/ssr.js";
import { L as Loader } from "../../../chunks/Loader.js";
const UnavailablePlayers = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<div class="grid grid-cols-1 gap-2 lg:gap-8 mx-auto justify-center sm:w-auto"><div class="h-32 rounded-lg lg:col-span-2"><div class="overflow-x-auto rounded-t-lg"><h2 class="text-2xl text-primary font-bold text-center mb-5" data-svelte-h="svelte-1ly75cn">Gli indisponibili</h2> <div>${`${validate_component(Loader, "Loader").$$render($$result, {}, {}, {})}`}</div></div></div></div>`;
});
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `${validate_component(UnavailablePlayers, "UnavailablePlayers").$$render($$result, {}, {}, {})}`;
});
export {
  Page as default
};
