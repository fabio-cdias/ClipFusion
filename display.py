import tkinter as tk
from tkinter import filedialog as fd
import cfusion
import threading

class ClipFusionApp():
    def __init__ (self,root,w=600,r=300):
        self.r_width, self.r_height = w,r
        self.root = root
        self.root.title("ClipFusion")
        self.root.config(background="white")
        self.root.geometry(f"{self.r_width}x{self.r_height}")
        self.stopFlag=False
        self.box_width = 40
        self.button_width = 20
        self.padding=5
        self.filename = tk.StringVar()
        self.output_name = tk.StringVar()

        self.cf = cfusion.ClipFusion()
        self.interface()
        
    def interface(self):
        frame = tk.Frame(self.root,
                         background="white")
        frame.pack(side="bottom",
                   fill="x",
                   padx=10,
                   pady=10)

        proj_name = tk.Label(frame,text="ClipFusion",
                             background="white",
                             height=1,
                             width=1,
                             font=("Arial",30,"bold"))
        
        proj_name.grid(row=0,
                       column=0,
                       columnspan=5,
                       sticky="ew",
                       padx=self.padding,
                       pady=self.padding)

        self.cancel_button = tk.Button(frame,
                                  text="CANCEL",
                                  width=self.button_width,
                                  command=self.cancel,
                                  background="#c4a79d",
                                  foreground="black",
                                  activebackground="#ff4000")
        
        self.cancel_button.grid(row=0,
                           column=5,
                           sticky="ew")

        self.cmd_text = tk.Text(frame,
                           wrap="word",
                           background="white",
                           height=6,
                           width=1,
                           font=("Arial",12),
                           state="disabled")
        
        self.cmd_text.grid(row=1,
                      column=0,
                      columnspan=6,
                      sticky="ew",
                      padx=self.padding,
                      pady=self.padding)

        self.text_out = tk.Entry(frame,
                            textvariable=self.output_name,
                            width=self.box_width)
        
        self.text_out.insert(0,
                        "video.mp4")
        self.text_out.grid(row=3,
                      column=0,
                      columnspan=5,
                      sticky="ew",
                      padx=self.padding,
                      pady=self.padding)

        self.fusion_button = tk.Button(frame,
                                  text="CLIP FUSION!",
                                  width=self.button_width,
                                  command=self.run,
                                  background="#85e332",
                                  foreground="black",
                                  activebackground="#95ff38")
        
        self.fusion_button.grid(row=3,
                           column=5,
                           sticky="ew")

        self.text_in = tk.Entry(frame,
                           textvariable=self.filename,
                           width=self.box_width)
        
        self.text_in.grid(row=2,
                     column=0,
                     columnspan=5,
                     sticky="ew",
                     padx=self.padding,
                     pady=self.padding)

        self.open_button = tk.Button(frame,
                                text="OPEN FILE",
                                command=self.openfile,
                                width=self.button_width)
        
        self.open_button.grid(row=2,
                         column=5,
                         sticky="ew")

    def openfile(self):
        file_path = fd.askopenfilename(title="Open file")
        if file_path:
            self.text_in.delete(0,tk.END)
            self.text_in.insert(0,self.filename)
            self.filename.set(file_path)
            self.cf.filename = file_path

    def lock(self):
        self.text_in.config(state=tk.DISABLED)
        self.text_out.config(state=tk.DISABLED)
        self.open_button.config(state=tk.DISABLED)
        self.fusion_button.config(state=tk.DISABLED)

    def unlock(self):
        self.text_in.config(state=tk.NORMAL)
        self.text_out.config(state=tk.NORMAL)
        self.open_button.config(state=tk.NORMAL)
        self.fusion_button.config(state=tk.NORMAL)

    def cancel(self): 
        if self.thread and self.thread.is_alive():
            self.cf.stop()
            self.unlock()
            
    def run(self):
        self.lock()
        self.cf.outfile = self.output_name.get()
        self.cf.reset_stop()
        self.thread = threading.Thread(target=self.process)
        self.thread.start()
        self.unlock()
        

    def process(self):
        try:
            self.lock()
            self.cf.download_videos(widget=self.cmd_text)
            self.cf.join_clips(widget=self.cmd_text)
            self.cf.export(widget=self.cmd_text)
            self.cf.rmdir()
        finally:
            self.unlock()

if __name__ == "__main__":
    root = tk.Tk()
    clipfusion = ClipFusionApp(root)
    root.mainloop()
