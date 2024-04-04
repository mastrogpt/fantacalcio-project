import { c as create_ssr_component, v as validate_component } from "../../../chunks/ssr.js";
import { L as Loader } from "../../../chunks/Loader.js";
const Lineup = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<body><div class="flex items-center justify-center"><div class="mx-auto">${`${validate_component(Loader, "Loader").$$render($$result, {}, {}, {})}`} ${``}</div></div> ${``} ${``} ${``}</body>`;
});
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `${validate_component(Lineup, "Lineup").$$render($$result, {}, {}, {})}`;
});
export {
  Page as default
};
