def Log(t):
    """Computes the log of a sequence."""
    return [math.log(x) for x in t]


def ComputeCorrelations():
    resp = brfss_scatter.Respondents()
    resp.ReadRecords()
    print
    'Number of records:', len(resp.records)

    heights, weights = resp.GetHeightWeight()
    pearson = correlation.Corr(heights, weights)
    print
    'Pearson correlation (weights):', pearson

    log_weights = Log(weights)
    pearson = correlation.Corr(heights, log_weights)
    print
    'Pearson correlation (log weights):', pearson

    spearman = correlation.SpearmanCorr(heights, weights)
    print
    'Spearman correlation (weights):', spearman

    inter, slope = correlation.LeastSquares(heights, log_weights)
    print
    'Least squares inter, slope (log weights):', inter, slope

    res = correlation.Residuals(heights, log_weights, inter, slope)
    R2 = correlation.CoefDetermination(log_weights, res)
    print
    'Coefficient of determination:', R2
    print
    'sqrt(R^2):', math.sqrt(R2)


def main(name):
    ComputeCorrelations()


if __name__ == '__main__':
    main(*sys.argv)
