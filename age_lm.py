import rpy2.robjects as robjects

r = robjects.r

import agemodel


def GetAgeWeightFirst(table):
    """Get sequences of mother's age, birth weight, and first baby flag.

    Args:
        table: Table object

    Returns:
        tuple of sequences (ages, weights, first_bool)
    """
    ages = []
    weights = []
    first_bool = []
    for r in table.records:
        if 'NA' in [r.agepreg, r.totalwgt_oz, r.birthord]:
            continue

        # first is 1.0 for first babies; 0.0 for others
        if r.birthord == 1:
            first = 1.0
        else:
            first = 0.0

        ages.append(r.agepreg)
        weights.append(r.totalwgt_oz)
        first_bool.append(first)

    return ages, weights, first_bool


def RunModel(model, print_flag=True):
    """Submits model to r.lm and returns the result."""
    model = r(model)
    res = r.lm(model)
    if print_flag:
        PrintSummary(res)
    return res


def PrintSummary(res):
    """Prints results from r.lm (just the parts we want)."""
    flag = False
    lines = r.summary(res)
    lines = str(lines)

    for line in lines.split('\n'):
        # skip everything until we get to coefficients
        if line.startswith('Coefficients'):
            flag = True
        if flag:
            print
            line
    print


def main(script, model_number=0):
    model_number = int(model_number)

    # get the data
    pool, firsts, others = agemodel.MakeTables()
    ages, weights, first_bool = GetAgeWeightFirst(pool)
    ages2 = [age ** 2 for age in ages]

    # put the data into the R environment
    robjects.globalEnv['weights'] = robjects.FloatVector(weights)
    robjects.globalEnv['ages'] = robjects.FloatVector(ages)
    robjects.globalEnv['ages2'] = robjects.FloatVector(ages2)
    robjects.globalEnv['first'] = robjects.FloatVector(first_bool)

    # run the models
    models = ['weights ~ first',
              'weights ~ ages',
              'weights ~ first + ages',
              'weights ~ ages + ages2',
              'weights ~ first + ages + ages2']

    model = models[model_number]
    print
    model
    RunModel(model)


if __name__ == '__main__':
    import sys

    main(*sys.argv)
