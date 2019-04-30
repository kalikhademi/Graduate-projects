
#==================================== Merging country of citizenship columns=================================================
#Df= pd.read_table("C:/Users/Mahdi Kouretchian/Desktop/applied_multivariable_analysis/project/us_perm_visas.txt")
#==================================== Merging country of citizenship columns=============================Df['country_of_citizenship'].fillna(" ", inplace = True)
# Df['country'].fillna(" ", inplace = True)
# Df['Country_final']=Df['country_of_citizenship'].astype(str)+Df['country'].astype(str)
# Df.to_csv("/Users/kianamac/Dropbox (UFL)/courses/Spring 2019/MultivariateDataAnalysis/project/output.csv", index=False)====================
# 
def sjoin(x): return ';'.join(x[x.notnull()].astype(str))
