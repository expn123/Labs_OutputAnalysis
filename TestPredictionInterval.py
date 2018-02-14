import numpy as np
import matplotlib.pyplot as plt
import Parameters as Params
import SurvivalModelClasses as Cls

nSimCohorts = []    # number of simulated cohorts used to make predictions
# will be populated with [2^2, 2^3, 2^4, ... , 2^13 = 8,192]
for i in range(2, 13):
    nSimCohorts.append(pow(2, i))

# create the figure
fig = plt.figure('Prediction Intervals')
plt.title('95% Prediction Intervals')
plt.xlim([max(1/Params.MORTALITY_PROB - 5, 0), 1/Params.MORTALITY_PROB + 5])   # range of x-axis
plt.ylim([nSimCohorts[0]/2, nSimCohorts[-1]*2])     # range of y-axis

# calculate prediction intervals for different number of simulated cohorts
for n in nSimCohorts:

    multiCohort = Cls.MultiCohort(
        ids=range(n),
        pop_sizes=[Params.REAL_POP_SIZE] * n,
        mortality_probs=[Params.MORTALITY_PROB]*n)

    multiCohort.simulate(Params.TIME_STEPS)

    mean = multiCohort.get_overall_mean_survival()
    PI = multiCohort.get_PI_mean_survival(Params.ALPHA)

    # find the coordinates of the estimated mean and confidence intervals
    mean_x = mean   # mean of mean survival times
    mean_y = n   # population size
    PI_xs = np.linspace(PI[0], PI[1], 2)  # [lower upper] of the prediction interval
    PI_ys = mean_y * np.ones(2)  # [popSize popSize]

    plt.semilogy(mean_x, mean_y, 'ko', basey=2)  # draw the estimated mean (in log scale)
    plt.semilogy(PI_xs, PI_ys, 'k', basey=2)     # draw the confidence interval (in log scale)

# labels
plt.ylabel('Number of simulated cohorts')
plt.xlabel('Survival time' + ' (true mean = ' + str(1/Params.MORTALITY_PROB) + ')')
plt.show()
