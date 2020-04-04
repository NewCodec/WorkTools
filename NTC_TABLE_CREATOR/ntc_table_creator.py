

import numpy as np
import argparse

parser = argparse.ArgumentParser(description='create ntc table for adc_tm')

parser.add_argument("-b", "--beta", type = int , default=3435,help="beta value")
parser.add_argument("-t","--root_temp",type = int, default=25,help="root temperature value")
parser.add_argument("-r","--resistance",type = int, default = 68,help = "ntc resistance in room temp")
parser.add_argument("-p","--pull_up",type = int, default = 100, choices=[30,100,400],help = "pull up value")
parser.add_argument("-s","--step",type = int, default = 4, choices=[1,2,3,4,5],help = "temperature step")
parser.add_argument("-m","--mode",type = str, default = 'v-t',choices=['v-t','r-t','v-r'], help = "out put file mode")
parser.add_argument("-V","--vref",type = float, default = 1.875,choices=[1.875,1.80], help = "vref")
parser.add_argument("-rev","--reverse",action='store_true', default = False, help = "reverse mode")

args = parser.parse_args()

NTC_BETA = args.beta
ROOM_TEMP = args.root_temp
NTC_RESIS = args.resistance
PULL_UP = args.pull_up
TEMP_STEP= args.step
VREF=args.vref
MODE=args.mode
REVERSE=args.reverse
mode_name=['电压-温度','电阻-温度','电压-电阻']
def CaculateResistance(temp):
    return NTC_RESIS*np.exp(NTC_BETA*(np.divide(1,temp+273.15)-np.divide(1,ROOM_TEMP+273.15)))

ntc_table='ntc_table'
if __name__ == "__main__":
    resis=[]
    temps=[]
    volts=[]
    for temp in range(-20,120,TEMP_STEP):
        temps.append(temp)
        res = CaculateResistance(temp)
        vol=np.multiply(VREF,np.divide(res,res+PULL_UP))
        res = int(res*1000)
        vol = round(vol,4)
        resis.append(res)
        volts.append(vol)
    
    if MODE =='v-t':
        c1=volts
        c2=temps
    elif MODE =='r-t':
        c1=resis
        c2=temps
    elif MODE =='v-r':
        c1=volts
        c2=resis
    else:
        print("no support mode")
    if REVERSE:
        c1,c2 = (c2,c1)
    fp = open(ntc_table,"w+")
    print("{\n")
    fp.write("{\n")
    for i in range(len(c1)):
        print('    {'+str(c1[i])+', '+str(c2[i])+'},\n')
        fp.write('    {'+str(c1[i])+', '+str(c2[i])+'},\n')
    print("}\n")
    fp.write("}\n")
    fp.close()
        
    