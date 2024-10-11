import serial, time
import Commands_Ismatec_V2 as ismatec_pump
import keyboard

t0 = int(time.time()) # starting time
pumpe = ismatec_pump.ismatec("COM4") 

pumpe.kanalmodus(2) # configure operating mode of pump
pumpe.pumpenmodus(1) # configure operating mode of pump

for n in range(1,5):
    pumpe.ratemodus(n)
    
# definitions
    # pump channel 1: PBS_O2rich
    # pump channel 2: PBS_O2poor
    

# parameters:
ratio_O2 = [0, 0.2, 0.4, 0.6, 0.8, 1] 
total_pump_rate = 0.5 
volume_flushing = 0.5 


i = 0

pumpe.rate(1, total_pump_rate) # first postition
pumpe.rate(2, total_pump_rate) # first postition

pumpe.start(1) # start flushing with PBS
pumpe.start(2) # start flushing with PBS

time.sleep(90) # flushing the sensor 
pumpe.stop(1) # end flushing with PBS
pumpe.stop(2) # end flushing with PBS


while True: # main loop: calibration sequence
    print(time.strftime('%H:%M:%S', time.gmtime(int(time.time()) - t0)),
          "Flushing", i+1, "with", ratio_O2[i]*100,"% starts")
    pumpe.rate(2, total_pump_rate*ratio_O2[i]) 
    pumpe.rate(1, total_pump_rate-(total_pump_rate*ratio_O2[i])) 
    pumpe.start(1) 
    pumpe.start(2)
    time.sleep(volume_flushing/total_pump_rate*60) 
    pumpe.stop(1)
    pumpe.stop(2) 
    
    time.sleep(10) # 15s Zeitpuffer 
    print(time.strftime('%H:%M:%S', time.gmtime(int(time.time()) - t0)),
          "PalmSense measurement", i+1, "with", ratio_O2[i]*100,"% starts")
    keyboard.press_and_release('F5')
    
    time.sleep(112)
    i = i+1
    if i == len(ratio_O2): 
         break
    
    
print(time.strftime('%H:%M:%S', time.gmtime(int(time.time()) - t0)),
      "Calibration sequence successfully completed!")

