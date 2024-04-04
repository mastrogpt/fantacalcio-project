import { c as create_ssr_component, d as add_attribute, e as escape, v as validate_component } from "../../../../chunks/ssr.js";
import axios from "axios";
import { P as PUBLIC_URL_AI_SINGLE_PLAYER } from "../../../../chunks/public.js";
import { L as Loader } from "../../../../chunks/Loader.js";
const GreenButton = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { href = "#" } = $$props;
  let { text = "Download" } = $$props;
  let { clickAction = null } = $$props;
  function handleClick() {
    if (clickAction) {
      console.log("clicked");
      clickAction();
    }
  }
  if ($$props.href === void 0 && $$bindings.href && href !== void 0)
    $$bindings.href(href);
  if ($$props.text === void 0 && $$bindings.text && text !== void 0)
    $$bindings.text(text);
  if ($$props.clickAction === void 0 && $$bindings.clickAction && clickAction !== void 0)
    $$bindings.clickAction(clickAction);
  if ($$props.handleClick === void 0 && $$bindings.handleClick && handleClick !== void 0)
    $$bindings.handleClick(handleClick);
  return `<a class="group inline-block rounded-full bg-gradient-to-r from-green-500 via-green-200 to-light p-[2px] hover:text-white focus:outline-none focus:ring active:text-opacity-75"${add_attribute("href", href, 0)}><span class="block rounded-full bg-white px-8 py-3 text-sm font-medium group-hover:bg-transparent">${escape(text)}</span></a>`;
});
const BackButton = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { href = "#" } = $$props;
  let { text = "Download" } = $$props;
  let { clickAction = null } = $$props;
  if ($$props.href === void 0 && $$bindings.href && href !== void 0)
    $$bindings.href(href);
  if ($$props.text === void 0 && $$bindings.text && text !== void 0)
    $$bindings.text(text);
  if ($$props.clickAction === void 0 && $$bindings.clickAction && clickAction !== void 0)
    $$bindings.clickAction(clickAction);
  return `<a class="group inline-block rounded-full bg-gradient-to-r from-secondary via-secondary to-light p-[2px] hover:text-white focus:outline-none focus:ring active:text-opacity-75"${add_attribute("href", href, 0)}><span class="block rounded-full bg-white px-8 py-3 text-sm font-medium group-hover:bg-transparent">${escape(text)}</span></a>`;
});
function getAiOpinionFromBackend(input) {
  return axios.post(PUBLIC_URL_AI_SINGLE_PLAYER, {
    "input": input
  }).then((response) => {
    return response.data.output;
  }).catch((error) => {
    console.error(error);
    throw error;
  });
}
const DisabledButton = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { href = "#" } = $$props;
  let { text = "Download" } = $$props;
  let { clickAction = null } = $$props;
  if ($$props.href === void 0 && $$bindings.href && href !== void 0)
    $$bindings.href(href);
  if ($$props.text === void 0 && $$bindings.text && text !== void 0)
    $$bindings.text(text);
  if ($$props.clickAction === void 0 && $$bindings.clickAction && clickAction !== void 0)
    $$bindings.clickAction(clickAction);
  return `<a class="group inline-block rounded-full bg-gradient-to-r from-gray-200 via-gray-300 to-gray-500 p-[2px] hover:text-white focus:outline-none focus:ring active:text-opacity-75"${add_attribute("href", href, 0)}><span class="block rounded-full bg-white px-8 py-3 text-sm font-medium group-hover:bg-transparent">${escape(text)}</span></a>`;
});
const Person = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<div class="relative" role="tooltip"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="#1b81a5" class="w-6 h-6"><path d="M10 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM3.465 14.493a1.23 1.23 0 0 0 .41 1.412A9.957 9.957 0 0 0 10 18c2.31 0 4.438-.784 6.131-2.1.43-.333.604-.903.408-1.41a7.002 7.002 0 0 0-13.074.003Z"></path></svg> ${``}</div>`;
});
const Foot = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<div class="relative" role="tooltip"><svg width="800px" height="800px" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" fill="#ffa944" class="w-6 h-6"><title>footprint</title><g id="Layer_2" data-name="Layer 2"><g id="invisible_box" data-name="invisible box"><rect width="48" height="48" fill="none"></rect></g><g id="Q3_icons" data-name="Q3 icons"><path d="M20,5.8c.2,2.2-1.1,4.1-2.7,4.2S14.2,8.4,14,6.2,15.1,2.1,16.7,2,19.8,3.6,20,5.8ZM22.8,4c-1.1.1-1.9,1.5-1.8,3.1s1.1,3,2.2,2.9S25.1,8.5,25,6.9,23.9,3.9,22.8,4Zm4.3,2.3c-.8-.1-1.5.9-1.6,2.1s.6,2.3,1.4,2.3,1.5-.9,1.6-2.1S27.9,6.3,27.1,6.3ZM30.7,8c-.7-.1-1.5.7-1.7,1.8A1.8,1.8,0,0,0,30,12c.7.1,1.4-.7,1.6-1.8A1.9,1.9,0,0,0,30.7,8Zm3,2.5c-.6-.1-1.2.5-1.3,1.3a1.4,1.4,0,0,0,.6,1.7c.6.1,1.1-.5,1.3-1.3A1.4,1.4,0,0,0,33.7,10.5ZM20,12c-2,0-6,1-5,6s8,7,8,11-3,5-5,9,0,7,3,8a6.8,6.8,0,0,0,8-4c1-3-.6-4.2,1-9,1-3,3-4,4-10C35.4,14.9,27,12,20,12Z"></path></g></g></svg> ${``}</div>`;
});
const Ball = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  return `<div class="relative" role="tooltip"><svg fill="#000000" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="w-5 h-5 cursor-pointer" viewBox="0 0 31.492 31.492" xml:space="preserve"><g><path d="M15.796,0.049c-0.017,0-0.033,0.002-0.05,0.003c-0.017,0-0.033-0.003-0.05-0.003C7.028,0.049,0,7.076,0,15.745
		s7.028,15.698,15.696,15.698c0.017,0,0.033-0.002,0.05-0.004c0.017,0,0.033,0.004,0.05,0.004c8.668,0,15.696-7.028,15.696-15.697
		S24.464,0.049,15.796,0.049z M16.826,4.605l4.087-0.47c1.543,0.683,2.922,1.665,4.069,2.871l0.521,4.164l-5.051,1.327l-3.627-2.525
		V4.605z M6.509,7.006c1.148-1.206,2.527-2.188,4.07-2.871l4.087,0.47v5.367l-3.627,2.525L5.988,11.17L6.509,7.006z M4.594,21.889
		c-0.878-1.58-1.418-3.365-1.55-5.267l2.155-3.593l5.116,1.344l1.294,4.27l-3.331,4.965L4.594,21.889z M18.65,28.107
		c-0.92,0.212-1.872,0.334-2.854,0.336c-0.017,0-0.033-0.002-0.05-0.002s-0.033,0.002-0.05,0.002
		c-0.983-0.002-1.935-0.124-2.854-0.336l-2.885-3.411l3.254-4.847h2.535h2.535l3.254,4.847L18.65,28.107z M23.214,23.607
		l-3.331-4.965l1.295-4.27l5.115-1.344l2.155,3.593c-0.132,1.901-0.673,3.687-1.55,5.267L23.214,23.607z"></path></g></svg> ${``}</div>`;
});
const Card = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { color = "black" } = $$props;
  if ($$props.color === void 0 && $$bindings.color && color !== void 0)
    $$bindings.color(color);
  return `<div class="relative" role="tooltip"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"${add_attribute("fill", color, 0)} class="w-5 h-5"><path d="M5.25 3A2.25 2.25 0 0 0 3 5.25v9.5A2.25 2.25 0 0 0 5.25 17h9.5A2.25 2.25 0 0 0 17 14.75v-9.5A2.25 2.25 0 0 0 14.75 3h-9.5Z"></path></svg> ${``}</div>`;
});
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { data } = $$props;
  let aiOpinion;
  let aiOpinionWritingEffect;
  let isLoading = false;
  async function showMessage() {
    for (let i = 0; i < aiOpinion.length; i++) {
      aiOpinionWritingEffect = aiOpinion.substring(0, i + 1);
      await sleep(30);
    }
  }
  async function getAiOpinion() {
    isLoading = true;
    aiOpinion = await getAiOpinionFromBackend(data.playerData);
    showMessage();
    isLoading = false;
  }
  if ($$props.data === void 0 && $$bindings.data && data !== void 0)
    $$bindings.data(data);
  return `<div class="grid grid-cols-1 gap-4 lg:gap-8 mx-auto justify-center"><div class="h-32 rounded-lg bg-gray-200 lg:col-span-2"><div class="bg-gradient-to-r from-primary from-10% via-gray-200 via-30% to-gray-100 to-65%"><h2 class="text-2xl text-primary font-bold text-center mb-5"><strong>${escape(data.playerData.name)}</strong> -
				<strong class="text-primary">${escape(data.playerData.team)}</strong></h2> <div class="flex justify-end">${validate_component(BackButton, "BackButton").$$render($$result, { href: "/all", text: "Indietro" }, {}, {})} ${!aiOpinion && !isLoading ? `${validate_component(GreenButton, "GreenButton").$$render(
    $$result,
    {
      text: "AIpinion",
      clickAction: getAiOpinion
    },
    {},
    {}
  )}` : `${isLoading || aiOpinion ? `${validate_component(DisabledButton, "DisabledButton").$$render($$result, { text: "AIpinion" }, {}, {})}` : ``}`}</div></div> ${data ? `<div class="overflow-x-auto"><table class="min-w-full divide-y-2 divide-gray-200 bg-white text-sm"><thead class="ltr:text-left rtl:text-right"><tr><th class="whitespace-nowrap p-2 font-bold text-left">${validate_component(Person, "Person").$$render($$result, {}, {}, {})}</th> <th class="whitespace-nowrap p-2 font-bold text-left">${validate_component(Foot, "Foot").$$render($$result, {}, {}, {})}</th> <th class="whitespace-nowrap p-2 font-medium text-primary text-xl font-bold text-left">${validate_component(Ball, "Ball").$$render($$result, {}, {}, {})}</th> <th class="whitespace-nowrap p-2 font-medium text-primary text-xl font-bold text-left" data-svelte-h="svelte-4cs95j">Media</th> <th class="whitespace-nowrap p-2 font-medium text-primary text-xl font-bold text-left" data-svelte-h="svelte-16k0y5r">Fmedia</th> <th class="whitespace-nowrap p-2 font-medium text-primary text-xl font-bold text-left">${validate_component(Card, "Card").$$render($$result, { color: "#ef4444" }, {}, {})}</th> <th class="whitespace-nowrap p-2 font-medium text-primary text-xl font-bold text-left">${validate_component(Card, "Card").$$render($$result, { color: "#facc15" }, {}, {})}</th></tr></thead> <tbody><tr class="border-b"><td class="whitespace-nowrap p-4 font-medium text-gray-900">${escape(data.playerData.caps)}</td> <td class="whitespace-nowrap p-4 font-medium text-gray-900">${escape(data.playerData.assists)}</td> <td class="whitespace-nowrap p-4 font-medium text-gray-900">${escape(data.playerData.goals)}</td> <td class="whitespace-nowrap p-4 font-medium text-gray-900">${escape(data.playerData.markavg)}</td> <td class="whitespace-nowrap p-4 font-medium text-gray-900">${escape(data.playerData.fmarkavg)}</td> <td class="whitespace-nowrap p-2 font-medium text-gray-900">${escape(data.playerData.rcards)}</td> <td class="whitespace-nowrap p-2 font-medium text-gray-900">${escape(data.playerData.ycards)}</td></tr></tbody></table></div>` : ``} <div class="h-32 rounded-lg">${isLoading ? `${validate_component(Loader, "Loader").$$render($$result, {}, {}, {})}` : ``} ${aiOpinionWritingEffect && !isLoading ? `<div class="w-full overflow-auto bg-gradient-to-r from-gray-100 from-45% via-gray-200 to-primary p-[2px] mx-0.5 text-center">${escape(aiOpinionWritingEffect)}</div>` : ``}</div></div></div>`;
});
export {
  Page as default
};
