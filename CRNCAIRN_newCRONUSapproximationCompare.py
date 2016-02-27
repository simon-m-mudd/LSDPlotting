# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 13:44:32 2016

@author: smudd
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 06:38:37 2015

@author: smudd
"""

    
import numpy as np
import CRNResults as CRNR
import LSDOSystemTools as LSDost
from glob import glob
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec
        #from scipy.stats import gaussian_kde



def CollatenewCRONUScomparisonCRNData():
    
    Directory = "C://basin_data//CosmoPaper//Results//Compiled//"
    #Directory = "T://Papers_LaTeX//crn_basinwide_paper//Compiled_results//"
    Dirname = LSDost.ReformatSeperators(Directory)
    Dirname = LSDost.AppendSepToDirectoryPath(Dirname)
    
    Fileformat = 'svg'
    
    # This list will store the crn data
    CRNDataList = []  
    CRNprefixes = []
    PaperNames = []
    ScalingNames = []
    
    label_size = 8
    axis_size = 12

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = label_size
    rcParams['xtick.major.size'] = 4    
    rcParams['ytick.major.size'] = 4
    rcParams['legend.fontsize'] = label_size
    rcParams['legend.handletextpad'] = 0.05
    rcParams['legend.labelspacing'] =0.1
    rcParams['legend.columnspacing'] =0.1

    SiteDicts = []   
       
    # loop through the directory, getting the results from the data    
    for fname in glob(Dirname+"*_CRNResults.csv"):
  
        # this will hold the lists of data
        thisdict = {}
        
        # get only the file without the data directory
        NoDirFname = LSDost.GetFileNameNoPath(fname)
        
        # Now get the prefix of the file
        splitfname = NoDirFname.split('_CRNResults.csv')
        fprefix = splitfname[0]
        
        # now produce the cronus name from this prefix
        CRONUS_name = Dirname+fprefix+"_CRONUS.csv"
        
        print "File prefix is: " + fprefix 
        print "Cronus_name is: " + CRONUS_name
        
        # now read in the data
        thisCRNData = CRNR.CRNResults(fname)        

        # read in the Cronus data and get the errors
        thisCRNData.ReadCRONUSData(CRONUS_name)
        thisCRNData.GetErrorsBetweenMethods()
        thisCRNData.GetErrorsBetweenCRONUS()
        
        CRNDataList.append(thisCRNData)
        CRNprefixes.append(fprefix)
        
        # now get the prefixes
        if fprefix == "Dethier":
            PaperNames.append("Dethier et al., 2014")
        elif fprefix == "Palumbo":
            PaperNames.append("Palumbo et al., 2010")
            
        # now get lists based on this data and place into a dictionary
        if "newCRONUS" in fname:
            ScalingNames.append("newCronus") 
        else:
            ScalingNames.append("Braucher")                  
        

    # now get the errors
    for index,CRNObj in enumerate( CRNDataList):
        if "Dethier" in PaperNames[index]:
            if "newCRONUS" in ScalingNames[index]:
                dethier_index_newCRONUS = index
            else:
                dethier_index_braucher = index
        elif "Palumbo" in PaperNames[index]:
            if "newCRONUS" in ScalingNames[index]:
                palumbo_index_newCRONUS = index
            else:
                palumbo_index_braucher = index            
        
    P_erate_brauch = CRNDataList[palumbo_index_braucher].GetErosionRates
    P_erate_newCRONUS =CRNDataList[palumbo_index_newCRONUS].GetErosionRates 

    P_B = np.asarray(P_erate_brauch)
    P_nC = np.asarray(P_erate_newCRONUS) 
    
    P_err = np.divide(  np.subtract(P_nC,P_B),P_B)
    
    D_erate_brauch = CRNDataList[dethier_index_braucher].GetErosionRates
    D_erate_newCRONUS =CRNDataList[dethier_index_newCRONUS].GetErosionRates 

    D_B = np.asarray(D_erate_brauch)
    D_nC = np.asarray(D_erate_newCRONUS) 
    
    D_err = np.divide(  np.subtract(D_nC,D_B),D_B)    
    
            
    #===========================================================================    
    # now make plots based on these data
    # 3.26 inches = 83 mm, the size of a 1 column figure
    Fig1 = plt.figure(1, facecolor='white',figsize=(3.26,3.26))  

    # generate a 120,90 grid. 
    gs = GridSpec(100,75,bottom=0.13,left=0.13,right=0.98,top=0.85) 
    ax = Fig1.add_subplot(gs[10:100,5:75])   
    
    ax.plot(P_B,P_err,"ro",markersize=4, label = "Palumbo et al., 2010",markeredgewidth=1)
    ax.plot(D_B,D_err,"bo",markersize=4, label = "Dethier et al., 2014",markeredgewidth=1)

    ax.spines['top'].set_linewidth(1)
    ax.spines['left'].set_linewidth(1)
    ax.spines['right'].set_linewidth(1)
    ax.spines['bottom'].set_linewidth(1) 
    ax.tick_params(axis='both', width=1) 
 
    plt.xlabel('CAIRN erosion rate g cm$^{-2}$ yr$^{-1}$', fontsize = axis_size)
    plt.ylabel('($E_{newCRONUS}$-$E_{CAIRN}$)/$E_{CAIRN}$', fontsize = axis_size)
    #plt.title('Cosmocalc / New_code',fontsize = label_size+6)
    handles, labels = ax.get_legend_handles_labels()
    plt.legend()
    plt.legend(handles, labels, numpoints = 1, bbox_to_anchor=(0., 1.02, 1., .102), 
               loc=3, ncol=2, mode="expand", borderaxespad=0.)
        
    plt.savefig(Dirname+"CAIRNvsnewCRONUSapprox_erate.svg",format = Fileformat)
    
    #Fig1.show()
     
    Fig1.clf()     



if __name__ == "__main__":
    CollateCRNData() 