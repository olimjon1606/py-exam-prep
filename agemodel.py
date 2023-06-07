def Process(table, name):
    """Runs various analyses on this table.

    Creates instance variables:
        ages: sequence of int ages in years
        age_pmf: Pmf object
        age_cdf: Cdf object
        weights: sequence of total weight in ounces
        weight_cdf: Cdf object
    """
    cumulative.Process(table, name)

    table.ages = [p.agepreg for p in table.records
                  if p.agepreg != 'NA']
    table.age_pmf = Pmf.MakePmfFromList(table.ages, table.name)
    table.age_cdf = Cdf.MakeCdfFromList(table.ages, table.name)

    table.weights = [p.totalwgt_oz for p in table.records
                     if p.totalwgt_oz != 'NA']
    table.weight_cdf = Cdf.MakeCdfFromList(table.weights, table.name)


def MakeTables(data_dir='.'):
    """Reads survey data and returns a tuple of Tables"""
    table, firsts, others = first.MakeTables(data_dir)
    pool = descriptive.PoolRecords(firsts, others)

    Process(pool, 'live births')
    Process(firsts, 'first babies')
    Process(others, 'others')

    return pool, firsts, others


def GetAgeWeight(table, low=0.0, high=20.0):
    """Get sequences of mother's age and birth weight.

    Args:
        table: Table object
        low: float min weight in pounds
        high: float max weight in pounds

    Returns:
        tuple of sequences (ages, weights)
    """
    ages = []
    weights = []
    for r in table.records:
        if r.agepreg == 'NA' or r.totalwgt_oz == 'NA':
            continue

        if r.totalwgt_oz < low * 16 or r.totalwgt_oz > high * 16:
            continue

        ages.append(r.agepreg)
        weights.append(r.totalwgt_oz)

    return ages, weights


def Partition(ages, weights, bin_size=2):
    """Break ages into bins.

    Returns a map from age to list of weights.
    """
    weight_dict = {}
    for age, weight in zip(ages, weights):
        bin = bin_size * math.floor(age / bin_size) + bin_size / 2.0
        weight_dict.setdefault(bin, []).append(weight)

    for bin, bin_weights in weight_dict.iteritems():
        try:
            mean = thinkstats.Mean(bin_weights)
        except ZeroDivisionError:
            continue

    return weight_dict


def MakeFigures(pool, firsts, others):
    """Creates several figures for the book."""

    # CDF of all ages
    myplot.Clf()
    myplot.Cdf(pool.age_cdf)
    myplot.Save(root='agemodel_age_cdf',
                title="Distribution of mother's age",
                xlabel='age (years)',
                ylabel='CDF',
                legend=False)

    # CDF of all weights
    myplot.Clf()
    myplot.Cdf(pool.weight_cdf)
    myplot.Save(root='agemodel_weight_cdf',
                title="Distribution of birth weight",
                xlabel='birth weight (oz)',
                ylabel='CDF',
                legend=False)

    # plot CDFs of birth ages for first babies and others
    myplot.Clf()
    myplot.Cdfs([firsts.age_cdf, others.age_cdf])
    myplot.Save(root='agemodel_age_cdfs',
                title="Distribution of mother's age",
                xlabel='age (years)',
                ylabel='CDF')

    myplot.Clf()
    myplot.Cdfs([firsts.weight_cdf, others.weight_cdf])
    myplot.Save(root='agemodel_weight_cdfs',
                title="Distribution of birth weight",
                xlabel='birth weight (oz)',
                ylabel='CDF')

    # make a scatterplot of ages and weights
    ages, weights = GetAgeWeight(pool)
    pyplot.clf()
    # pyplot.scatter(ages, weights, alpha=0.2)
    pyplot.hexbin(ages, weights, cmap=matplotlib.cm.gray_r)
    myplot.Save(root='agemodel_scatter',
                xlabel='Age (years)',
                ylabel='Birth weight (oz)',
                legend=False)


def DifferenceInMeans(firsts, others, attr):
    """Compute the difference in means between tables for a given attr.

    Prints summary statistics.
    """
    firsts_mean = thinkstats.Mean(getattr(firsts, attr))
    print
    'First babies, %s, trimmed mean:' % attr, firsts_mean

    others_mean = thinkstats.Mean(getattr(others, attr))
    print
    'Other babies, %s, trimmed mean:' % attr, others_mean

    diff = others_mean - firsts_mean
    print
    'Difference in means:', diff
    print

    return diff


def ComputeLeastSquares(ages, weights):
    """Computes least squares fit for ages and weights.

    Prints summary statistics.
    """
    # compute the correlation between age and weight
    print
    'Pearson correlation', correlation.Corr(ages, weights)
    print
    'Spearman correlation', correlation.SpearmanCorr(ages, weights)

    # compute least squares fit
    inter, slope = correlation.LeastSquares(ages, weights)
    print
    '(inter, slope):', inter, slope

    res = correlation.Residuals(ages, weights, inter, slope)
    R2 = correlation.CoefDetermination(weights, res)

    print
    'R^2', R2
    print
    return inter, slope, R2


def main(name, data_dir=''):
    pool, firsts, others = MakeTables(data_dir)

    for table in [pool, firsts, others]:
        print
        table.name, len(table.records),
        print
        len(table.ages), len(table.weights)

    # compute differences in mean age and weight
    age_diff = DifferenceInMeans(firsts, others, 'ages')
    weight_diff = DifferenceInMeans(firsts, others, 'weights')

    # get ages and weights
    ages, weights = GetAgeWeight(pool)

    # compute a least squares fit
    inter, slope, R2 = ComputeLeastSquares(ages, weights)

    # see how much of the weight difference is explained by age
    weight_diff_explained = age_diff * slope
    print
    'Weight difference explained by age:', weight_diff_explained
    print
    'Fraction explained:', weight_diff_explained / weight_diff
    print

    # make a table of mean weight for 5-year age bins
    weight_dict = Partition(ages, weights)
    MakeLinePlot(weight_dict)

    # the correlations are slightly higher if we trim outliers
    ages, weights = GetAgeWeight(pool, low=4, high=12)
    inter, slope, R2 = ComputeLeastSquares(ages, weights)

    MakeFigures(pool, firsts, others)


def MakeLinePlot(age_bins):
    xs = []
    ys = []
    for bin, weights in sorted(age_bins.iteritems()):
        xs.append(bin)
        ys.append(thinkstats.Mean(weights))

    myplot.Plot(xs, ys, 'bs-')
    myplot.Save(root='agemodel_line',
                xlabel="Mother's age (years)",
                ylabel='Mean birthweight (oz)',
                legend=False)


if __name__ == '__main__':
    import sys

    main(*sys.argv)
