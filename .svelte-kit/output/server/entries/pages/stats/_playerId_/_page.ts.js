import axios from "axios";
import { a as PUBLIC_URL_STATS } from "../../../../chunks/public.js";
function getStatsData() {
  return axios.get(PUBLIC_URL_STATS).then((response) => {
    return response.data.players;
  }).catch((error) => {
    console.error(error);
    throw error;
  });
}
async function getStatsDataById(id) {
  try {
    const allPlayers = await getStatsData();
    const player = allPlayers.find((p) => p.id == id);
    if (player) {
      return player;
    } else {
      throw new Error(`Player with ID ${id} not found.`);
    }
  } catch (error) {
    console.error(error);
    throw error;
  }
}
function load({ params }) {
  return getStatsDataById(params.playerId).then((result) => {
    const playerData = result;
    return { playerData };
  });
}
export {
  load
};
