import wget, os, argparse,sys
from moviepy.editor import VideoFileClip, concatenate_videoclips
import tkinter as tk, threading

class ClipFusion:
	def __init__ (self,filename="video.m3u8",outfile="video.mp4"):
		self.total_videos = 0
		self.download = ""
		self.dirname = "temp/"
		self.filename = filename
		self.out_video = ""  #Concatenated video, not the name of output file
		self.outfile = outfile
		self.stop_event = threading.Event()

	def rmdir(self):
		if self.stop_event.is_set():
			return
		if os.path.isdir(self.dirname):
			for root, _, files in os.walk(self.dirname):
				for f in files:
					file_path = os.path.join(root,f)
					os.remove(file_path)
				os.rmdir(self.dirname)

	def mkdir(self):
		if self.stop_event.is_set():
			return
		if not os.path.isdir(self.dirname):
			os.mkdir(self.dirname)

	def load_stream(self):
		if self.stop_event.is_set():
			return
		links =[]
		with open(self.filename,"r") as line:
			lines = line.readlines()

		self.total_videos = 0
		for line in lines:
			if self.stop_event.is_set():
				return
			if "https://" in line:
				links.append(line.replace("\n",""))
				self.total_videos += 1
		return links

	def download_videos(self, fnum = 0, widget = None):
		if self.stop_event.is_set():
			return
		self.rmdir()
		links = self.load_stream()
		self.mkdir()

		if widget is not None:
			def progress_bar(current, total, width=10):
				progress = int((current) / total * width)*"|" if total else 0  # Avoid division by zero
				bar = f"Downloading -- {fnum} / {self.total_videos} video files.\n{str(progress)}\n{round(current*0.001,2)}/{round(total*0.001,2)} (KB) kiloBytes"
				widget.config(state="normal")
				widget.delete(1.0, tk.END)
				widget.insert(tk.END, bar)
				widget.config(state="disabled")
				widget.update_idletasks()


			for url in links:
				if self.stop_event.is_set():
					break
				self.download = wget.download(url,out = self.dirname + str(fnum) + ".ts",bar=progress_bar)
				fnum +=1
		else:
			for url in links:
				self.download = wget.download(url,out = self.dirname + str(fnum) + ".ts")
				fnum +=1
	
	def join_clips(self,widget=None):
		if self.stop_event.is_set():
			return
		section = []

		if widget is not None:
			widget.config(state="normal")
			widget.delete(1.0, tk.END)
			widget.insert(tk.END, "Joining Clips...")
			widget.update_idletasks()
			widget.config(state="disabled")

		for _, _, files in os.walk(self.dirname):
			files.sort()
		for vclip in files:
			if self.stop_event.is_set():
				break
			clip = VideoFileClip(self.dirname + vclip)
			section.append(clip)
		self.out_video = concatenate_videoclips(section, method = "compose")

	def export(self,widget=None):
		if self.stop_event.is_set():
			return
		if widget is not None:
			widget.config(state="normal")
			widget.delete(1.0, tk.END)
			widget.insert(tk.END, f"Exporting video as '{self.outfile}'")
			widget.update_idletasks()
			widget.config(state="disabled")

		self.out_video.write_videofile(self.outfile)

		if widget is not None:
			widget.config(state="normal")
			widget.insert(tk.END, f"\nDONE!")
			widget.update_idletasks()
			widget.config(state="disabled")
		
	def stop(self):
		self.stop_event.set()
		
	def reset_stop(self):
		self.stop_event.clear()
		
	def main(self):
		parser = argparse.ArgumentParser(description = "ClipFusion: by Fabio Dias. This tool downloads videos from M3U8 or TXT playlists and sequentially merges them into a single video file.", usage = "python3 %(prog)s [-h] [-i] <input.m3u8> [-o] <output.mp4>")
		parser.add_argument("-i", "--input", type=str,metavar="input.m3u8", required=True, help="The path to the .m3u8 or .txt video url playlist.")
		parser.add_argument("-o", "--output", type=str,metavar="output.mp4", default = "output.mp4", help = "The path to the output video file. Default: 'output.mp4'")
		args = parser.parse_args()
	
		self.filename = args.input
		self.outfile = args.output
		dirname = "temp/"
		os.system("clear")
		self.download_videos()
		os.system("clear")
		self.join_clips()
		self.export()
		self.rmdir()

if __name__  == "__main__":
	cf = ClipFusion()
	cf.main()
