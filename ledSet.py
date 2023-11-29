self.LPub = self.create_publisher(bool,"/led/left", 10)
self.RPub = self.create_publisher(bool,"/led/right", 10)

def ledSet(bool left, bool right):
    
    if left is True: lmsg = True
    else: lmsg = False 
        
    if right is true: rmsg = True
    else: rmsg = False 

    self.LPub.publish(lmsg)
    self.RPub.publish(rmsg)
