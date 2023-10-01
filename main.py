#Project by Omar Hossam Khalil || 20101110
import simpy

def empty_l(size):
    l = []
    for i in range(size):
        l.append(-1)
    return l

#store output
produced = 0

#track how buffer changes
buf1 = empty_l(200001) 
buf2 = empty_l(200001)
buf3 = empty_l(200001)
buf4 = empty_l(200001)

#track machine utilization
ins = []
machine2 = []
machine3 = []
machine4 = []
out = []

#track buffer sizes
buffer = [5,5,5,5]

#track blocking
downtime = [0, 0, 0, 0, 0]

totaltime = 0

class Packing_Line:
    machines = []
    buffers = []

    def __init__(self, env):
        self.env = env
        for i in range(5):
            self.machines.append(simpy.Resource(env))
        for i in range(4):
            self.buffers.append(simpy.Resource(env, 5))
        
    #packing
    def buff5(self):
        global produced
        global buf4, buffer, ins, out

        with self.machines[4].request() as request2:
            yield request2
            yield self.env.timeout(6)
            
            out.append(env.now)

            if(env.now * 2 < 200001):
                buf4[int(env.now * 2)] = buffer[3]+1
                buffer[3] += 1
            
            produced += 1
        
    #sealing
    def buff4(self):  
        global buf4, buf3, buffer, ins, out, machine4
        with self.buffers[3].request() as request:
            yield request
            with self.machines[3].request() as request2:
                yield request2
                
                if(env.now * 2 < 200001):
                    buf3[int(env.now * 2)] = buffer[2]+1
                    buffer[2] += 1
                
                yield self.env.timeout(5)
                machine4.append(env.now)
                
                if(env.now * 2 < 200001):
                    buf4[int(env.now * 2)] = buffer[3]-1
                    buffer[3] -= 1
        
        with self.machines[4].request() as request2:
            yield request2
        
        self.env.process(self.buff5())

    #labeling
    def buff3(self): 
        global buf2, buf3, buffer, ins, out, machine3
        with self.buffers[2].request() as request:
            yield request
            with self.machines[2].request() as request2:
                yield request2
                
                if(env.now * 2 < 200001):
                    buf2[int(env.now * 2)] = buffer[1]+1
                    buffer[1] += 1
                
                yield self.env.timeout(8)
                machine3.append(env.now)
                
                if(env.now * 2 < 200001):
                    buf3[int(env.now * 2)] = buffer[2]-1
                    buffer[2] -= 1
            
            with self.buffers[3].request() as request2:
                yield request2
            
            self.env.process(self.buff4())
    
    #capping
    def buff2(self):
        global buf1, buf2, buffer, ins, out, machine2
        
        with self.buffers[1].request() as request:
            yield request
            
            with self.machines[1].request() as request2:
                yield request2
            
                if(env.now * 2 < 200001):
                    buf1[int(env.now * 2)] = buffer[0]+1
                    buffer[0] += 1
                    
                yield self.env.timeout(5)
                machine2.append(env.now)
            
                x = int(env.now * 2)
                if( x < 200001):
                    buf2[x] = buffer[1]-1
                    buffer[1] -= 1
            
            with self.buffers[2].request() as request2:
                yield request2
            
            self.env.process(self.buff3())
    #filling
    def buff1(self):
        global buf1, buffer, ins, out, machine1
        with self.buffers[0].request() as request:
            yield request     
            
            with self.machines[0].request() as request2:
                yield request2
                yield self.env.timeout(6.5)
            
                ins.append(env.now-6.5)  
                x = int(env.now * 2)
            
                if( x < 200001):
                    buf1[x] = buffer[0]-1
                    buffer[0] -= 1
            
            with self.buffers[1].request() as request2:
                yield request2
            
            self.env.process(self.buff2())
    #Start of process   
    def buff0(self):
        with self.buffers[0].request() as request2:
            yield request2
            self.env.process(self.buff1())

def setup(env):
    fact = Packing_Line(env)
    while True:
            yield env.process(fact.buff0())
            
def stats(buffers, produced, machines):
    global downtime, totaltime
    #calculate and print levels in buffers
    c = 0
    sum = [0, 0, 0, 0]
    for i in buffers:
        for j in range(1, len(i)):
            if(i[j] == -1):
                i[j] = i[j-1]
            sum[c] += min(5 - i[j], 5)
        c+=1
    sum[0] = 0
    
    print("Units: ", produced)
    print("Throughput: ", produced/100000)
    
    print("Average level in buf1: ", sum[0]/200000)
    print("Average level in buf2: ", sum[1]/200000)
    print("Average level in buf3: ", sum[2]/200000)
    print("Average level in buf4: ", sum[3]/200000) 

    #print and calculate the value Down time probability of machines
    down = [6.5, 5, 8, 5, 6]
    c = 0
    for i in machines:
        for j in range(1, len(i)):
            downtime[c] += i[j] - i[j-1] - down[c]
        c+=1
    
    print("Down time probability of machine 1: ", downtime[0]/100000)
    print("Down time probability of machine 2: ", downtime[1]/100000)
    print("Down time probability of machine 3: ", downtime[2]/100000)
    print("Down time probability of machine 4: ", downtime[3]/100000)
    print("Down time probability of machine 5: ", downtime[4]/100000)
    
    for i in range(len(out)):
        totaltime += out[i] - ins[i]
    print("Average flow times: ", totaltime/produced)


env = simpy.Environment()
env.process(setup(env))
env.run(until=100000)

buffers = [buf1, buf2, buf3, buf4]
machines = [ins, machine2, machine3, machine4, out]

stats(buffers, produced, machines)


