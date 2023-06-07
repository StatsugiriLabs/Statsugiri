export function getPkmnSpriteName(pkmn: string): string {
    // Source: https://play.pokemonshowdown.com/sprites/gen5/
    let sanitizedPkmn = pkmn.replace(/\s/g, "");
    return sanitizedPkmn;
}
