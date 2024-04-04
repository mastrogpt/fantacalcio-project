import { c as create_ssr_component, d as add_attribute, v as validate_component } from "../../chunks/ssr.js";
import { L as Loader } from "../../chunks/Loader.js";
const football = "/_app/immutable/assets/football.8bd74c0c.png";
const footballVertical = "/_app/immutable/assets/footballVertical.be149ba5.png";
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<div><div class="w-full mt-2 bg-gray-900 h-96"><div class="relative h-full sm:block"><img alt=""${add_attribute("src", footballVertical, 0)} class="absolute inset-0 w-full h-120 object-cover block lg:hidden"> <img alt=""${add_attribute("src", football, 0)} class="absolute inset-0 w-full h-120 object-cover hidden lg:block"> <div class="m-4 p-2 absolute flex items-center justify-center lg:w-2/5 sm:w-3/5 bg-opacity-85 bg-gray-900 rounded-lg">${`${validate_component(Loader, "Loader").$$render($$result, {}, {}, {})}`}</div></div></div></div>`;
});
export {
  Page as default
};
