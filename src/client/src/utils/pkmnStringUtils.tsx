export function prettifyPkmnName(pkmn: string): string {
    let prettifyPkmn = pkmn
        .split(" ")
        .map((pkmn) => pkmn.charAt(0).toUpperCase() + pkmn.slice(1))
        .join(" ");
    // Capitalize after every hyphen
    prettifyPkmn = prettifyPkmn.replace(/\-[a-z]/g, (match) =>
        match.toUpperCase()
    );
    return prettifyPkmn;
}

export function convertToPkmnSpritePath(pkmn: string): string {
    // Source: https://play.pokemonshowdown.com/sprites/gen5/
    let sanitizedPkmn = pkmn.replace(/\s/g, "");
    return sanitizedPkmn;
}
