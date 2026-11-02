import re
from collections import defaultdict, Counter

FINANCIAL_ADVISORY_CORPUS = """
Personal financial management requires disciplined budgeting and regular savings.
Budgeting ensures that monthly expenses do not exceed total income.
Emergency fund is essential to protect against unexpected medical expenses and job loss.
Save at least three to six months of living expenses in an emergency fund.
High interest debt should be cleared before making risky speculative investments.
Reduce discretionary spending when monthly expenses exceed eighty percent of income.
Discretionary spending includes dining out shopping and entertainment activities.
Systematic investment plans help grow wealth through compounding interest over time.
Diversified index funds offer balanced long term wealth accumulation with moderate risk.
Continuous financial improvement requires comparing spending patterns across months.
Review monthly budget limits to avoid unexpected deficits and maintain financial discipline.
Tracking daily transactions helps identify unnecessary subscription fees and recurring leaks.
Allocate fifty percent of income to essential needs thirty percent to wants and twenty percent to savings.
Compound interest is the eighth wonder of the financial world.
Maintain financial discipline to reach early financial independence and peace of mind.
"""

class FinancialLanguageModels:
    def __init__(self, corpus=FINANCIAL_ADVISORY_CORPUS):
        self.raw_corpus = corpus
        self.words = self._preprocess(corpus)
        self.vocabulary = sorted(list(set(self.words)))
        self.bigram_model = defaultdict(Counter)
        self.trigram_model = defaultdict(Counter)
        self._build_models()

    def _preprocess(self, text):
        clean_text = text.lower()
        clean_text = re.sub(r'[^a-zA-Z\s]', '', clean_text)
        return clean_text.split()

    def _build_models(self):
        for i in range(len(self.words) - 1):
            w1 = self.words[i]
            w2 = self.words[i + 1]
            self.bigram_model[w1][w2] += 1

        for i in range(len(self.words) - 2):
            w1 = self.words[i]
            w2 = self.words[i + 1]
            w3 = self.words[i + 2]
            self.trigram_model[(w1, w2)][w3] += 1

    def ulm_predict_next_word(self, word):
        w = word.strip().lower()
        if w not in self.bigram_model:
            return None, "No prediction available"
        top_prediction = self.bigram_model[w].most_common(1)[0]
        total_occurrences = sum(self.bigram_model[w].values())
        prob = top_prediction[1] / total_occurrences
        return top_prediction[0], round(prob, 3)

    def ulm_generate_text(self, start_word, length=8):
        current = start_word.strip().lower()
        sequence = [current]
        for _ in range(length - 1):
            if current not in self.bigram_model:
                break
            next_w = self.bigram_model[current].most_common(1)[0][0]
            sequence.append(next_w)
            current = next_w
        return " ".join(sequence)

    def slm_predict_next_word(self, word1, word2):
        ctx = (word1.strip().lower(), word2.strip().lower())
        if ctx not in self.trigram_model:
            fallback_word, _ = self.ulm_predict_next_word(word2)
            if fallback_word:
                return fallback_word, "Fallback"
            return None, "No prediction available"
        top_prediction = self.trigram_model[ctx].most_common(1)[0]
        total_occurrences = sum(self.trigram_model[ctx].values())
        prob = top_prediction[1] / total_occurrences
        return top_prediction[0], round(prob, 3)

    def slm_generate_text(self, word1, word2, length=12):
        w1 = word1.strip().lower()
        w2 = word2.strip().lower()
        sequence = [w1, w2]
        for _ in range(length - 2):
            ctx = (sequence[-2], sequence[-1])
            if ctx not in self.trigram_model:
                if sequence[-1] in self.bigram_model:
                    next_w = self.bigram_model[sequence[-1]].most_common(1)[0][0]
                else:
                    break
            else:
                next_w = self.trigram_model[ctx].most_common(1)[0][0]
            sequence.append(next_w)
        return " ".join(sequence)


def run_experiment_10():
    lm = FinancialLanguageModels()
    pred, prob = lm.ulm_predict_next_word("emergency")
    gen = lm.slm_generate_text("emergency", "fund", length=8)
    return {"prediction": pred, "generated": gen}

if __name__ == "__main__":
    res = run_experiment_10()
    print("Prediction:", res["prediction"])
