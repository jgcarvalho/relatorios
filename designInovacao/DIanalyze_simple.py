import fnmatch
import os
import math
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

freq_genes = [ [0,0,0,0] for i in range(13248)]
sum_genes = [ [0.0,0.0,0.0,0.0] for i in range(13248)]
mean_genes = [ [0.0,0.0,0.0,0.0] for i in range(13248)]
variance_genes = [ [0.0,0.0,0.0,0.0] for i in range(13248)]
mean_variance = 0.0
not_float = 0

n_pop = 0
pop_fitness = []
pop_fitness_mean = 0.0

f_output = open('./output_simple', 'w')
f_mean = open('./bb_means_simple', 'w')
f_variance = open('./bb_variance_simple', 'w')
f_fitness = open('./pop_fitness_simple', 'w')

samples =[]
for root, dirnames, filenames in os.walk('./'):
    for filename in fnmatch.filter(filenames, 'sample_*'):
        samples.append(os.path.join(root, filename))
# print samples

tmp =0
for s in samples:
    with open(s) as fp:
        for line in fp:
            genome = line.split(", ")[576:-1]
            fitness = line.split(", ")[-1]
            for i in range(len(genome)):
                try:
                    fit = float(fitness)
                    if i == 0:
                        n_pop +=1
                        pop_fitness.append(fit)
                    if genome[i] == '-':
                        freq_genes[i][0] += 1
                        sum_genes[i][0] += fit
                    elif genome[i] == '*':
                        freq_genes[i][1] += 1
                        sum_genes[i][1] += fit
                    elif genome[i] == '|':
                        freq_genes[i][2] += 1
                        sum_genes[i][2] += fit
                    elif genome[i] == '?':
                        freq_genes[i][3] += 1
                        sum_genes[i][3] += fit
                except ValueError:
                    not_float += 1
                    # print "Not a float", fitness
    tmp +=1
    if tmp == 9:
        break
            # break
    # print freq_genes
    # print sum_genes

#####################################################################################
# Calcula o fitness medio por BB
for i in range(len(freq_genes)):
    mean_genes[i][0] = sum_genes[i][0]/float(freq_genes[i][0])
    mean_genes[i][1] = sum_genes[i][1]/float(freq_genes[i][1])
    mean_genes[i][2] = sum_genes[i][2]/float(freq_genes[i][2])
    mean_genes[i][3] = sum_genes[i][3]/float(freq_genes[i][3])

for i in range(len(freq_genes)):
    f_mean.write("{}\t{}\t{}\t{}\t{}\n".format(i, mean_genes[i][0], mean_genes[i][1], mean_genes[i][2], mean_genes[i][3]))
    # print "{}\t{}\t{}\t{}\t{}".format(i, mean_genes[i][0], mean_genes[i][1], mean_genes[i][2], mean_genes[i][3])


###################################################################################
# Calcula as variancias media por BB
tmp=0
for s in samples:
    with open(s) as fp:
        for line in fp:
            genome = line.split(", ")[576:-1]
            fitness = line.split(", ")[-1]
            for i in range(len(genome)):
                try:
                    fit = float(fitness)
                    if genome[i] == '-':
                        variance_genes[i][0] += (mean_genes[i][0] - fit)**2
                    elif genome[i] == '*':
                        variance_genes[i][1] += (mean_genes[i][1] - fit)**2
                    elif genome[i] == '|':
                        variance_genes[i][2] += (mean_genes[i][2] - fit)**2
                    elif genome[i] == '?':
                        variance_genes[i][3] += (mean_genes[i][3] - fit)**2
                except ValueError:
                    not_float += 1
    tmp +=1
    if tmp == 9:
        break

n = 0
for i in range(len(freq_genes)):
    variance_genes[i][0] = variance_genes[i][0]/float(freq_genes[i][0])
    variance_genes[i][1] = variance_genes[i][1]/float(freq_genes[i][1])
    variance_genes[i][2] = variance_genes[i][2]/float(freq_genes[i][2])
    variance_genes[i][3] = variance_genes[i][3]/float(freq_genes[i][3])
    mean_variance += variance_genes[i][0]
    mean_variance += variance_genes[i][1]
    mean_variance += variance_genes[i][2]
    mean_variance += variance_genes[i][3]
    n += 4

# Variancia media da populacao
mean_variance = mean_variance/float(n)

for i in range(len(freq_genes)):
    f_variance.write("{}\t{}\t{}\t{}\t{}\n".format(i, variance_genes[i][0], variance_genes[i][1], variance_genes[i][2], variance_genes[i][3]))



#################################################################################
# OUTPUT
tmp_v = np.array(pop_fitness)
f_output.write("Numero de BBs = {}\n".format(len(freq_genes)))
f_output.write("Variancia media dos BBs = {}\n".format(mean_variance))
f_output.write("Desvio padrao medio BBs = {}\n".format(math.sqrt(mean_variance)))
f_output.write("Fitness medio da populacao = {}\n".format(np.mean(tmp_v, axis=0)))
f_output.write("Variancia do Fitness medio da populacao = {}\n".format(np.var(tmp_v, axis=0)))
f_output.write("Desvio padra do Fitness medio da populacao = {}\n".format(np.std(tmp_v, axis=0)))

#################################################################################
# FITNESS
for fit in pop_fitness:
    f_fitness.write("{} ".format(fit))

# #################################################################################
# # PLOT
# # example data
# mu = pop_fitness_mean # mean of distribution
# # sigma medio dos build blocks
# sigma = math.sqrt(mean_variance) # standard deviation of distribution
# x = mu + sigma * np.random.randn(10000)
#
# num_bins = 50
# # the histogram of the data
# n, bins, patches = plt.hist(np.array(pop_fitness), num_bins, normed=1, facecolor='blue', alpha=0.5)
# # add a 'best fit' line
# y = mlab.normpdf(bins, mu, sigma)
# plt.plot(bins, y, 'r--')
# plt.xlabel('Fitness')
# plt.ylabel('Probability')
# # plt.title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')
# plt.title(r'Histogram: $\mu={}$, $\sigma={}$'.format(mu, sigma))
#
# # Tweak spacing to prevent clipping of ylabel
# plt.subplots_adjust(left=0.15)
# plt.show()
