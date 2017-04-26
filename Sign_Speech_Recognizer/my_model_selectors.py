import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Baysian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        minimal_bic = float("inf")
        minimal_hmm_model = None
        try:
            for p in range(self.min_n_components, self.max_n_components + 1):

                # get HMM for p
                hmm_model = self.base_model(p)
                logL = hmm_model.score(self.X, self.lengths)
                number_of_parameters = p * (p + 2 * hmm_model.n_features) - 1
                bic = -2.0 * logL + number_of_parameters * np.log(len(self.X))
                # bic = -2.0 * logL + p * np.log(len(self.X))
                # print("p=",p,"bic=",bic)
                if minimal_bic > bic:
                    # print("  is minimal so far")
                    minimal_bic = bic
                    minimal_hmm_model = hmm_model
        except:
            pass

        if minimal_hmm_model is not None:
            return minimal_hmm_model
        else:
            return self.base_model(self.n_constant)


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    # """
    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        maximal_hmm_model = None
        maximal_dic = float("-inf")
        for p in range(self.min_n_components, self.max_n_components + 1):
            try:
                other_word_dics = []
                hmm_model = self.base_model(p)  # get HMM for p

                for hword in self.hwords:
                    if hword != self.this_word:
                        (hword_X, hword_lengths) = self.hwords[hword]
                        other_word_dics.append(hmm_model.score(hword_X, hword_lengths))
                mean_other_word_dic = np.mean(other_word_dics)
                dic = hmm_model.score(self.X, self.lengths) - mean_other_word_dic

                if maximal_dic < dic:
                    maximal_hmm_model = hmm_model
                    maximal_dic = dic
            except:
                pass

        if maximal_hmm_model is not None:
            return maximal_hmm_model
        else:
            return self.base_model(self.n_constant)
    # """


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        minimal_cv = float("inf")
        minimal_hmm_model = None
        try:
            for p in range(self.min_n_components, self.max_n_components + 1):

                # get HMM for p

                cross_validation_folding = KFold(n_splits=2)
                cv_eval = []

                # from sklearn doc
                for train_index, test_index in cross_validation_folding.split(self.sequences):
                    train_X, train_lengths = combine_sequences(train_index, self.sequences)
                    test_X, test_lengths = combine_sequences(test_index, self.sequences)

                    # need to replace selector's X & lengths to get HMM
                    self.X = train_X
                    self.lengths = train_lengths
                    hmm_model = self.base_model(p)

                    score = hmm_model.score(test_X, test_lengths)
                    cv_eval.append(score)

                cv = np.mean(cv_eval)
                # print("p=",p,"cv=",cv)

                if minimal_cv > cv:
                    # print("  is minimal so far")
                    minimal_cv = cv
                    minimal_hmm_model = hmm_model
        except:
            pass

        if minimal_hmm_model is not None:
            return minimal_hmm_model
        else:
            return self.base_model(self.n_constant)
