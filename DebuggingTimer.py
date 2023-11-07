__AUTHOR__ = 'Euclid'
PLUGIN_NAME = "DebuggingTimer"
PLUGIN_HOTKEY= 'Ctrl+Shift+D'
VERSION = '3.2.0'

import os
import idaapi
import time


def starttimer():
    f = open("timer.txt", "w+")
    f.write(str(time.time()))
    f.close()
    print("timer has started")

def endtimer():
    print("Ending Timer")
    f = open("timer.txt", "r")
    start = float(f.read())
    end = time.time()
    f.close()
    try:
        os.remove("timer.txt")
    except:
        print("start the timer first")
    print(end-start)

# Global flag to ensure plugin is only initialized once
p_initialized = False

p_timer = False

# Global plugin object
PLUGIN_OBJECT = None

class Timer(idaapi.plugin_t):
    """
    Required plugin entry point for IDAPython Plugins.
    """
    comment = "DebuggingTimer"
    help = ""
    flags= idaapi.PLUGIN_KEEP
    wanted_name = PLUGIN_NAME
    wanted_hotkey = 'Ctrl+Shift+D'
    
    def init(self):
        """
        This is called by IDA when it is loading the plugin.
        """
        global p_initialized, PLUGIN_OBJECT
        try:
            Searcher.register(self, "DebuggingTimer")
        except:
            pass        

        if p_initialized is False:
            def template():
                pass
            p_initialized = True
            idaapi.register_action(idaapi.action_desc_t(
                "DebuggingTimer",
                "Timer for Debugging",
                template(),
                None,
                None,
                0))
            idaapi.attach_action_to_menu("Tmeit", "DebuggingTimer", idaapi.SETMENU_APP)

            # initialize the menu actions our plugin will inject
            PLUGIN_OBJECT = self
            return idaapi.PLUGIN_KEEP

    
    def run(self, arg):
        global p_timer
        """
        This is called by IDA when the plugin is run from the plugins menu
        """
        if p_timer == False:
            p_timer = True
            starttimer()
        else:
            p_timer = False
            endtimer()
        return
    
    def term(self):
        """
        This is called by IDA when it is unloading the plugin.
        """
        pass

     
def PLUGIN_ENTRY():
    return Timer()
