"""
DSPy Logic for Chatbot

This module contains DSPy signatures and modules for the chatbot functionality.
"""

import dspy
from dspy.teleprompt import BootstrapFewShot
from django.conf import settings
import os


# Configure DSPy with OpenAI
lm = dspy.LM("openai/gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
dspy.configure(lm=lm)


# ============================================================================
# DSPy Signatures and Modules
# ============================================================================

class ChemistryQASignature(dspy.Signature):
    """Answer chemistry questions based on Class 10 Chemical Reactions and Equations."""

    question = dspy.InputField(desc="Chemistry question from Chapter 1")
    answer = dspy.OutputField(desc="Accurate answer to the chemistry question")


class ChemistryQAModule(dspy.Module):
    """Chemistry QA module using ChainOfThought with few-shot learning."""

    def __init__(self):
        super().__init__()
        self.generate_answer = dspy.ChainOfThought(ChemistryQASignature)

    def forward(self, question):
        result = self.generate_answer(question=question)
        return result.answer


def chemistry_answer_metric(example, pred, trace=None):
    """Simple metric for chemistry answers based on word overlap."""
    # Handle both string predictions and object predictions
    if isinstance(pred, str):
        pred_answer = pred.lower().strip()
    else:
        pred_answer = pred.answer.lower().strip()

    gold_answer = example.answer.lower().strip()

    if pred_answer == gold_answer:
        return 1.0

    gold_terms = set(gold_answer.split())
    pred_terms = set(pred_answer.split())

    overlap = len(gold_terms.intersection(pred_terms))
    total = len(gold_terms)

    return overlap / total if total > 0 else 0.0


def load_chemistry_eval_dataset():
    """Load the chemistry evaluation dataset."""
    import json

    dataset_path = os.path.join(settings.BASE_DIR, 'chemistry_eval_dataset.json')

    try:
        with open(dataset_path, 'r') as f:
            data = json.load(f)

        examples = []
        for item in data:
            if item['type'] == 'multiple_choice':
                question_text = f"{item['question']}\nOptions:\n"
                for i, opt in enumerate(item['options'], 1):
                    question_text += f"{i}. {opt}\n"

                example = dspy.Example(
                    question=question_text,
                    answer=item['answer']
                ).with_inputs("question")
            else:
                example = dspy.Example(
                    question=item['question'],
                    answer=item['answer']
                ).with_inputs("question")

            examples.append(example)

        return examples
    except FileNotFoundError:
        print(f"Dataset not found at {dataset_path}")
        return []


def evaluate_chemistry_qa(devset=None, metric=None):
    """
    Evaluate the Chemistry QA model on a dataset.

    Args:
        devset: Development/test dataset (list of dspy.Example)
        metric: Evaluation metric function

    Returns:
        Evaluation score
    """
    if devset is None:
        # Load default dataset
        all_examples = load_chemistry_eval_dataset()
        # Use last 20% as dev set
        devset = all_examples[int(0.8 * len(all_examples)):]

    if metric is None:
        metric = chemistry_answer_metric

    # Initialize model
    chemistry_qa = ChemistryQAModule()

    # Evaluate
    evaluator = dspy.evaluate.Evaluate(
        devset=devset,
        metric=metric,
        num_threads=1,
        display_progress=True,
        display_table=5
    )

    score = evaluator(chemistry_qa)
    return score


def optimize_chemistry_qa(trainset=None, valset=None, metric=None,
                          max_bootstrapped_demos=4, max_labeled_demos=3,
                          max_rounds=1):
    """
    Optimize the Chemistry QA model using BootstrapFewShot.

    Args:
        trainset: Training dataset (list of dspy.Example)
        valset: Validation dataset (list of dspy.Example) - optional
        metric: Evaluation metric function
        max_bootstrapped_demos: Max demos to generate per example
        max_labeled_demos: Max demos to include in prompt
        max_rounds: Number of optimization rounds

    Returns:
        Compiled/optimized ChemistryQAModule
    """
    if trainset is None:
        # Load default dataset and split
        all_examples = load_chemistry_eval_dataset()
        train_size = int(0.6 * len(all_examples))
        val_size = int(0.2 * len(all_examples))

        trainset = all_examples[:train_size]
        if valset is None:
            valset = all_examples[train_size:train_size + val_size]

    if metric is None:
        metric = chemistry_answer_metric

    print(f"\nOptimizing Chemistry QA with BootstrapFewShot...")
    print(f"  Training examples: {len(trainset)}")
    if valset:
        print(f"  Validation examples: {len(valset)}")
    print(f"  Max bootstrapped demos: {max_bootstrapped_demos}")
    print(f"  Max labeled demos: {max_labeled_demos}")
    print(f"  Max rounds: {max_rounds}\n")

    # Initialize the base module
    chemistry_qa = ChemistryQAModule()

    # Create the optimizer
    optimizer = BootstrapFewShot(
        metric=metric,
        max_bootstrapped_demos=max_bootstrapped_demos,
        max_labeled_demos=max_labeled_demos,
        max_rounds=max_rounds
    )

    # Compile the program
    compiled_qa = optimizer.compile(
        student=chemistry_qa,
        trainset=trainset
    )

    print("\nOptimization complete!")
    return compiled_qa


def save_optimized_model(compiled_model, filename='optimized_chemistry_qa.json'):
    """Save the optimized model to a file."""
    filepath = os.path.join(settings.BASE_DIR, filename)
    compiled_model.save(filepath)
    print(f"Optimized model saved to: {filepath}")
    return filepath


def load_optimized_model(filename='optimized_chemistry_qa.json'):
    """Load an optimized model from a file."""
    filepath = os.path.join(settings.BASE_DIR, filename)

    if not os.path.exists(filepath):
        print(f"No optimized model found at {filepath}")
        print("Returning base model. Run optimization first.")
        return ChemistryQAModule()

    chemistry_qa = ChemistryQAModule()
    chemistry_qa.load(filepath)
    print(f"Loaded optimized model from: {filepath}")
    return chemistry_qa


def get_chemistry_response(question):
    """
    Get a response to a chemistry question.

    Args:
        question: The chemistry question

    Returns:
        Answer string
    """
    chemistry_qa = load_optimized_model()
    answer = chemistry_qa.forward(question=question)
    return answer
