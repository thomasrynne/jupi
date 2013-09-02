Jupi - Jenkins USB power indicator

Jupi watches jenkins builds and switches usb ports on and off
to reflect the status of the build.

It means you can use usb lights and accessories to indicate the status of the build.

It requires a USB hub which supports the power switching feature.
Hubs typically don't support this feature but some do including hubs in monitors.


Most of the credit goes to 
  http://www.gniibe.org/development/ac-power-control-by-USB-hub/index
 which drew my attention to the usb power switching feature and provided the python code.


Jenkins setup:
  -Install the 'Jenkins Websocket Notifier' plugin
  -For any jobs you want to monitor add 'Websocket Notifier' as a post-build action

Jupi setup:
  > git clone https://github.com/thomasrynne/jupi
  > sudo python setup.py install
  > sudo jupi --list
  > sudo jupi --job JobName
This will switch off/on port 1 to reflect the status of the build

To work out which port is which you can use
  > jupi --port 1 --test
which switches the named port off for 1 second

If you want a more complex setup you can write a short python script using jupi as a library.
    import jupi
    j = jupi.Jupi("localhost", 8080, 8081)
    j.add_binding(None, 1, lambda : j.is_bad("Job1") or j.is_bad("Job2"))
    j.add_binding(None, 2, lambda : j.is_good("Job1"))
    j.start()


