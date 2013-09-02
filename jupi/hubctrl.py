import usb

USB_RT_HUB		=	(usb.TYPE_CLASS | usb.RECIP_DEVICE)
USB_RT_PORT		=	(usb.TYPE_CLASS | usb.RECIP_OTHER)
USB_PORT_FEAT_RESET 	=	4
USB_PORT_FEAT_POWER 	=	8
USB_PORT_FEAT_INDICATOR =       22
USB_DIR_IN		=	0x80		 # device to host

COMMAND_SET_NONE  = 0
COMMAND_SET_LED   = 1
COMMAND_SET_POWER = 2

HUB_LED_GREEN     = 2


def list_power_switching_hubs():
    hubs = {}
    for bus in usb.busses():
        for dev in bus.devices:
            if dev.deviceClass != usb.CLASS_HUB:
                continue
            uh = dev.open()
            try:
                # Get USB Hub descriptor
                desc = uh.controlMsg(requestType = USB_DIR_IN | USB_RT_HUB, 
                                     request = usb.REQ_GET_DESCRIPTOR,
                                     value = usb.DT_HUB << 8,
                                     index = 0, buffer = 1024, timeout = 1000)
            finally:
                del uh
            if not desc:
                continue
            # desc[3] is lower byte of wHubCharacteristics
            if (desc[3] & 0x80) == 0 and (desc[3] & 0x03) >= 2:
                continue
            busnum = int(bus.dirname.lstrip("0") or "0")
            hubs[busnum] = { 'busnum': busnum, 'dev' : dev, 'num_ports' : desc[2] }
    return hubs

def select_hub_device(devnum):
    hubs = list_power_switching_hubs()
    hub_device = None
    if len(hubs) == 0:
       print "No power switching hubs found"
    elif devnum == None:
       if len(hubs) == 1:
           hub_device = hubs.values()[0]["dev"]
       else:
           print "Don't know which hub to use (specify a device number " + str(hubs.keys()) + ")"
    else:
       hub_device = hubs[devnum]["dev"]
    return hub_device

def switch(devnum, portnum, on):
    hub_device = select_hub_device(devnum)
    if hub_device:
        if on:
            request = usb.REQ_SET_FEATURE
        else:
            request = usb.REQ_CLEAR_FEATURE
        uh = hub_device.open()
        uh.controlMsg(requestType = USB_RT_PORT, request = request, value = USB_PORT_FEAT_POWER,
                  index = portnum, buffer = None, timeout = 1000)
        del uh

