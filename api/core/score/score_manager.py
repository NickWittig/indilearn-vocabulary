from api.config.config import ScoreConfig


class ScoreManager:
    @staticmethod
    def get_score(is_correct, error_codes) -> int:
        if is_correct:
            score = ScoreConfig.SCORE_CORRECT
        elif is_correct is False and len(error_codes) > 0:
            score = ScoreConfig.SCORE_MISTAKE
        else:
            score = ScoreConfig.SCORE_WRONG
        return score
