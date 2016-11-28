# -*- coding: utf-8 -*-
"""
Configuration for the simulations, for the multi-players case.
"""
from __future__ import print_function

__author__ = "Lilian Besson"
__version__ = "0.2"

# Import arms
from Arms.Bernoulli import Bernoulli
# from Arms.Exponential import Exponential
# from Arms.Gaussian import Gaussian
# from Arms.Poisson import Poisson

# Import contained classes
from Environment.MAB import MAB
# Import algorithms, both single-player and multi-player
from Policies import *
from PoliciesMultiPlayers import *
# Collision Models
from Environment.CollisionModels import *


# HORIZON : number of time steps of the experiments
# XXX Should be >= 10000 to be interesting "asymptotically"
HORIZON = 20000
HORIZON = 2000
HORIZON = 500
HORIZON = 1000
HORIZON = 3000
HORIZON = 10000
# HORIZON = 40000

# REPETITIONS : number of repetitions of the experiments
# XXX Should be >= 10 to be stastically trustworthy
REPETITIONS = 1  # XXX To profile the code, turn down parallel computing
REPETITIONS = 4  # Nb of cores, to have exactly one repetition process by cores
REPETITIONS = 50
REPETITIONS = 200
# REPETITIONS = 20
# REPETITIONS = 8
REPETITIONS = 1  # XXX To profile the code, turn down parallel computing

DO_PARALLEL = False  # XXX do not let this = False  # To profile the code, turn down parallel computing
DO_PARALLEL = True
DO_PARALLEL = (REPETITIONS > 1) and DO_PARALLEL
N_JOBS = -1 if DO_PARALLEL else 1

# Parameters for the epsilon-greedy and epsilon-... policies
EPSILON = 0.1
# Temperature for the softmax
TEMPERATURE = 0.005
# Parameters for the Aggr policy
LEARNING_RATE = 0.01
LEARNING_RATES = [LEARNING_RATE]
DECREASE_RATE = HORIZON / 2.0
DECREASE_RATE = None
TEST_AGGR = True
TEST_AGGR = False

# NB_PLAYERS : number of player, for policies who need it ?
NB_PLAYERS = 6    # Less that the number of arms
# NB_PLAYERS = 13    # Less that the number of arms
# NB_PLAYERS = 17   # Just the number of arms
# NB_PLAYERS = 25   # More than the number of arms !!

# Collision model
collisionModel = rewardIsSharedUniformly
collisionModel = noCollision
collisionModel = onlyUniqUserGetsReward

# distances = np.random.random_sample(NB_PLAYERS)
# print("Each player is at the base station with a certain distance (the lower, the more chance it has to be selected)")
# for i in range(NB_PLAYERS):
#     print("  - Player nb {}\tis at distance {} ...".format(i + 1, distances[i]))
# def closerOneGetsReward(*args): return closerUserGetsReward(*args, distances=distances)
# collisionModel = closerOneGetsReward


# Test one the multi-players policy
TEST_MULTIPLAYER_POLICY = False
TEST_MULTIPLAYER_POLICY = True


# XXX This dictionary configures the experiments
configuration = {
    # --- Duration of the experiment
    "horizon": HORIZON,
    # --- Number of repetition of the experiment (to have an average)
    "repetitions": REPETITIONS,
    # --- Parameters for the use of joblib.Parallel
    "n_jobs": N_JOBS,    # = nb of CPU cores
    "verbosity": 6,  # Max joblib verbosity
    # --- Collision model
    "collisionModel": collisionModel,
    # --- Other parameters for the Evaluator
    "finalRanksOnAverage": True,  # Use an average instead of the last value for the final ranking of the tested players
    "averageOn": 1e-3,  # Average the final rank on the 1.0% last time steps
    # --- Arms
    "environment": [
        # {   # A very very easy problem: 3 arms, one bad, one average, one good
        #     "arm_type": Bernoulli,
        #     "params": [0.1, 0.5, 0.9]
        # },
        # {   # A very easy problem (9 arms), but it is used in a lot of articles
        #     "arm_type": Bernoulli,
        #     "params": [t / 10.0 for t in range(1, 10)]
        # },
        # {   # An easy problem (14 arms)
        #     "arm_type": Bernoulli,
        #     "params": [round(t / 15.0, 2) for t in range(1, 15)]
        # },
        # {   # An easy problem (19 arms)
        #     "arm_type": Bernoulli,
        #     "params": [t / 20.0 for t in range(1, 20)]
        # },
        {   # An other problem (17 arms), best arm = last, with three groups: very bad arms (0.01, 0.02), middle arms (0.3, 0.6) and very good arms (0.78, 0.85)
            "arm_type": Bernoulli,
            "params": [0.005, 0.01, 0.015, 0.02, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.78, 0.8, 0.82, 0.83, 0.84, 0.85]
        },
    ],
    # DONE I tried with other arms distribution: Exponential, it works similarly
    # "environment": [  # Exponential arms
    #     {   # An example problem with  arms
    #         "arm_type": Exponential,
    #         # "params": [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1)]
    #         "params": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    #     },
    # ],
    # DONE I tried with other arms distribution: Gaussian, it works similarly
    # FIXME Bayesian policies based on a Beta posterior (Thompson, BayesUCB) do not work - yet - for continuous reward in [0, 1] but only for Boolean reward in {0, 1} (ie Bernoulli).
    # "environment": [  # Gaussian arms
    #     {   # An example problem with  arms
    #         "arm_type": Gaussian,
    #         "params": [(0.1, 0.5), (0.2, 0.5), (0.3, 0.5), (0.4, 0.5), (0.5, 0.5), (0.6, 0.5), (0.7, 0.5), (0.8, 0.5), (0.9, 0.5)]
    #     },
    # ],
    # --- Defining each player manually
    # "players": [
    #     # --- Stupid algorithm
    #     {
    #         "archtype": Uniform,   # The stupidest policy
    #         "params": {
    #         }
    #     },
    #     # # --- Static or perfect (toy) algorithm
    #     # {
    #     #     "archtype": TakeFixedArm,   # The static policy: always selects one arm
    #     #     "params": {
    #     #         "armIndex": 16
    #     #     }
    #     # },
    #     # --- Take randomly one arm from a fixed set
    #     # {
    #     #     "archtype": UniformOnSome,
    #     #     "params": {
    #     #         "armIndexes": [0, 16]
    #     #     }
    #     # },
    #     {
    #         "archtype": UniformOnSome,
    #         "params": {  # Example: one of the best arms
    #             "armIndexes": [13, 14, 15, 16]
    #         }
    #     },
    #     {
    #         "archtype": UniformOnSome,
    #         "params": {
    #             "armIndexes": [6, 7, 8, 9]
    #         }
    #     },
    #     {
    #         "archtype": UniformOnSome,
    #         "params": {
    #             "armIndexes": [0, 1, 15, 16]
    #         }
    #     },
    #     {
    #         "archtype": UniformOnSome,
    #         "params": {  # Example: one of the worse arms
    #             "armIndexes": [0, 1, 2, 3]
    #         }
    #     },
    #     # # --- Epsilon-... algorithms
    #     # {
    #     #     "archtype": EpsilonGreedy,   # This basic EpsilonGreedy is very bad
    #     #     "params": {
    #     #         "epsilon": EPSILON
    #     #     }
    #     # },
    #     # {
    #     #     "archtype": EpsilonDecreasing,   # This basic EpsilonGreedy is also very bad
    #     #     "params": {
    #     #         "epsilon": EPSILON,
    #     #         "decreasingRate": 0.005,
    #     #     }
    #     # },
    #     # {
    #     #     "archtype": EpsilonFirst,   # This basic EpsilonFirst is also very bad
    #     #     "params": {
    #     #         "epsilon": EPSILON,
    #     #         "horizon": HORIZON
    #     #     }
    #     # },
    #     # # --- UCB algorithms
    #     # {
    #     #     "archtype": UCB,   # This basic UCB is very worse than the other
    #     #     "params": {}
    #     # },
    #     # {
    #     #     "archtype": UCBV,   # UCB with variance term
    #     #     "params": {}
    #     # },
    #     # # # --- Softmax algorithms
    #     # {
    #     #     "archtype": Softmax,   # This basic Softmax is very bad
    #     #     "params": {
    #     #         "temperature": TEMPERATURE
    #     #     }
    #     # },
    #     # # --- Thompson algorithms
    #     # {
    #     #     "archtype": Thompson,
    #     #     "params": {}
    #     # },
    #     # # --- KL algorithms
    #     # {
    #     #     "archtype": klUCB,
    #     #     "params": {}
    #     # },
    #     # {
    #     #     "archtype": BayesUCB,
    #     #     "params": {}
    #     # },
    #     # # --- AdBandit with different alpha parameters
    #     # {
    #     #     "archtype": AdBandit,
    #     #     "params": {
    #     #         "alpha": 0.5,
    #     #         "horizon": HORIZON
    #     #     }
    #     # },
    #     # # {
    #     # #     "archtype": AdBandit,
    #     # #     "params": {
    #     # #         "alpha": 0.125,
    #     # #         "horizon": HORIZON
    #     # #     }
    #     # # },
    # ],
    # --- Using the same type of player for all players:
    # "players": [
    #     {
    #         "archtype": TakeRandomFixedArm,
    #         "params": {}
    #     }
    #     for _ in range(NB_PLAYERS)
    # ],
}


# Dynamic hack to force the Aggr (player aggregator) to use all the player previously/already defined
if TEST_AGGR:
    non_aggr_players = configuration["players"]
    for learning_rate in LEARNING_RATES:
        current_players = configuration["players"]
        # Add one Aggr policy
        configuration["players"] = current_players + [{
            "archtype": Aggr,
            "params": {
                "learningRate": learning_rate,
                "decreaseRate": DECREASE_RATE,
                "children": non_aggr_players
            },
        }]


if TEST_MULTIPLAYER_POLICY:
    nbArms = len(configuration['environment'][0]['params'])
    if len(configuration['environment']) > 1:
        raise ValueError("WARNING do not use this hack if you try to use more than one environment.")
    configuration.update({
        # # --- Defining manually each child
        # "players": [TakeFixedArm(nbArms, 16) for _ in range(NB_PLAYERS)]
        # "players": [TakeRandomFixedArm(nbArms) for _ in range(NB_PLAYERS)]
        # --- Defining each player as one child of a multi-player policy
        # # --- Using multi-player Selfish policy
        # "players": Selfish(NB_PLAYERS, Uniform, nbArms).childs
        # "players": Selfish(NB_PLAYERS, TakeRandomFixedArm, nbArms).childs
        # "players": Selfish(NB_PLAYERS, UCB, nbArms).childs
        "players": Selfish(NB_PLAYERS, Thompson, nbArms).childs
        # "players": Selfish(NB_PLAYERS, klUCB, nbArms).childs
        # "players": Selfish(NB_PLAYERS, BayesUCB, nbArms).childs
        # "players": Selfish(NB_PLAYERS, Softmax, nbArms, temperature=TEMPERATURE).childs
        # --- Using multi-player Centralized policy
        # "players": CentralizedNotFair(NB_PLAYERS, nbArms).childs
        # "players": CentralizedFair(NB_PLAYERS, nbArms).childs
        # --- Using multi-player Oracle policy
        # XXX they need a perfect knowledge on the arms, even this is not physically plausible
        # "players": OracleNotFair(NB_PLAYERS, MAB(configuration['environment'][0])).childs
        # "players": OracleFair(NB_PLAYERS, MAB(configuration['environment'][0])).childs
    })
# FIXME the EvaluatorMultiPlayers should regenerate the list of players in every repetitions, to have at the end results on the average behavior of these randomized multi-players policies

print("Loaded experiments configuration from 'configuration.py' :")
print("configuration =", configuration)  # DEBUG
