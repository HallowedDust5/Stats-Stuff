from turtle import Vec2D
from statistics import mean
from random import randint
import matplotlib.pyplot as plt

class Vector2D(Vec2D):
    x:int
    y:int
    mag:float

    def __init__(self,x:int,y:int)->None:
        self.x = x
        self.y = y
        self.mag = abs(self)



MIN = -10
MAX = 10
RANGE = MAX - MIN

def main():
    vector_distribution = [Vector2D(randint(MIN,MAX),randint(MIN,MAX)) for _ in range(10**3)]

    bins = [[0]*RANGE]*RANGE
    x_bins = []
    y_bins = []
    freq = []

    fig = plt.figure()
    ax = fig.add_subplot(projection = '3d')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Freq')


    x_comps = [vector.x for vector in vector_distribution]
    y_comps = [vector.y for vector in vector_distribution]

    avg_vector = Vector2D(mean(x_comps),mean(y_comps))

    for v in vector_distribution:
        disp_vec = v - Vector2D(MIN,MAX)
        disp_vec = Vector2D(disp_vec[0],disp_vec[1])
        bins[abs(disp_vec.y)-1][abs(disp_vec.x)-1]+=1

    for i in range(MIN,MAX):
        for j in range(MIN,MAX):
            y_bins.append(i-MIN)
            x_bins.append(j+MAX)
            freq.append(bins[i][j])

    ax.scatter(
        x_bins,
        y_bins,
        freq,
        c=freq
    )

    plt.show()




if __name__ == '__main__':
    main()
