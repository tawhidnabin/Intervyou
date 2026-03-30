def generate_feedback(speaking_rate, filler_count, pause_count, relevance_score, fluency_score):
    """Generate 3-4 sentence feedback based on analysis metrics."""
    sentences = []

    # Speaking rate feedback
    if speaking_rate < 100:
        sentences.append('Your speaking pace was a little slow — try to speak more naturally and confidently to keep the interviewer engaged.')
    elif speaking_rate > 170:
        sentences.append('You spoke quite quickly; slowing down slightly will help the interviewer follow your points more easily.')
    else:
        sentences.append('Your speaking pace was well-balanced, making your answer easy to follow.')

    # Filler word feedback
    if filler_count > 10:
        sentences.append(f'You used filler words ({filler_count} times) quite frequently — practising your answers aloud will help reduce these significantly.')
    elif filler_count > 5:
        sentences.append(f'You used a few filler words ({filler_count} times); being mindful of pausing silently instead will improve your delivery.')
    else:
        sentences.append('Great job keeping filler words to a minimum — your delivery sounded polished and professional.')

    # Relevance feedback
    if relevance_score < 0.35:
        sentences.append('Your answer did not closely address the question; try using the STAR method (Situation, Task, Action, Result) to structure a more relevant response.')
    elif relevance_score < 0.6:
        sentences.append('Your answer was partially relevant — focus on directly addressing what was asked and supporting your points with specific examples.')
    else:
        sentences.append('Your answer was highly relevant to the question, demonstrating a clear understanding of what was being asked.')

    # Pause feedback
    if pause_count > 15:
        sentences.append('There were many pauses in your response; more practice will help you speak more fluently and with greater confidence.')

    return ' '.join(sentences)


def compute_overall_score(relevance_score, fluency_score):
    """Compute overall score as weighted average of relevance and fluency (0–100)."""
    return round(relevance_score * 50 + fluency_score * 50, 1)
