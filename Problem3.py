import numpy as np
import scr.StatisticalClasses as Stat

class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin
        self.n_of_flips = 20
        self._countLoss = 0

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100 * self._countWins - 250


    def get_loss_count(self):
        if self.get_reward() < 0:
            self._countLoss = 1

        return self._countLoss


class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = []  # create an empty list where rewards will be stored
        self._lossProb = []

        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())
            self._lossProb.append(game.get_loss_count())

        self._sumStat_GameRewards = Stat.SummaryStat('Game Rewards', self._gameRewards)
        self._sumStat_LossProb = Stat.SummaryStat('Probability of Loss', self._lossProb)

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return self._sumStat_GameRewards.get_mean()

    def get_CI_GameRewards(self, alpha):
        return self._sumStat_GameRewards.get_t_CI(alpha)


    def get_PI_GameRewards(self, alpha):
        return self._sumStat_GameRewards.get_PI(alpha)



Casino = SetOfGames(prob_head=0.5, n_games=1000)

Gambler = SetOfGames(prob_head=0.5, n_games=10)

print('*******************************************************************************************************************'
      '     Since the casino owner gets to play this game many times, we can apply the Law of Large Numbers '
      'and use a steady-state simulation to obtain the mean expected reward and confidence interval. '
      'On the other hand, the gambler plays this game 10 times only; in this case, the number of games are too small to '
      'apply the Law of Large Numbers. Hence, a transient-state simulation is used to obtain the mean expected reward '
      'and prediction interval.  '

      '*******************************************************************************************************************')

print('Expected reward for CASINO OWNER when the probability of head is 0.5:', Casino.get_ave_reward())

print("95% t-based CONFIDENCE interval for expected CASINO OWNER's game reward:", Casino.get_CI_GameRewards(0.05))

print('We would expect the confidence interval to cover the true mean expected reward for the casino owner 95% of times, '
              'when the game is played many times.')

print('Expected reward for GAMBLER when the probability of head is 0.5:', Gambler.get_ave_reward())

print("95% PREDICTION interval for expected GAMBLER's game reward:", Gambler.get_PI_GameRewards(0.05))

print("There is 95% probability that the GAMBLER's game reward will lie between the prediction intervals for the next game played.")


