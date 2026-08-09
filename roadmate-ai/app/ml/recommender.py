def rank_places(places: list[dict]) -> list[dict]:
    ranked=[]
    for p in places:
        rating=float(p.get("rating") or 0);reviews=min(float(p.get("reviews") or 0),1000)/1000
        score=round(0.8*(rating/5.0)+0.2*reviews,4)
        ranked.append({**p,"recommendation_score":score})
    return sorted(ranked,key=lambda x:x["recommendation_score"],reverse=True)
