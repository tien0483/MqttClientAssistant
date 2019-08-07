def get_pass():
    import tkinter
    import tkinter.simpledialog
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    return tkinter.simpledialog.askstring('Password','Enter Your Password:', show='*')
get_pass()