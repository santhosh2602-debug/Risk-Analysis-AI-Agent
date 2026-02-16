from app.models import EvaluationResult


class Evaluator:
    def evaluate(self) -> EvaluationResult:
        return EvaluationResult(
            relevance=4.5,
            clarity=5.0,
            coverage=4.0
        )
