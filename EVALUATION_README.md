# DSPy Evaluation Setup for Chemistry Chatbot

## 📁 Files Created

1. **chemistry_eval_dataset.json** - Evaluation dataset with 30 questions from Chapter 1: Chemical Reactions and Equations
2. **chat/dspy_logic.py** - Updated with evaluation metrics and Chemistry QA module
3. **test_evaluation.py** - Script to run evaluations
4. **dspy_eval_example.py** - Example usage patterns

## 📊 Dataset Structure

The evaluation dataset contains 30 carefully crafted questions covering:

### Question Types:
- **short_answer** - Short answer questions
- **definition** - Definition-based questions
- **conceptual** - Conceptual understanding questions
- **multiple_choice** - MCQ questions
- **reaction_balancing** - Chemical equation balancing
- **observation_based** - Lab observation questions
- **application** - Real-world application questions
- **reaction_analysis** - Analyzing chemical reactions

### Topics Covered:
- Chemical Reactions
- Chemical Equations
- Balancing Equations
- Types of Reactions (Combination, Decomposition, Displacement, Double Displacement)
- Energy in Reactions (Exothermic, Endothermic)
- Oxidation and Reduction
- Corrosion and Rancidity

### Difficulty Levels:
- Easy: 8 questions
- Medium: 18 questions
- Hard: 4 questions

## 🔧 Evaluation Metrics Implemented

### 1. **chemistry_answer_metric** (Recommended)
Comprehensive metric that:
- Checks for exact matches (score: 1.0)
- Calculates word overlap between prediction and gold answer
- Awards bonus points for key chemistry concepts
- Returns score between 0.0 and 1.0

### 2. **f1_score_metric**
Standard F1 score based on word overlap:
- Calculates precision and recall
- Returns harmonic mean

### 3. **exact_match_metric**
Binary metric:
- Returns 1.0 for exact match
- Returns 0.0 otherwise

## 🚀 Usage

### Running Evaluation

```bash
# Run the test evaluation script
python test_evaluation.py
```

### Using in Your Code

```python
from chat.dspy_logic import (
    load_chemistry_eval_dataset,
    evaluate_chemistry_qa,
    get_chemistry_response,
    ChemistryQAModule
)

# Load dataset
examples = load_chemistry_eval_dataset()

# Get a chemistry answer
answer = get_chemistry_response("What is a balanced chemical equation?")
print(answer)

# Run evaluation
score = evaluate_chemistry_qa(devset=examples[:10])
print(f"Score: {score:.2%}")
```

### Integrating with Django Views

```python
# In your views.py
from .dspy_logic import get_chemistry_response

def chat_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')

        # Use chemistry-specific response for chemistry questions
        if is_chemistry_question(user_message):
            response = get_chemistry_response(user_message)
        else:
            response = get_chatbot_response(user_message)

        # ... rest of your code
```

## 📈 Optimization with DSPy

You can optimize your model using DSPy's optimization tools:

```python
import dspy
from chat.dspy_logic import (
    ChemistryQAModule,
    load_chemistry_eval_dataset,
    chemistry_answer_metric
)

# Load data
examples = load_chemistry_eval_dataset()
trainset = examples[:18]  # 60%
devset = examples[18:24]  # 20%

# Initialize optimizer
optimizer = dspy.BootstrapFewShot(
    metric=chemistry_answer_metric,
    max_bootstrapped_demos=4,
    max_labeled_demos=4
)

# Compile the program
chemistry_qa = ChemistryQAModule()
compiled_qa = optimizer.compile(
    chemistry_qa,
    trainset=trainset,
    valset=devset
)

# Save the optimized model
compiled_qa.save('optimized_chemistry_qa.json')
```

## 📝 Example Questions in Dataset

1. Why should a magnesium ribbon be cleaned before burning in air?
2. What is a balanced chemical equation?
3. Balance the equation: Fe + H2O → Fe3O4 + H2
4. What is the difference between exothermic and endothermic reactions?
5. Why does copper sulphate solution change color when iron nail is dipped?
6. What is corrosion? Give examples.
7. Why are chips bags flushed with nitrogen?

... and 23 more questions!

## 🎯 Metrics Interpretation

### Chemistry Answer Metric Scores:
- **1.0** - Perfect match or all key concepts present
- **0.7-0.9** - Good answer with most key terms
- **0.5-0.7** - Partial answer with some key concepts
- **< 0.5** - Incomplete or incorrect answer

## 🔄 Next Steps

1. **Run Initial Evaluation**
   ```bash
   python test_evaluation.py
   ```

2. **Optimize the Model**
   - Use BootstrapFewShot or other DSPy optimizers
   - Fine-tune on the training set
   - Validate on dev set

3. **Test on Hold-out Set**
   - Evaluate final model on test set
   - Compare with baseline

4. **Deploy**
   - Integrate optimized model into Django views
   - Monitor performance in production

## 📦 Dataset Format

```json
{
  "id": 1,
  "type": "short_answer",
  "question": "Question text here?",
  "answer": "Expected answer here",
  "topic": "Topic name",
  "difficulty": "easy|medium|hard",
  "options": ["opt1", "opt2"],  // For MCQs only
  "explanation": "Explanation"  // For MCQs only
}
```

## 🐛 Troubleshooting

**Issue**: Dataset not found
- Ensure `chemistry_eval_dataset.json` is in the project root directory
- Check the path in `load_chemistry_eval_dataset()` function

**Issue**: Evaluation running slowly
- Reduce `num_threads` in evaluator
- Use a smaller subset for testing

**Issue**: Low scores
- The baseline model may need optimization
- Try using DSPy optimizers like BootstrapFewShot
- Add few-shot examples to prompts

## 📚 References

- [DSPy Documentation](https://dspy-docs.vercel.app/)
- [DSPy GitHub](https://github.com/stanfordnlp/dspy)
- NCERT Class 10 Science Chapter 1: Chemical Reactions and Equations
