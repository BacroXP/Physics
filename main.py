import customtkinter
import random
import math

# Variables
max_intensity = 2
minimal = 1e-99
speed = 50
is_running = True


def get_y_by_function(x: float) -> float:
    return max_intensity * math.pow(math.sin(x) / (minimal + x), 2) if x != 0 else max_intensity


def add_random_points() -> None:
    global is_running
    if is_running:
        for _ in range(speed):
            got = False
            while not got:
                x = random.randint(-674, 674)
                if random.random() <= get_y_by_function(x * 1e-1):
                    y = random.randint(0, 230)
                    screen_canvas.create_oval(674 + x - 1, y - 1, 674 + x + 1, y + 1, fill="lime", outline="lime")
                    got = True

        app.after(1000 // speed, add_random_points)


def start_generating() -> None:
    global is_running
    is_running = True
    add_random_points()


def draw_coordinate_system() -> None:
    canvas.delete("all")

    canvas.create_line(674, 0, 674, 230, fill="black", width=2)
    canvas.create_line(0, 230, 1348, 230, fill="black", width=2)

    for i in range(25, 1348, 50):
        canvas.create_line(i, 0, i, 230, fill="#DDDDDD")
    for j in range(28, 230, 50):
        canvas.create_line(0, j, 1348, j, fill="#DDDDDD")

    for x in range(-600, 601, 100):
        canvas.create_line(674 + x, 225, 674 + x, 235, fill="black")
        canvas.create_text(674 + x, 220, text=str(x // 100), font=("Arial", 10))

    for y in range(0, 201, 100):
        canvas.create_line(669, 229 - y, 679, 229 - y, fill="black")
        canvas.create_text(685, 229 - y, text=str(y//100), font=("Arial", 10))


def plot_function() -> None:
    canvas.delete("function")
    points = []

    for x in range(-600, 601):
        y = get_y_by_function(x * 1e-1)

        canvas_x = 674 + (x)
        canvas_y = 229 - (y * 100)
        canvas_y = max(0, canvas_y)

        points.append((canvas_x, canvas_y))

    for i in range(len(points) - 1):
        canvas.create_line(points[i], points[i + 1], fill="blue", width=2, tags="function")


def update_speed_label(value):
    global speed
    speed_label.configure(text=f"Speed: {int(value)}photons / s")
    speed = value


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    
    app = customtkinter.CTk()
    app.geometry("1200x600")
    app.wm_title("Interference Simulator")
    
    graph_display = customtkinter.CTkFrame(app, width=1100, height=250, fg_color="#8A9A5B")
    graph_display.place(x=50, y=25)
    
    graph_title = customtkinter.CTkTextbox(graph_display, width=200, height=30, fg_color="#8A9A5B", text_color="#C0C0C0",
                              font=("Aptos", 24), border_width=0)
    graph_title.insert("end", "Intensity Distribution")
    graph_title.place(x=5, y=5)
    graph_title.configure(state="disabled")
    
    canvas = customtkinter.CTkCanvas(graph_display, width=1348, height=230, bg="#FFFFFF")
    canvas.place(x=10, y=65)
    
    draw_coordinate_system()
    plot_function()
    
    screen_display = customtkinter.CTkFrame(app, width=1100, height=275, fg_color="#8A9A5B")
    screen_display.place(x=50, y=300)
    
    screen_title = customtkinter.CTkTextbox(screen_display, width=200, height=30, fg_color="#8A9A5B", text_color="#C0C0C0",
                               font=("Aptos", 24), border_width=0)
    screen_title.insert("end", "Screen")
    screen_title.place(x=5, y=5)
    screen_title.configure(state="disabled")
    
    speed_slider = customtkinter.CTkSlider(screen_display, from_=1, to=100, number_of_steps=99, width=300)
    speed_slider.place(x=250, y=242)
    
    speed_label = customtkinter.CTkLabel(screen_display, text="Speed: 50photons / s", text_color="#C0C0C0", font=("Arial", 20))
    speed_label.place(x=10, y=235)
    
    speed_slider.bind("<Motion>", lambda event: update_speed_label(speed_slider.get()))
    
    screen_canvas = customtkinter.CTkCanvas(screen_display, width=1348, height=220, bg="#000000")
    screen_canvas.place(x=10, y=65)
    
    start_generating()
    
    app.mainloop()
