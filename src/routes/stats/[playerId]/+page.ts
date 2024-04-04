import { getStatsDataById } from '$lib/service/getStats';

export function load({ params }: { params: { playerId: number } }) {
    
    return getStatsDataById(params.playerId).then((result) => {
        const playerData = result;
        return { playerData };
    });
}
