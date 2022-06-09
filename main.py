import alsaseq
import os

if __name__ == "__main__":
    # FSID = os.system("aconnect -l | grep FLUID").split('\'')[1]
    # print(FSID)
    # os.system(f"aconnect \"Vortex Wireless 2\" \"{FSID}\"")

    alsaseq.client('FSynth-Controller', 1, 1, False)

    while True:
        if alsaseq.inputpending():
            ev = alsaseq.input()


            # evtype = ev[0]
            # evdata = ev[7]
            # if evtype == 10 and evdata[4] == 82 and evdata[5] == 127:
            #     self.handleSW()
            # elif evtype == 10 and evdata[4] >= 26 and evdata[4] <= 29 and evdata[5] == 127:
            #     self.handleCCSetTone(evdata[4]-26)
            # elif evtype == 10 and evdata[4] == 4:
            #     self.handlePedal(ev[7][5], ev[6], ev[5])
            # elif evtype == 12:
            #     self.handleAT(ev[7][5], ev[6], ev[5])

    
            # alsaseq.output( (10, 0, 0, 253, (0,0), src, dest, (0, 0, 0, 0, self.pedalCC, val)) )