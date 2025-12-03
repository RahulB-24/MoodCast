def score_basic(track, target_valence=None, target_energy=None, language=None):
    # simple hybrid scoring: popularity + language heuristics
    pop = track.get("popularity", 0) / 100.0
    score = pop * 0.6

    # language heuristic: if language requested, bump tracks with market match
    if language and language.lower() != "none":
        # naive market-language mapping; adjust as needed
        if language.lower() in ["ta", "tamil"] and ("IN" in (track.get("available_markets") or [])):
            score += 0.2
    # small artist/track name match bonus could be added by frontend / query
    return score

def score_smart(features, target_valence, target_energy, popularity=0):
    if features is None:
        # fallback to popularity weight
        return (popularity / 100.0) * 0.2
    energy = features.get("energy", 0)
    valence = features.get("valence", 0)
    dance = features.get("danceability", 0)
    score = 0
    # closeness to target, normalized
    score += (1 - abs(energy - target_energy))
    score += (1 - abs(valence - target_valence))
    score += dance * 0.1
    # small popularity boost
    score += (popularity / 100.0) * 0.1
    return score
