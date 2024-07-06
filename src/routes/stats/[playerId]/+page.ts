import { getStatsDataById } from '$lib/service/fantamaster/getStats';

export function load({ params }: { params: { playerId: number } }) {
    
    return getStatsDataById(params.playerId).then((result) => {
        const playerData = result;
        return { playerData };
    });
}
