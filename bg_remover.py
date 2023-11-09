import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from rembg import remove
import os
import customtkinter as ctk
import io
import pygame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

 #----------------------SOUND SETUP-------------------------------------------# 
pygame.mixer.init()

reset_sound = pygame.mixer.Sound("reset_sound.mp3")
reset_sound.set_volume(0.5)

done_sound = pygame.mixer.Sound("done.mp3")
done_sound.set_volume(0.4)

link_sound = pygame.mixer.Sound("link_sound.mp3")
link_sound.set_volume(0.6)

hover_sound = pygame.mixer.Sound("hover_sound.mp3")
hover_sound.set_volume(0.7)

hover_sound_leave = pygame.mixer.Sound("hover_sound_leave.wav")
hover_sound_leave.set_volume(0.7)

main_theme = pygame.mixer.Sound("main_theme.mp3")
main_theme.set_volume(0.2)

#------------------MAKING THE APP CLASS-----------------------------------------------#  

class BgRemoverApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.title("VIKZ BG REMOVER")

 
 #------------------APP WINDOW SETUP-----------------------------------------------#  
 
 # SETTING THE WINDOW SIZE
        
        window_width = 800
        window_height = 600


        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

# MAKING THE WINDOW NON-RESIZEABLE

        self.resizable(width=False, height=False)
        self.configure(bg="EFEFEF")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)



#------------------IMAGE SETUP-----------------------------------------------#  

# SETTING THE CORRECT FILEPATH

        current_path = os.path.join(os.path.dirname(__file__))
        image_path = os.path.join(os.path.dirname(__file__))
        
# LOAD AND CREATE ICON        
        
        icon_path = os.path.join(os.path.dirname(__file__), "maybe_icon.ico")
        self.iconbitmap(icon_path)

# LOAD AND CREAT BG IMAGE
        
        self.bg_image = ctk.CTkImage(Image.open(current_path + "/bg_8bit_space.png"), size=(800,600))
        self.bg_image_label = ctk.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.place(relx=0.5, rely=0.5, anchor='center')
        

        self.frame = ctk.CTkFrame(self, fg_color="transparent", border_width=0)
        
        
        
#------------------SETTING ALIEN LOGO-----------------------------------------------#  

# METHODS FOR HOVERING OVER LOGO

        def change(event):
            self.LogoContainer.configure(image=self.hover_logo,fg_color="transparent")
            hover_sound.play()

        def change_back(event): 
            self.LogoContainer.configure(image=self.logo,fg_color="transparent")
        

# LOADING AND CREATING THE LOGO
  
        self.logo = ctk.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(60,40))
        self.hover_logo = ctk.CTkImage(Image.open(os.path.join(image_path, "hover_logo.png")), size=(60, 40))

        
        self.vikz_image = ctk.CTkImage(Image.open(os.path.join(image_path, "vikz.png")), size=(100,60))
        
        self.bg_remover_image = ctk.CTkImage(Image.open(os.path.join(image_path, "bg_remover2.png")), size=(160,70))

        self.LogoContainer = ctk.CTkButton(self.frame,text="",image=self.logo, fg_color="transparent",hover=False, command=self.open_spotify)
        
        self.bg_remover_image_container = ctk.CTkLabel(self.frame,text="", image= self.bg_remover_image)
        self.vikz_image_container = ctk.CTkLabel(self.frame,text="", image= self.vikz_image)
        
        self.bg_remover_image_container.grid(row=0, column=1,pady=(0,20), columnspan=2, sticky="e")
        self.vikz_image_container.grid(row=0, column=0,pady=(0,20), columnspan=2, sticky="w")
        
        
        self.LogoContainer.bind("<Enter>", change)
        self.LogoContainer.bind("<Leave>", change_back)
        self.LogoContainer.grid(row=0, column=0,pady=(0,20), columnspan=2)
    
        
#------------------SETTING UP THE TWO CANVASES-----------------------------------------------#  
        
#INPUT CANVAS
        self.input_canvas = ctk.CTkCanvas(self.frame, width=400, height=400, bg="black",highlightthickness=2)

#OUTPUT CANVAS
        self.output_canvas = ctk.CTkCanvas(self.frame, width=400, height=400, bg="black",highlightthickness=2)
        
#PLACING THEM ON THE APP

        self.frame.grid()
        

        self.input_canvas.grid(row=1, column=0, padx=10)
        self.output_canvas.grid(row=1, column=1, padx=10)

#------------------BUTTONS-----------------------------------------------#  
        
# "LOAD IMAGE" BUTTON
        
        self.open_image = ctk.CTkButton(self, text= "Select Image", command=self.load_image,text_color="black",border_width=2, corner_radius=25, border_color="black", font=("Roboto bold", 13))
        self.open_image.grid(row=0, column=0, columnspan=2, padx=10, pady=(0, 15),sticky="s")

# "RESET" BUTTON
        
        self.reset_btn = ctk.CTkButton(self, text="RESET", command=self.reset,text_color="black",border_width=2, corner_radius=25, border_color="black", font=("Roboto bold", 15))
        self.reset_btn.grid(row=1, column=0, padx=10, pady=(0, 30))
        
# LINK BUTTON
        
        self.open_github_link = ctk.CTkButton(self, text="Check out my GitHub!", command=self.open_github,text_color="black",border_width=2, corner_radius=25, border_color="black", font=("Roboto bold", 13))
        self.open_github_link.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="n")
        
# START/STOP MUSIC BUTTON
        
        stop_image_path = os.path.join(os.path.dirname(__file__))
        self.stop_image = ctk.CTkImage(Image.open(os.path.join(stop_image_path, "stop.png")))
        self.play_image = ctk.CTkImage(Image.open(os.path.join(image_path, "play.png")))
        self.stop_start_music = ctk.CTkButton(self,image=self.stop_image,text="Stop Music", command=self.stop_music,text_color="black",border_width=2, corner_radius=25, border_color="black", font=("Roboto", 13))
        self.stop_start_music.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="se")

# Volume Slider
        self.volume_slider = ctk.CTkSlider(self, from_=0.0, to=1.0, command=self.volume, width=100)
        self.volume_slider.grid(row=1, column=0, sticky="e",padx=30, pady=(5, 55))
        self.volume_slider.set(0.2)
   
   
   
#----------------------METHODS-------------------------------------------# 
    
    def load_image(self):
        link_sound.play()

        file_path = filedialog.askopenfilename(title="Select a File", filetypes=(("JPEG", "*.jpg"), ("PNG", "*.png"),("all files", "*.*")))

        if file_path:
            _, file_extension = os.path.splitext(file_path)
            allowed_extensions = {".jpg", ".jpeg", ".png"}

            if file_extension.lower() in allowed_extensions:
                self.file_path = file_path

                self.input_image = Image.open(self.file_path)
                self.input_image = self.input_image.resize((400, 400))
                self.input_photo = ImageTk.PhotoImage(self.input_image)

                self.input_canvas.create_image(0, 0, anchor=tk.NW, image=self.input_photo)

                self.open_image.configure(text="Remove BG", command=self.remove_bg, state="normal")
            else:
                messagebox.showerror("BAD FILE TYPE", "Only JPEG (.jpg) and PNG (.png) files are supported.")
    
       
    def remove_bg(self):
        link_sound.play()
        
        with open(self.file_path, "rb") as i:
            input_data = i.read()
            output_data = remove(input_data)
        
        self.output_image = Image.open(io.BytesIO(output_data))
        self.output_image = self.output_image.resize((400, 400))
        self.output_photo = ImageTk.PhotoImage(self.output_image)
        

# Display the image on the canvas

        self.output_canvas.create_image(0, 0, anchor=tk.NW, image=self.output_photo)

        self.open_image.configure(text="Save", command=self.save_image, state="normal")

        self.configure(cursor="")

    def reset(self):
        reset_sound.play()
        self.input_canvas.delete("all")
        self.output_canvas.delete("all")
        self.open_image.configure(text="Select Image", command=self.load_image, state="normal")

    def save_image(self):
        link_sound.play()
        output_path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=(("Png","*.png*"),("Png","*.png*") ))
        if output_path:
            self.output_image.save(output_path)
            messagebox.showinfo("DONE!", "Image saved successfully!")
            done_sound.play()
        self.reset()

    def volume(self, x):
        main_theme.set_volume(self.volume_slider.get())
        print(self.volume_slider.get())
         


 #----------------------LINK OPENING-------------------------------------------# 
    
    def open_github(self):
        link_sound.play()
        webbrowser.open_new_tab("https://github.com/vnnikolov30")
    
    def open_spotify(self):
        link_sound.play()
        webbrowser.open_new_tab("https://open.spotify.com/artist/0cDEwbwCuc3JlXS4nS1I8r?si=w1wEcyN5SEGnJZiSYjR4mw")
    
    def stop_music(self):
        pygame.mixer.pause()
        self.stop_start_music.configure(text="Play Music", command= self.start_music, image=self.play_image)

    def start_music(self):
        pygame.mixer.unpause()
        self.stop_start_music.configure(text="Stop Music", command= self.stop_music, image=self.stop_image)

    main_theme.play(-1)


if __name__ == "__main__":
    app = BgRemoverApp()
    
    app.mainloop()
