import sys
import numpy as np
import pylab
import math

class point:
    def __init__(self):
        self.ind = 0
        self.x = .0
        self.y = .0
        self.vx = .0
        self.vy = .0
        self.ang = .0  
        
    def __str__(self):
        return '[{0:d}] Position({1:s}, {2:s}), Velocity({3:s}, {4:s}), Angle({5:s})'\
        .format(self.ind, str(self.x), str(self.y), str(self.vx), str(self.vy), str(self.ang))
    
    def move(self, ax, ay, t):
        # first update the position with the formula s = v0t+ 0.5at^2
        self.x += self.vx * t + 0.5 * ax * t**2 
        self.y += self.vy * t + 0.5 * ay * t**2 
        
        # then update the line velocity and angular velocity
        self.vx += ax*t
        self.vy += ay*t  
        
    def turn(self, omegaz, t):
        # update the angular velocity
        rotate = omegaz*t
        self.ang += rotate
        self.vx = math.cos(rotate) * self.vx - math.sin(rotate) * self.vy
        self.vy = math.sin(rotate) * self.vx + math.cos(rotate) * self.vy
        
    
    def update(self, ax, ay, omegaz, t):
        # transform local coordinate to global coordinate
        ax = ax * math.cos(self.ang) - ay * math.sin(self.ang)
        ay = ax * math.sin(self.ang) + ay * math.cos(self.ang)
        
        self.ind += 1
        self.move(ax, ay, t)
        #print ax
        #print ay
        #print t
        self.turn(omegaz, t)
        
    def get_position(self):
        return [self.x, self.y, self.ang]
 
def isvalid(line):
    try:
        _ =  [float(item) for item in line.strip().split(',')]  
        return True
    except ValueError:
        return False
   
def readcsv(fileName):
    with open(fileName, 'r') as f:
        f.readline()
        raw_data = [[float(item) for item in line.strip().split(',')] \
        for line in f if line if isvalid(line)]
        data = np.array(raw_data)
        
        nrow = data.shape[0]
        data[1:,-1] = data[1:,-1] - data[:nrow-1,-1]
        data[:,-1] /= 1000.0 # transform ms to s
        return data[:, [0,1,5,6]] # read ax, ay, omegaz and t
    
def smooth(data, alpha = 0.01):
    smooth_data = data.copy()
    for i in range(1, data.shape[0]):
        smooth_data[i,:-1] = (alpha * data[i,:-1] + (1 - alpha) * smooth_data[i-1,:-1])
    return smooth_data
    
def simulate(data):
    pt = point()
    x = [0]
    y = [0]
    ang = [0]
    positions = []
    for item in data:
        pt.update(item[0], item[1], item[2], item[3])
        positions.append(pt.get_position())
        #print pt
    return np.array(positions)

def visualize(result, fileName):
    pylab.figure(1)
    pylab.plot(result[:,0], result[:,1], 'rx')
    pylab.plot(result[:,0], result[:,1], 'r')

    pylab.title("Simulation Trajectory\n (data = {0:s})".format(fileName))
    pylab.xlabel("x")
    pylab.ylabel("y")
    pylab.savefig("result_{0:s}.jpg".format(fileName))
    pylab.show() 
    return
    
def errMsg():
    print 'Usage: python cs407-hw03.py <data-file> <alpha>'
    
if __name__ == "__main__":
    if 0:
        dataFile = "RightTurnData.csv"
        rawdata = readcsv(dataFile)
        #rawdata = rawdata[0:1000,:]
        data = smooth(rawdata)
        result = simulate(data)
        plot = visualize(result, dataFile)
    else:
        args = [arg for arg in sys.argv]
        try:
            dataFile = args[1]
            alpha = float(args[2])
            rawdata = readcsv(dataFile)
            data = smooth(rawdata, alpha)
            result = simulate(data)
            plot = visualize(result, dataFile)
        except:
            errMsg()