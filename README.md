# cffi-xll
Python XLL SDK via CFFI


Problem:

    If we just cffi back and forwads we are good.
    We can implement some fast marshalling of XLOPER -> wire easily
    Putting that in Python makes it harder.
    
    So have the python implement  a single callback, and register that with C.
    C translator can work from the xlfRegister strings to unpack parameters? 
    Mini CFF. 
    Must figure out the stack size from the arguments, and go from TOS.
    
    Simplifications:
    
    Always return in the first parameter, which is pre-allocated, so all entry points are void.
    (or interpret correctly).
    
    Async functions just work the same, take away the reference and send via a callback later.
    
    So we have a listener on a single socket/port. 
    
    But for async we need a third channel into the process, since we can recv at any time.
    Makes session management harder.
    
    For synchronous calls
    
    Or should we do them _all_ asynchonous.
    
    Call must prepare all callbacks right away - resolve values, get sheet locations.
    Using OPER types etc will help.
    XLOPER type must be xlfValue/xlfSheetRef whatever to get the details...
    
    Primary connection must be kept alive, use an OnTimer thing to do that, and drain
    any requests (slowly).
    
    Trying to sync the main thread calls with the socket reads won't work. Would ahve to  handover
    to the background thread. Better that async results go via some other channel.
    
    Need a special xlfResult (or use the function number) as a callback. xlAsyncResult, xlResult.
    So when a function is invoked:
        -> Marshal the funciton id, parameters and send them
        -> Receive any results.
        
    Add a macro to connect the back channel thread to another socket/port, as callback.
    xlAsyncRecv or whatever. Or _could_ use stdin/stdout/stderr. DOes windows have those? yes
    it's consoles taht don't. 
    
    Simplest thing that might work.
    stderr channel is processed in another thread, and can do stuff like logging.
    Perhaps introduce a magic header -> <magic><msg> special character int he stream
    otherwise we relay it to stdout.
 
    Use zero characters or something. Binary mode.
    If you do this then the router is smple.
    
    A socket, or zeromq will require more work.
    Anything networks should be a websocket.
    Again, do we have many to make the processing easier. Doing sync calls is hard.
    Is there a perf. drop wit async. 
    
    Ascn -> don't allow remote to do callbacks. Just pre-pack the marshaling.
    
    PoD marshalling is simple.
    We want xlfCaller (always)?
    xltypeRef/xltypeMRef -> include cell references and values? 
    They are rare, so why bother.
    How to marshal...
    Pickle? 
    Marshal?
    Excel Specific. 
    Make sure it is a streamable, pre-allocated protocol. 
    Not like pickel.
    How to finesse the extra data in xltypeRef/xltypeMRef...
    Do we care about the cell references. We shouldn't do.
    Send the params, and then send a second set of resolved paraemters. 
    
    Don't do the sync thing
    Have a second stream for xlResultAsync.
    Have an OnTimer (slow) that allows it to run - make sure cx + buffering are enough.
    
    2x websockets shouldbe ok.
    
    Need to embed the reactor loop inside the call, what does that look like?
    
    Enhance to log, or send stuff toe stdout/stdin.
    
    Protocls: stdout/stderr/stdin. (fast/local/simple) WebSocket (remote, secure, logged).
    In Process -> use named pipes. 
    
    Client must be as simple as possible,.
    Thsse are two different XLLs.
    
    How to do the marshalling synchronously... just invoke a callback witht eh parameters. 
    Can't listen. So then invoke excel directly.
    Relly needs a flask-liek request object to deal with this - only place that Excel12
    can exist...
    
    
    
    
    
    
    
    
    
    
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    