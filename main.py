#%%
from turtle import Vec2D
from statistics import mean
from random import randrange
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
import pandas as pd

class Vector2D(Vec2D):
    x:float
    y:float
    mag:float

    def __init__(self,x:int,y:int)->None:
        self.x = x
        self.y = y
        self.mag = abs(self)



QUESTIONS ={

    "CONTROL":{
        "LEFT_QUESTIONS":[
        "The rich should face heavier taxes to distribute wealth evenly.",
        "The poor need more help than the rich.",
        "America’s economic system is flawed.",
        ],

        "RIGHT_QUESTIONS":[
        "Hard work separates the rich from the poor.",
        "There is no lack of opportunity in America.",
        "Too much government aid makes people lazy.",
        ],

        "AUTH_QUESTIONS" : [
        "The government protects us.",
        "Safety is a priority.",
        "The people often make poor decisions.",
        ],

        "LIB_QUESTIONS" : [
        "The government often overreaches.",
        "Freedom of speech is a priority.",
        "The government should not be involved in our personal lives.",
        ],
    },

    "BIAS":{
        "LEFT_QUESTIONS":[
        "Money should be distributed more evenly.",
        "Everyone should have equal opportunity.",
        "America’s current economic system is not perfect.",
        ],

        "RIGHT_QUESTIONS":[
        "People are poor because they do not try hard enough.",
        r"The rich earned their money 100% legitimately.",
        "Minimum wage should be abolished.",
        ],

        "AUTH_QUESTIONS" : [
        "The government is mostly good for us.",
        "Safety is more important than freedom.",
        "Democracy is stupid.",
        ],

        "LIB_QUESTIONS" : [
        "Government power should be limited.",
        "People should have control over their life.",
        "Freedom of speech is important.",
        ],
    }

}

MIN = -6
MAX = 6
RANGE = MAX - MIN


#Displays magnitude histogram
def magHist(vec_distro:list):

    fig,ax = plt.subplots()

    x_comps = [vector.x for vector in vec_distro]
    y_comps = [vector.y for vector in vec_distro]

    avg_vec = Vector2D(np.mean(x_comps),np.mean(y_comps))

    disp_distro = [v-avg_vec for v in vec_distro]
    mag_distro = [abs(v) for v in disp_distro]
    
    step = ((max(mag_distro)+1) - min(mag_distro))/10
    plt.hist(mag_distro,
        bins = np.arange(min(mag_distro),max(mag_distro)+1,
            step = step
            )
    )
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Distance from Average Vector')
    ax.set_title('Frequency Distribution from Average Vector')
    plt.show()
    
    #Displays scatterplot with average vector highlighted
def scatter(vec_distro:list):
    fig,ax = plt.subplots()
    x_comps = [vector.x for vector in vec_distro]
    y_comps = [vector.y for vector in vec_distro]

    avg_vec = Vector2D(np.mean(x_comps),np.mean(y_comps))

    plt.scatter(x_comps,y_comps,color="black")
    plt.scatter(avg_vec.x,avg_vec.y, color = "red")
    ax.set_ylim(MIN,MAX)
    ax.set_xlim(MIN,MAX)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.set_ylabel('Lib/Auth',loc = 'top')
    ax.set_xlabel('Left/Right', loc = 'left')
    ax.set_title('Political Vectors')

    plt.show()

def comps_hist(comp_distro:list, target_vec_comp:int, axis:str):

    disp_distro = [v-target_vec_comp for v in comp_distro]
    fig,ax = plt.subplots()


    if axis == 'x':
        ax.set_xlabel('Left/Right')
    elif axis == 'y':
        ax.set_xlabel('Lib/Auth')
    else:
        pass


    ax.set_ylabel('Frequency')
    ax.set_title(f'{axis.upper()} Component Frequency Distribution')
    ax.set_xlim(MIN,MAX)

    plt.hist(disp_distro)
    plt.show()



def heatmap(vec_distribution:list, target_vec:Vector2D,hexsize:int):
    disp_distro = [v-target_vec for v in vec_distribution]
    disp_distro = [Vector2D(v[0],v[1]) for v in disp_distro]

    fig,ax = plt.subplots()

    x_comps = [vector.x for vector in disp_distro]
    y_comps = [vector.y for vector in disp_distro]

    plt.hexbin(x_comps, y_comps, gridsize=hexsize, cmap='Blues',extent=(MIN,MAX,MIN,MAX))
    cb = plt.colorbar(label='Frequency')
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.set_ylabel('Lib/Auth', loc = 'top')
    ax.set_xlabel('Left/Right', loc = 'left')
    ax.set_title('Political Vectors Heatmap')

    plt.axis()

    plt.show()

def overlayScatter(control_vecs:list, bias_vecs:list):
    fig,ax = plt.subplots()

    plt.scatter(
        x=[v.x for v in control_vecs],
        y=[v.y for v in control_vecs],
         c= "green",
        label = 'Control')
    plt.scatter(
        x=[v.x for v in bias_vecs],
        y=[v.y for v in bias_vecs],
         c= "purple",
        label = 'Biased')
    ax.set_ylim(MIN,MAX)
    ax.set_xlim(MIN,MAX)
    ax.legend(loc="upper right")
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.set_ylabel('Lib/Auth', loc = 'top')
    ax.set_xlabel('Left/Right', loc = 'left')
    ax.set_title('Political Vectors')
    # plt.axis()


def ThreeDVisualization(vec_distribution:list,target_vec:Vector2D):
    pass


# Given a number [1,5] outputs [-1,1] to scale
def normQuestion(x:int)->int:
    return .5*x-1.5

#Input df, uses it inplace
def toPoliVec(df:pd.DataFrame,control_or_bias:str):
    questions = QUESTIONS[control_or_bias]
    for col in df.columns[1:]:
        df[col] = df[col].apply(normQuestion)

    def VecGen(person:pd.Series)->Vector2D:
        x_comp=y_comp=0

        for q,value in person.iteritems():
            if q in questions['LEFT_QUESTIONS']:
                x_comp-=value
            elif q in questions['RIGHT_QUESTIONS']:
                x_comp+=value
            elif q in questions['AUTH_QUESTIONS']:
                y_comp+=value
            elif q in questions['LIB_QUESTIONS']:
                y_comp-=value

        return Vector2D(x_comp, y_comp)


    df['PVecs'] = df.apply(VecGen,axis=1)


#%%

control_df = pd.read_csv('Political Leanings 1.csv')
bias_df = pd.read_csv('Political Leanings 2.csv')
for col in control_df.columns[1:]:
    control_df[col] = control_df[col].apply(normQuestion)
for col in bias_df.columns[1:]:
    bias_df[col] = bias_df[col].apply(normQuestion)
toPoliVec(control_df,'CONTROL')
toPoliVec(bias_df,'BIAS')
#%%


magHist(bias_df.PVecs.tolist())
heatmap(bias_df.PVecs.tolist(),Vector2D(0,0),15)
scatter(bias_df.PVecs.tolist())
comps_hist([v.x for v in bias_df.PVecs.tolist()],0,'x')
comps_hist([v.y for v in bias_df.PVecs.tolist()],0,'y')


#%%
magHist(control_df.PVecs.tolist())
heatmap(control_df.PVecs.tolist(),Vector2D(0,0),15)
scatter(control_df.PVecs.tolist())
comps_hist([v.x for v in control_df.PVecs.tolist()],0,'x')
comps_hist([v.y for v in control_df.PVecs.tolist()],0,'y')


#%%

overlayScatter(bias_df.PVecs.tolist(),control_df.PVecs.tolist())
