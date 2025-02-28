import numpy as np
from scipy import stats
from scipy import integrate
from scipy import interpolate
from astropy.table import Table
from scipy.stats import rv_continuous
from astropy.io import ascii

# Create a function that returns the PDF of the axial ratio
# Empirical virgo-cluster dE distribution taken from
# Sanchez-Janssen 2016, ApJ 820, 69 doi:10.3847/0004-637X/820/1/69
# Normalize PDF via numerical integral (it was pretty close to normalized to begin with)
# While it's not necessary to add the _cdf routine, it speeds up the rvs draws by a huge factor
class AxialRatioPDF(rv_continuous):
    """
    The PDF of the axial ratio of dwarf-elliptical galaxies
    This is a subclass of scipy.stats.rv_continuous, so the rvs() method returns the
    random deviates and the pdf() method returns the probability of getting a certain axial ratio
    The empirical virgo-cluster dE distribution taken from
    Sanchez-Janssen 2016, ApJ 820, 69 doi:10.3847/0004-637X/820/1/69
    Normalize PDF via numerical integral (it was pretty close to normalized to begin with)
    While it's not necessary to add the _cdf routine, it speeds up the rvs draws by a huge factor
    """

    def __init__(self,**args):
        super(AxialRatioPDF,self).__init__(a=0.,b=1.,**args)
#        self.qdist = Table.read('data/sanchez-janssen_fig9.txt',format='ascii.commented_header')
        self.qdist = sanchez_jansen()
        self.normalization = integrate.trapz(self.qdist['pdf'],self.qdist['q'])
        self.qfunc = interpolate.interp1d(self.qdist['q'],self.qdist['pdf'],kind='linear')
        qsamples = np.arange(0,1.01,0.01)
        cdf_samples = np.array([integrate.quad(self._pdf,0,q)[0] for q in qsamples])
        self.cfunc = interpolate.interp1d(qsamples,cdf_samples)
    def _pdf(self,q):
        return self.qfunc(q)/self.normalization
    def _cdf(self,q):
        return self.cfunc(q)

def sanchez_jansen():
    """ Data from  Sanchez-Janssen 2016, ApJ 820, 69 doi:10.3847/0004-637X/820/1/69 """
    sj = """
    #q      pdf
    0.000   0.000
    0.0000001       0.001
    0.001   0.004
    0.150   0.010
    0.200   0.023
    0.262   0.056
    0.319   0.123
    0.362   0.253
    0.377   0.307
    0.400   0.340
    0.415   0.398
    0.432   0.511
    0.445   0.605
    0.462   0.710
    0.486   0.835
    0.543   1.137
    0.577   1.564
    0.600   1.837
    0.611   1.934
    0.623   1.957
    0.634   1.965
    0.645   1.994
    0.657   2.015
    0.665   2.006
    0.673   2.000
    0.679   2.011
    0.689   2.074
    0.698   2.155
    0.703   2.190
    0.710   2.219
    0.716   2.239
    0.723   2.227
    0.733   2.212
    0.740   2.210
    0.752   2.238
    0.761   2.295
    0.771   2.350
    0.778   2.359
    0.785   2.369
    0.794   2.352
    0.801   2.316
    0.809   2.263
    0.820   2.175
    0.838   2.039
    0.847   1.998
    0.866   1.952
    0.880   1.884
    0.892   1.844
    0.897   1.839
    0.906   1.850
    0.922   1.893
    0.933   1.919
    0.945   1.910
    0.954   1.858
    0.965   1.716
    0.972   1.579
    0.980   1.409
    0.992   1.179
    0.998   1.050
    0.9999999       0.50
    1.000   0.000
    """
    t = ascii.read(sj,format='commented_header')
    return t
