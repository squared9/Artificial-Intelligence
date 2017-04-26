import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

    :param models: dict of trained models
        {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
    :param test_set: SinglesData object
    :return: (list, list)  as probabilities, guesses
        both lists are ordered by the test set word_id
        probabilities is a list of dictionaries where each key a word and value is Log Liklihood
            [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
             {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
             ]
        guesses is a list of the best guess words ordered by the test set word_id
            ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
    """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    probabilities = []
    guesses = []

    X_lengths = test_set.get_all_Xlengths()

    for test_word in X_lengths:
        (X, lengths) = X_lengths[test_word]
        maximal_score = float("-inf")
        maximal_guess = ""

        word_log_likelihood = {}

        for training_word in models:
            word_log_likelihood[training_word] = float("inf")
            try:
                hmm_model = models[training_word]
                score = hmm_model.score(X, lengths)
                word_log_likelihood[training_word] = score

                if score > maximal_score:
                    maximal_score = score
                    maximal_guess = training_word
            except Exception as e:
                pass

        probabilities.append(word_log_likelihood)
        guesses.append(maximal_guess)

    return probabilities, guesses
