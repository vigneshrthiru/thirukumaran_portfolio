#!/usr/bin/env python
# coding: utf-8

# In[157]:


import pandas as pd


# In[158]:


food=pd.read_csv(r'C:\Users\Vignesh\Desktop\pandas\real_world_projects\food_marketing.csv')
food


# In[159]:


food.head()


# In[160]:


pd.set_option('display.max.columns',40)
pd.set_option('display.max.rows',2205)


# In[161]:


food.info()


# In[162]:


food.drop_duplicates(keep=False, inplace=True)


# In[163]:


food.info()


# In[164]:


food['Total_Children']=food[['Kidhome','Teenhome']].sum(axis=1)


# In[165]:


food.head()


# In[166]:


food['marital_Divorced']=food['marital_Divorced'].replace({1:5,0:0})


# In[167]:


food[food['marital_Divorced']!=0].head()


# In[168]:


food['marital_Married']=food['marital_Married'].replace({1:4,0:0})
food['marital_Single']=food['marital_Single'].replace({1:3,0:0})
food['marital_Together']=food['marital_Together'].replace({1:2,0:0})
food['marital_Widow']=food['marital_Widow'].replace({1:1,0:0})


# In[169]:


food['marital_Status']=food[['marital_Divorced','marital_Married','marital_Single','marital_Together','marital_Widow']].sum(axis=1)


# In[170]:


food[food['marital_Status']!=0].head()


# In[171]:


food['marital_Status_str']=food['marital_Status'].map({5:'Divorced',4:'Married',3:'Single',2:'Together',1:'Widow'})


# In[172]:


food.info()


# In[173]:


food['education_2n Cycle']=food['education_2n Cycle'].replace({1:1,0:0})
food['education_Basic']=food['education_Basic'].replace({1:2,0:0})
food['education_Graduation']=food['education_Graduation'].replace({1:3,0:0})
food['education_Master']=food['education_Master'].replace({1:4,0:0})
food['education_PhD ']=food['education_PhD'].replace({1:5,0:0})


# In[174]:


food['educational_Status']=food[['education_2n Cycle','education_Basic','education_Graduation','education_Master','education_PhD ']].sum(axis=1)


# In[175]:


food[food['educational_Status']!=0].head()


# In[176]:


food['Accepted_campaigns']=food[['AcceptedCmp3','AcceptedCmp4','AcceptedCmp5','AcceptedCmp1','AcceptedCmp2']].sum(axis=1)


# In[177]:


food[food['Accepted_campaigns']!=0].head()


# In[178]:


food.info()


# In[179]:


food.corr(method='pearson')['Accepted_campaigns'].sort_values(ascending=False)


# In[180]:


food['Accepted_campaigns']=(food['Accepted_campaigns']!=0).astype(int)


# In[181]:


food[food['Accepted_campaigns']!=0].head()


# In[182]:


food.corr(method='pearson')['Accepted_campaigns'].sort_values(ascending=False)


# In[183]:


food[food['Accepted_campaigns']!=0].head()


# In[184]:


import seaborn as sns
sns.heatmap(food.corr(method='pearson'))


# In[185]:


import seaborn as sns
all_correlations=food.corr(method='pearson')
all_correlations=all_correlations[(all_correlations>0.3)&(all_correlations<1)]
sns.heatmap(food.corr(method='pearson'))


# In[186]:


all_correlations['Accepted_campaigns']


# In[187]:


food['Age'].sort_values()


# In[188]:


age_groups=[(23,30),(31,40),(41,50),(51,60),(61,70),(71,80)]

def assign_age_groups(Age):
    for age_range in age_groups:
        if age_range[0] <= Age <= age_range[1]:
            return f"{age_range[0]}-{age_range[1]}"
    return("Unknown")
       
        
food['Age_Group']=food['Age'].apply(assign_age_groups)   


# In[189]:


food.head()


# In[190]:


food[['Age','Age_Group']].head()


# In[191]:


import seaborn as sns


# In[192]:


age_order=[(23-30),(31-40),(41-50),(51-60),(61-70),(71-80)]

sns.pointplot(data=food,x='Age_Group', y='Accepted_campaigns', order=age_order)


# In[193]:


counts=food['Age_Group'].value_counts()
counts


# In[194]:


percentage=counts/food.shape[0]
percentage


# In[195]:


percent_food=percentage.reset_index()
percent_food


# In[196]:


percent_food.columns=['Age_Group','percentage']


# In[197]:


percent_food=percent_food.sort_values('Age_Group')


# In[198]:


percent_food


# In[199]:


import matplotlib.pyplot as plt
sns.barplot(x='Age_Group',y='percentage',data=percent_food)
plt.title('Percentage of Accepted Campaign per Age Group')
plt.show()


# In[200]:


food.head()


# In[201]:


food.groupby('Age_Group')['MntTotal'].sum()


# In[202]:


grouped_food=food.groupby('Age_Group')['MntTotal'].sum().reset_index()
grouped_food


# In[203]:


grouped_food=food.groupby('Age_Group')['MntTotal'].sum().reset_index()

sns.barplot(x='Age_Group',y='MntTotal',data=grouped_food)
plt.title('Amount spent per age group')
plt.show()


# In[204]:


accept_camp=food[food['Accepted_campaigns']!=0]

grouped_food=food.groupby('Age_Group')['MntTotal'].sum().reset_index()

sns.barplot(x='Age_Group',y='MntTotal',data=grouped_food)
plt.title('Amount spent per age group')
plt.show()


# In[ ]:


#age segmentation core audience for accepting campaigns right now is 31-70,23-30,71 and up accept at higher rates


# In[205]:


food.head()


# In[209]:


sum_food=pd.DataFrame(food[['NumCatalogPurchases','NumStorePurchases','NumWebPurchases']].sum(),columns=['sums'])


# In[215]:


sum_food=sum_food.reset_index()


# In[216]:


sum_food.rename(columns={'index':'Type_of_Purchases'},inplace=True)


# In[217]:


sum_food


# In[218]:


sns.barplot(x='Type_of_Purchases',y='sums',data=sum_food)


# In[219]:


accept_camp=food[food['Accepted_campaigns']!=0]
sum_food=pd.DataFrame(accept_camp[['NumCatalogPurchases','NumStorePurchases','NumWebPurchases']].sum(),columns=['sums'])
sum_food=sum_food.reset_index()
sum_food.rename(columns={'index':'Type_of_Purchases'},inplace=True)
sns.barplot(x='Type_of_Purchases',y='sums',data=sum_food)


# In[221]:


x=sns.jointplot(data=food,x='MntTotal',y='NumWebPurchases',kind='kde')
x.plot_joint(sns.regplot,color='r')


# In[222]:


x=sns.jointplot(data=food,x='MntTotal',y='NumStorePurchases',kind='kde')
x.plot_joint(sns.regplot,color='yellow')


# In[223]:


x=sns.jointplot(data=food,x='MntTotal',y='NumCatalogPurchases',kind='kde')
x.plot_joint(sns.regplot,color='black')


# In[ ]:


# 2 directions: Boost up the higher percentage catalogue customers or focus on Instore/web because they have more traffic


# In[225]:


sns.regplot(x='Total_Children',y='MntTotal',data=food)


# In[226]:


sns.regplot(x='Total_Children',y='Accepted_campaigns',data=food)


# In[ ]:


# less kids= More likely to accept camapign, spend less to people who are having the least number of children


# In[230]:


sns.regplot(x='educational_Status',y='Accepted_campaigns',data=food)


# In[231]:


sns.regplot(x='educational_Status',y='MntTotal',data=food)


# In[ ]:


#education isn't really significant in our segmentation


# In[232]:


sns.countplot(x='marital_Status_str',data=food)


# In[236]:


sns.regplot(x='marital_Status',y='MntTotal',data=food)


# In[237]:


rel_food=food.groupby('marital_Status_str')['MntTotal'].sum().reset_index()


# In[238]:


rel_food


# In[239]:


sns.barplot(x='marital_Status_str',y='MntTotal',data=rel_food)


# In[242]:


total=food['marital_Status_str'].value_counts()
accepted=food[food['Accepted_campaigns']==1]['marital_Status_str'].value_counts()


# In[243]:


accepted=food[food['Accepted_campaigns']==1]['marital_Status_str'].value_counts()


# In[244]:


accepted


# In[245]:


pect_mat=accepted/total*100


# In[247]:


pect_mat.reset_index()


# In[ ]:





# In[ ]:





# In[253]:


#married,single,together are spending a lot more money.


# In[ ]:





# ## OVERALL FINDING
#  
#  
#  ## Age-30-70 were spending more money but less likely to accept campaigns,higher volume have though
#  ## Catalog was more likely to accept campaign but in person spends more ,recommend a split between all
#   30 web 30 store  40 catalog
# # Focus on people with no kids or less kids
# # Education no impact not to target any group
# ## Marital status doesnt play a big part
# 

# ## focus on middle aged people with no kids, target on different platforms with a recommended split
# ## new users spend more money focus on 21-30 statistically who accepted campaigns high.

# In[ ]:





# In[ ]:




