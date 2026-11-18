

def check_proposal(method, proposed, scores, expected, tolerance=0.5):
    if method not in scores:
        return "reject", f"'{method}' is not a valid method."
    best = min(scores.values())
    if scores[method] - best > tolerance:
        return "reject", f"{method} scores {scores[method]}, well above the best {best}."
    if proposed != expected:
        return "reject", "Forecast numbers don't match the tool output."
    return "approve", ""