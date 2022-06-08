#rewrite by Dr. Ardiansyah in April 2020 for student of Hydrology
#don't delete this first two lines

import scipy
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt

class Distribution(object):
    def __init__(self,dist_names_list = []):
        self.dist_names = ['norm','lognorm','pearson3', 'expon']
        self.dist_results = []
        self.params = {}
        self.pdf_fitteds = {}
        self.cdf_fitteds = {}
        
        self.DistributionName = ""
        self.PValue = 0
        self.Param = None
        self.isFitted = False
        #for plotting pdf we need x and 
        self.x = []        
        self.pdf_nod = 0
        
        
    def Fit(self, y):
        self.dist_results = []
        self.params = {}
        desc = scipy.stats.describe(y)
        nod = desc[0]
        minmax = desc[1]
        mean = desc[2]
        std = np.sqrt(desc[3])  
        cv  = std/mean    
        var = desc[3]
        skew = desc[4]
        kurt = desc[5]
        print ('Data description : ')
        print ('=======================================')
        print ('Number of Data    : ', nod)
        print ('Minimum - Maximum : ', minmax)
        print ('Mean              : ', mean)
        print ('Standar Deviation : ', std)
        print ('Variance          : ', var)
        print ('Coef.Variance (Cv): ', cv)
        print ('Coef.Skewness (Cs): ', skew)
        print ('Coef.Kurtosis (Ck): ', kurt)
        print ('=======================================')
        print ('')
        self.pdf_nod = 5 * nod
        self.x = np.linspace(min(y), max(y), self.pdf_nod) # x pdf (probability density function)

        print ('Distribution, its p value, and parameters :')
        print ('=======================================')
        for dist_name in self.dist_names:
            dist = getattr(scipy.stats, dist_name)
            param = dist.fit(y)
            pdf_fitted = dist.pdf(self.x, *param[:-2], loc=param[-2], scale=param[-1])
            cdf_fitted = dist.cdf(self.x, *param[:-2], loc=param[-2], scale=param[-1])
            self.params[dist_name] = param
            self.pdf_fitteds[dist_name] = pdf_fitted
            self.cdf_fitteds[dist_name] = cdf_fitted
            #Applying the Kolmogorov-Smirnov test
            D, p = scipy.stats.kstest(y, dist_name, args=param);
            self.dist_results.append((dist_name,p))
            print (dist_name, p, param)
        print ('=======================================')
        
        #select the best fitted distribution
        sel_dist,p = (max(self.dist_results,key=lambda item:item[1]))
        #store the name of the best fit and its p value
        self.DistributionName = sel_dist
        self.PValue = p

        print ('The best fit distribution is : ', self.DistributionName)
        print ('The best fit distribution p value is : ', self.PValue)
        
        self.isFitted = True
        return self.DistributionName,self.PValue
    
    def Random(self, n = 1):
        if self.isFitted:
            dist_name = self.DistributionName
            param = self.params[dist_name]
            #initiate the scipy distribution
            dist = getattr(scipy.stats, dist_name)
            return dist.rvs(*param[:-2], loc=param[-2], scale=param[-1], size=n)
        else:
            raise ValueError('Must first run the Fit method.')
            
    def Plot(self,y):
        plt.figure(1)
        #x = self.Random(n=len(y))
        #plt.hist(x, alpha=0.5, label='Fitted')
        #plt.hist(y, alpha=0.5, label='Actual')

        yhist, xhist, _ = plt.hist(y, alpha=0.5, label='Actual')
        pdf_scale = yhist.max() / np.amax(self.pdf_fitteds[self.DistributionName])
        pdf_fitted_scaled = self.pdf_fitteds[self.DistributionName] * pdf_scale
        plt.plot(self.x, pdf_fitted_scaled, 'r-', label=str(self.DistributionName)+'(Fitted)')
        color = ['b--', 'g--', 'k--']; color_index = 0
        for dist_name in self.dist_names:
            if (dist_name != self.DistributionName):
                pdf_scale = yhist.max() / np.amax(self.pdf_fitteds[dist_name])
                pdf_fitted_scaled = self.pdf_fitteds[dist_name] * pdf_scale
                plt.plot(self.x, pdf_fitted_scaled, color[color_index], label=dist_name)
                color_index = color_index + 1

        plt.legend(loc='upper right')
        plt.xlabel('Data')
        plt.ylabel('Frequency')
        plt.title('Best Fitted Distribution is '+ str(self.DistributionName))
        plt.savefig('Fitted Distribution.png')
        #plt.show()

    def normPlot(self, y):
        fig, ax = plt.subplots()
        # Calculate quantiles and least-square-fit curve
        fitted_dist_name = self.DistributionName
        fitted_dist = getattr(scipy.stats, fitted_dist_name)
        (quantiles, values), (slope, intercept, r) = scipy.stats.probplot(y, dist=fitted_dist_name,          
                                                                          sparams=self.params[fitted_dist_name])

        # Plot probability in quantile-quantile, later change x axis to probability and return period
        ax.plot(quantiles, values,'ob', label='Observed')
        ax.plot(quantiles, quantiles * slope + intercept, 'r', label='Theoretical')
        ax.legend(loc='lower center')
        ax.set_ylabel('Data')
        ax.set_title('Probability Plot : '+ str(self.DistributionName))

        #define ticks for new xaxis(es)
        ticks_perc=np.array([1, 5, 10, 20, 50, 80, 90, 95, 99]) #percentile, prob. non exeedance
        #transfrom them from precentile to cumulative density (cdf)
        param = self.params[self.DistributionName]
        #nilai data teoritis dari probability tick_perc (i/100) yang diminta (ppf --> percentile to cdf)
        #or quantiles of corresponding cdf in tick_perc
        ticks_quan=[fitted_dist.ppf(i/100., *param[:-2], loc=param[-2], scale=param[-1]) for i in ticks_perc] 
        #ticks_quan=np.array(ticks_quan)
        #transform to Probability of Exeedance tick
        ticks_Pex = (1. - (ticks_perc/100.))*100 #probability of exeedance
        ticks_Pex = np.around(ticks_Pex, decimals=1)
        #transform to Return Period tick
        ticks_RetP = 100./ticks_Pex
        ticks_RetP = np.around(ticks_RetP, decimals=1)

        #print in terminal
        #np.set_printoptions(precision=2)
        #print ticks_quan
        #print ticks_Pex
        #print ticks_RetP

        #assign new ticks
        ax.set_xticks(ticks_quan) #position in old axis
        ax.set_xticklabels(ticks_Pex) #label in new axis
        ax.xaxis.set_ticks_position('bottom') # set the position of the second x-axis to bottom
        ax.xaxis.set_label_position('bottom') # set the position of the second x-axis to bottom
        ax.spines['bottom'].set_position(('outward', 10))
        ax.set_xlabel('Probability of Exeedance (%)')
        ax.grid()
        plt.xticks(rotation=90)
        #plt.gca().invert_xaxis()

        # Set scond x-axis
        ax2 = ax.twiny()
        # Decide the ticklabel position in the new x-axis,
        ax2.set_xticks(ticks_quan) #position in old axis
        ax2.set_xticklabels(ticks_RetP) #label in new axis
        ax2.xaxis.set_ticks_position('bottom') # set the position of the second x-axis to bottom
        ax2.xaxis.set_label_position('bottom') # set the position of the second x-axis to bottom
        ax2.spines['bottom'].set_position(('outward', 60))
        ax2.set_xlabel('Return Period (years)')
        ax2.set_xlim(ax.get_xlim())
        plt.xticks(rotation=90)
        #plt.gca().invert_xaxis()

        plt.savefig('Probability Plot.png',bbox_inches='tight',dpi=100)
        plt.show()

