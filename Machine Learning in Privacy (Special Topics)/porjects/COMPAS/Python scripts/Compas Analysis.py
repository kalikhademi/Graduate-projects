#!/usr/bin/env python
# coding: utf-8

# # Compas Analysis
# 
# What follows are the calculations performed for ProPublica's analaysis of the COMPAS Recidivism Risk Scores. It might be helpful to open [the methodology](https://www.propublica.org/article/how-we-analyzed-the-compas-recidivism-algorithm/) in another tab to understand the following.
# 
# ## Loading the Data
# 
# We select fields for severity of charge, number of priors, demographics, age, sex, compas scores, and whether each person was accused of a crime within two years.

# In[1]:


# filter dplyr warnings
get_ipython().run_line_magic('load_ext', 'rpy2.ipython')
import warnings
warnings.filterwarnings('ignore')


# In[2]:


get_ipython().run_cell_magic('R', '', 'library(dplyr)\nlibrary(ggplot2)\nraw_data <- read.csv("./compas-scores-two-years.csv")\nnrow(raw_data)')


# However not all of the rows are useable for the first round of analysis.
# 
# There are a number of reasons remove rows because of missing data:
# * If the charge date of a defendants Compas scored crime was not within 30 days from when the person was arrested, we assume that because of data quality reasons, that we do not have the right offense.
# * We coded the recidivist flag -- `is_recid` -- to be -1 if we could not find a compas case at all.
# * In a similar vein, ordinary traffic offenses -- those with a `c_charge_degree` of 'O' -- will not result in Jail time are removed (only two of them).
# * We filtered the underlying data from Broward county to include only those rows representing people who had either recidivated in two years, or had at least two years outside of a correctional facility.

# In[3]:


get_ipython().run_cell_magic('R', '', 'df <- dplyr::select(raw_data, age, c_charge_degree, race, age_cat, score_text, sex, priors_count, \n                    days_b_screening_arrest, decile_score, is_recid, two_year_recid, c_jail_in, c_jail_out) %>% \n        filter(days_b_screening_arrest <= 30) %>%\n        filter(days_b_screening_arrest >= -30) %>%\n        filter(is_recid != -1) %>%\n        filter(c_charge_degree != "O") %>%\n        filter(score_text != \'N/A\')\nnrow(df)')


# Higher COMPAS scores are slightly correlated with a longer length of stay. 

# In[4]:


get_ipython().run_cell_magic('R', '', 'df$length_of_stay <- as.numeric(as.Date(df$c_jail_out) - as.Date(df$c_jail_in))\ncor(df$length_of_stay, df$decile_score)')


# After filtering we have the following demographic breakdown:

# In[5]:


get_ipython().run_cell_magic('R', '', 'summary(df$age_cat)')


# In[6]:


get_ipython().run_cell_magic('R', '', 'summary(df$race)')


# In[7]:


print("Black defendants: %.2f%%" %            (3175 / 6172 * 100))
print("White defendants: %.2f%%" %            (2103 / 6172 * 100))
print("Hispanic defendants: %.2f%%" %         (509  / 6172 * 100))
print("Asian defendants: %.2f%%" %            (31   / 6172 * 100))
print("Native American defendants: %.2f%%" %  (11   / 6172 * 100))


# In[8]:


get_ipython().run_cell_magic('R', '', 'summary(df$score_text)')


# In[9]:


get_ipython().run_cell_magic('R', '', 'xtabs(~ sex + race, data=df)')


# In[10]:


get_ipython().run_cell_magic('R', '', 'summary(df$sex)')


# In[11]:


print("Men: %.2f%%" %   (4997 / 6172 * 100))
print("Women: %.2f%%" % (1175 / 6172 * 100))


# In[12]:


get_ipython().run_cell_magic('R', '', 'nrow(filter(df, two_year_recid == 1))')


# In[13]:


get_ipython().run_cell_magic('R', '', 'nrow(filter(df, two_year_recid == 1)) / nrow(df) * 100')


# Judges are often presented with two sets of scores from the Compas system -- one that classifies people into High, Medium and Low risk, and a corresponding decile score. There is a clear downward trend in the decile scores as those scores increase for white defendants.

# In[14]:


get_ipython().run_cell_magic('R', '-w 900 -h 363 -u px', 'library(grid)\nlibrary(gridExtra)\npblack <- ggplot(data=filter(df, race =="African-American"), aes(ordered(decile_score))) + \n          geom_bar() + xlab("Decile Score") +\n          ylim(0, 650) + ggtitle("Black Defendant\'s Decile Scores")\npwhite <- ggplot(data=filter(df, race =="Caucasian"), aes(ordered(decile_score))) + \n          geom_bar() + xlab("Decile Score") +\n          ylim(0, 650) + ggtitle("White Defendant\'s Decile Scores")\ngrid.arrange(pblack, pwhite,  ncol = 2)')


# In[15]:


get_ipython().run_cell_magic('R', '', 'xtabs(~ decile_score + race, data=df)')


# ## Racial Bias in Compas
# 
# After filtering out bad rows, our first question is whether there is a significant difference in Compas scores between races. To do so we need to change some variables into factors, and run a logistic regression, comparing low scores to high scores.

# In[16]:


get_ipython().run_cell_magic('R', '', 'df <- mutate(df, crime_factor = factor(c_charge_degree)) %>%\n      mutate(age_factor = as.factor(age_cat)) %>%\n      within(age_factor <- relevel(age_factor, ref = 1)) %>%\n      mutate(race_factor = factor(race)) %>%\n      within(race_factor <- relevel(race_factor, ref = 3)) %>%\n      mutate(gender_factor = factor(sex, labels= c("Female","Male"))) %>%\n      within(gender_factor <- relevel(gender_factor, ref = 2)) %>%\n      mutate(score_factor = factor(score_text != "Low", labels = c("LowScore","HighScore")))\nmodel <- glm(score_factor ~ gender_factor + age_factor + race_factor +\n                            priors_count + crime_factor + two_year_recid, family="binomial", data=df)\nsummary(model)')


# Black defendants are 45% more likely than white defendants to receive a higher score correcting for the seriousness of their crime, previous arrests, and future criminal behavior.

# In[17]:


get_ipython().run_cell_magic('R', '', 'control <- exp(-1.52554) / (1 + exp(-1.52554))\nexp(0.47721) / (1 - control + (control * exp(0.47721)))')


# Women are 19.4% more likely than men to get a higher score.

# In[18]:


get_ipython().run_cell_magic('R', '', 'exp(0.22127) / (1 - control + (control * exp(0.22127)))')


# Most surprisingly, people under 25 are 2.5 times as likely to get a higher score as middle aged defendants.

# In[19]:


get_ipython().run_cell_magic('R', '', 'exp(1.30839) / (1 - control + (control * exp(1.30839)))')


# ### Risk of Violent Recidivism
# 
# Compas also offers a score that aims to measure a persons risk of violent recidivism, which has a similar overall accuracy to the Recidivism score. As before, we can use a logistic regression to test for racial bias.

# In[20]:


get_ipython().run_cell_magic('R', '', 'raw_data <- read.csv("./compas-scores-two-years-violent.csv")\nnrow(raw_data)')


# In[21]:


get_ipython().run_cell_magic('R', '', 'df <- dplyr::select(raw_data, age, c_charge_degree, race, age_cat, v_score_text, sex, priors_count, \n                    days_b_screening_arrest, v_decile_score, is_recid, two_year_recid) %>% \n        filter(days_b_screening_arrest <= 30) %>%\n        filter(days_b_screening_arrest >= -30) %>% \n        filter(is_recid != -1) %>%\n        filter(c_charge_degree != "O") %>%\n        filter(v_score_text != \'N/A\')\nnrow(df)')


# In[22]:


get_ipython().run_cell_magic('R', '', 'summary(df$age_cat)')


# In[23]:


get_ipython().run_cell_magic('R', '', 'summary(df$race)')


# In[24]:


get_ipython().run_cell_magic('R', '', 'summary(df$v_score_text)')


# In[25]:


get_ipython().run_cell_magic('R', '', 'nrow(filter(df, two_year_recid == 1)) / nrow(df) * 100')


# In[26]:


get_ipython().run_cell_magic('R', '', 'nrow(filter(df, two_year_recid == 1))')


# In[27]:


get_ipython().run_cell_magic('R', '-w 900 -h 363 -u px', 'library(grid)\nlibrary(gridExtra)\npblack <- ggplot(data=filter(df, race =="African-American"), aes(ordered(v_decile_score))) + \n          geom_bar() + xlab("Violent Decile Score") +\n          ylim(0, 700) + ggtitle("Black Defendant\'s Violent Decile Scores")\npwhite <- ggplot(data=filter(df, race =="Caucasian"), aes(ordered(v_decile_score))) + \n          geom_bar() + xlab("Violent Decile Score") +\n          ylim(0, 700) + ggtitle("White Defendant\'s Violent Decile Scores")\ngrid.arrange(pblack, pwhite,  ncol = 2)')


# In[28]:


get_ipython().run_cell_magic('R', '', 'df <- mutate(df, crime_factor = factor(c_charge_degree)) %>%\n      mutate(age_factor = as.factor(age_cat)) %>%\n      within(age_factor <- relevel(age_factor, ref = 1)) %>%\n      mutate(race_factor = factor(race,\n                                  labels = c("African-American", \n                                             "Asian",\n                                             "Caucasian", \n                                             "Hispanic", \n                                             "Native American",\n                                             "Other"))) %>%\n      within(race_factor <- relevel(race_factor, ref = 3)) %>%\n      mutate(gender_factor = factor(sex, labels= c("Female","Male"))) %>%\n      within(gender_factor <- relevel(gender_factor, ref = 2)) %>%\n      mutate(score_factor = factor(v_score_text != "Low", labels = c("LowScore","HighScore")))\nmodel <- glm(score_factor ~ gender_factor + age_factor + race_factor +\n                            priors_count + crime_factor + two_year_recid, family="binomial", data=df)\nsummary(model)')


# The violent score overpredicts recidivism for black defendants by 77.3% compared to white defendants.

# In[29]:


get_ipython().run_cell_magic('R', '', 'control <- exp(-2.24274) / (1 + exp(-2.24274))\nexp(0.65893) / (1 - control + (control * exp(0.65893)))')


# Defendands under 25 are 7.4 times as likely to get a higher score as middle aged defendants.

# In[30]:


get_ipython().run_cell_magic('R', '', 'exp(3.14591) / (1 - control + (control * exp(3.14591)))')


# ## Predictive Accuracy of COMPAS
# 
# In order to test whether Compas scores do an accurate job of deciding whether an offender is Low, Medium or High risk,  we ran a Cox Proportional Hazards model. Northpointe, the company that created COMPAS and markets it to Law Enforcement, also ran a Cox model in their [validation study](http://cjb.sagepub.com/content/36/1/21.abstract).
# 
# We used the counting model and removed people when they were incarcerated. Due to errors in the underlying jail data, we need to filter out 32 rows that have an end date more than the start date. Considering that there are 13,334 total rows in the data, such a small amount of errors will not affect the results.

# In[31]:


get_ipython().run_cell_magic('R', '', 'library(survival)\nlibrary(ggfortify)\n\ndata <- filter(filter(read.csv("./cox-parsed.csv"), score_text != "N/A"), end > start) %>%\n        mutate(race_factor = factor(race,\n                                  labels = c("African-American", \n                                             "Asian",\n                                             "Caucasian", \n                                             "Hispanic", \n                                             "Native American",\n                                             "Other"))) %>%\n        within(race_factor <- relevel(race_factor, ref = 3)) %>%\n        mutate(score_factor = factor(score_text)) %>%\n        within(score_factor <- relevel(score_factor, ref=2))\n\ngrp <- data[!duplicated(data$id),]\nnrow(grp)')


# In[32]:


get_ipython().run_cell_magic('R', '', 'summary(grp$score_factor)')


# In[33]:


get_ipython().run_cell_magic('R', '', 'summary(grp$race_factor)')


# In[34]:


get_ipython().run_cell_magic('R', '', 'f <- Surv(start, end, event, type="counting") ~ score_factor\nmodel <- coxph(f, data=data)\nsummary(model)')


# People placed in the High category are 3.5 times as likely to recidivate, and the COMPAS system's concordance 63.6%. This is lower than the accuracy quoted in the Northpoint study of 68%.

# In[35]:


get_ipython().run_cell_magic('R', '', 'decile_f <- Surv(start, end, event, type="counting") ~ decile_score\ndmodel <- coxph(decile_f, data=data)\nsummary(dmodel)')


# COMPAS's decile scores are a bit more accurate at 66%.
# 
# We can test if the algorithm is behaving differently across races by including a race interaction term in the cox model.

# In[36]:


get_ipython().run_cell_magic('R', '', 'f2 <- Surv(start, end, event, type="counting") ~ race_factor + score_factor + race_factor * score_factor\nmodel <- coxph(f2, data=data)\nprint(summary(model))')


# The interaction term shows a similar disparity as the logistic regression above.
# 
# High risk white defendants are 3.61 more likely than low risk white defendants, while High risk black defendants are 2.99 more likely than low.

# In[37]:


import math
print("Black High Hazard: %.2f" % (math.exp(-0.18976 + 1.28350)))
print("White High Hazard: %.2f" % (math.exp(1.28350)))
print("Black Medium Hazard: %.2f" % (math.exp(0.84286-0.17261)))
print("White Medium Hazard: %.2f" % (math.exp(0.84286)))


# In[38]:


get_ipython().run_cell_magic('R', '-w 900 -h 563 -u px', '\nfit <- survfit(f, data=data)\n\nplotty <- function(fit, title) {\n  return(autoplot(fit, conf.int=T, censor=F) + ggtitle(title) + ylim(0,1))\n}\nplotty(fit, "Overall")')


# Black defendants do recidivate at higher rates according to race specific Kaplan Meier plots.

# In[39]:


get_ipython().run_cell_magic('R', '-w 900 -h 363 -u px', 'white <- filter(data, race == "Caucasian")\nwhite_fit <- survfit(f, data=white)\n\nblack <- filter(data, race == "African-American")\nblack_fit <- survfit(f, data=black)\n\ngrid.arrange(plotty(white_fit, "White defendants"), \n             plotty(black_fit, "Black defendants"), ncol=2)')


# In[40]:


get_ipython().run_cell_magic('R', '', 'summary(fit, times=c(730))')


# In[41]:


get_ipython().run_cell_magic('R', '', 'summary(black_fit, times=c(730))')


# In[42]:


get_ipython().run_cell_magic('R', '', 'summary(white_fit, times=c(730))')


# Race specific models have similar concordance values.

# In[43]:


get_ipython().run_cell_magic('R', '', 'summary(coxph(f, data=white))')


# In[44]:


get_ipython().run_cell_magic('R', '', 'summary(coxph(f, data=black))')


# Compas's violent recidivism score has a slightly higher overall concordance score of 65.1%.

# In[45]:


get_ipython().run_cell_magic('R', '', 'violent_data <- filter(filter(read.csv("./cox-violent-parsed.csv"), score_text != "N/A"), end > start) %>%\n        mutate(race_factor = factor(race,\n                                  labels = c("African-American", \n                                             "Asian",\n                                             "Caucasian", \n                                             "Hispanic", \n                                             "Native American",\n                                             "Other"))) %>%\n        within(race_factor <- relevel(race_factor, ref = 3)) %>%\n        mutate(score_factor = factor(score_text)) %>%\n        within(score_factor <- relevel(score_factor, ref=2))\n\n\nvf <- Surv(start, end, event, type="counting") ~ score_factor\nvmodel <- coxph(vf, data=violent_data)\nvgrp <- violent_data[!duplicated(violent_data$id),]\nprint(nrow(vgrp))\nsummary(vmodel)')


# In this case, there isn't a significant coefficient on African American's with High Scores.

# In[46]:


get_ipython().run_cell_magic('R', '', 'vf2 <- Surv(start, end, event, type="counting") ~ race_factor + race_factor * score_factor\nvmodel <- coxph(vf2, data=violent_data)\nsummary(vmodel)')


# In[47]:


get_ipython().run_cell_magic('R', '', 'summary(coxph(vf, data=filter(violent_data, race == "African-American")))')


# In[48]:


get_ipython().run_cell_magic('R', '', 'summary(coxph(vf, data=filter(violent_data, race == "Caucasian")))')


# In[49]:


get_ipython().run_cell_magic('R', '-w 900 -h 363 -u px', 'white <- filter(violent_data, race == "Caucasian")\nwhite_fit <- survfit(vf, data=white)\n\nblack <- filter(violent_data, race == "African-American")\nblack_fit <- survfit(vf, data=black)\n\ngrid.arrange(plotty(white_fit, "White defendants"), \n             plotty(black_fit, "Black defendants"), ncol=2)')


# ## Directions of the Racial Bias
# 
# The above analysis shows that the Compas algorithm does overpredict African-American defendant's future recidivism, but we haven't yet explored the direction of the bias. We can discover fine differences in overprediction and underprediction by comparing Compas scores across racial lines.

# In[50]:


from truth_tables import PeekyReader, Person, table, is_race, count, vtable, hightable, vhightable
from csv import DictReader

people = []
with open("./cox-parsed.csv") as f:
    reader = PeekyReader(DictReader(f))
    try:
        while True:
            p = Person(reader)
            if p.valid:
                people.append(p)
    except StopIteration:
        pass

pop = list(filter(lambda i: ((i.recidivist == True and i.lifetime <= 730) or
                              i.lifetime > 730), list(filter(lambda x: x.score_valid, people))))
recid = list(filter(lambda i: i.recidivist == True and i.lifetime <= 730, pop))
rset = set(recid)
surv = [i for i in pop if i not in rset]


# In[51]:


print("All defendants")
table(list(recid), list(surv))


# In[52]:


print("Total pop: %i" % (2681 + 1282 + 1216 + 2035))


# In[53]:


import statistics
print("Average followup time %.2f (sd %.2f)" % (statistics.mean(map(lambda i: i.lifetime, pop)),
                                                statistics.stdev(map(lambda i: i.lifetime, pop))))
print("Median followup time %i" % (statistics.median(map(lambda i: i.lifetime, pop))))


# Overall, the false positive rate is 32.35%.

# In[54]:


print("Black defendants")
is_afam = is_race("African-American")
table(list(filter(is_afam, recid)), list(filter(is_afam, surv)))


# That number is higher for African Americans at 44.85%.

# In[55]:


print("White defendants")
is_white = is_race("Caucasian")
table(list(filter(is_white, recid)), list(filter(is_white, surv)))


# And lower for whites at 23.45%.

# In[56]:


44.85 / 23.45


# Which means under COMPAS black defendants are 91% more likely to get a higher score and not go on to commit more crimes than white defendants after two year.

# COMPAS scores misclassify white reoffenders as low risk at 70.4% more often than black reoffenders.

# In[57]:


47.72 / 27.99


# In[58]:


hightable(list(filter(is_white, recid)), list(filter(is_white, surv)))


# In[59]:


hightable(list(filter(is_afam, recid)), list(filter(is_afam, surv)))


# ## Risk of Violent Recidivism
# 
# Compas also offers a score that aims to measure a persons risk of violent recidivism, which has a similar overall accuracy to the Recidivism score.

# In[60]:


vpeople = []
with open("./cox-violent-parsed.csv") as f:
    reader = PeekyReader(DictReader(f))
    try:
        while True:
            p = Person(reader)
            if p.valid:
                vpeople.append(p)
    except StopIteration:
        pass

vpop = list(filter(lambda i: ((i.violent_recidivist == True and i.lifetime <= 730) or
                              i.lifetime > 730), list(filter(lambda x: x.vscore_valid, vpeople))))
vrecid = list(filter(lambda i: i.violent_recidivist == True and i.lifetime <= 730, vpeople))
vrset = set(vrecid)
vsurv = [i for i in vpop if i not in vrset]


# In[61]:


print("All defendants")
vtable(list(vrecid), list(vsurv))


# Even moreso for Black defendants.

# In[62]:


print("Black defendants")
is_afam = is_race("African-American")
vtable(list(filter(is_afam, vrecid)), list(filter(is_afam, vsurv)))


# In[63]:


print("White defendants")
is_white = is_race("Caucasian")
vtable(list(filter(is_white, vrecid)), list(filter(is_white, vsurv)))


# Black defendants are twice as likely to be false positives for a Higher violent score than white defendants.

# In[64]:


38.14 / 18.46


# White defendants are 63% more likely to get a lower score and commit another crime than Black defendants.

# In[65]:


62.62 / 38.37


# ## Gender differences in Compas scores
# 
# In terms of underlying recidivism rates, we can look at gender specific Kaplan Meier estimates. There is a striking difference between women and men.

# In[66]:


get_ipython().run_cell_magic('R', '', '\nfemale <- filter(data, sex == "Female")\nmale   <- filter(data, sex == "Male")\nmale_fit <- survfit(f, data=male)\nfemale_fit <- survfit(f, data=female)')


# In[67]:


get_ipython().run_cell_magic('R', '', 'summary(male_fit, times=c(730))')


# In[68]:


get_ipython().run_cell_magic('R', '', 'summary(female_fit, times=c(730))')


# In[69]:


get_ipython().run_cell_magic('R', '-w 900 -h 363 -u px', 'grid.arrange(plotty(female_fit, "Female"), plotty(male_fit, "Male"),ncol=2)')


# As these plots show, the Compas score treats a High risk women the same as a Medium risk man.

# In[ ]:




