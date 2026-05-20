from pypotedited.primitive.move import MovePlayer
import tkinter as tk
import itertools
import threading
import time
import os
import sys

import pypotedited as pe
from pypotedited.creatures import PoppyTorso
from pypotedited.primitive.move import MovePlayer


# Display configuration for headless systems
if os.environ.get('DISPLAY', '') == '':
    print('no display, using 0.0')
    os.environ['DISPLAY'] = ':0'


class EyeAnimation:
    """Handles the eye animation in Tkinter (main thread)"""
    
    def __init__(self, canvas_width=800, canvas_height=600):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.eye_radius = 100
        self.root = None
        self.canvas = None
        self.pulse = itertools.cycle(range(-2, 3))
        
    def setup_window(self):
        """Create the Tkinter window and canvas"""
        self.root = tk.Tk()
        self.root.title("EVE Gradient Eyes")
        self.root.geometry(f"{self.canvas_width}x{self.canvas_height}")
        
        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="black"
        )
        self.canvas.pack()
        
    def draw_gradient_eye(self, center_x, center_y, radius, color_start, color_end, layers=10):
        """Draw a single gradient eye"""
        r_start, g_start, b_start = color_start
        r_end, g_end, b_end = color_end
        
        for i in range(layers):
            ratio = i / layers
            r = int(r_start + (r_end - r_start) * ratio)
            g = int(g_start + (g_end - g_start) * ratio)
            b = int(b_start + (b_end - b_start) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            
            current_radius = radius * (1 - i / (layers * 2))
            self.canvas.create_oval(
                center_x - current_radius,
                center_y - current_radius,
                center_x + current_radius,
                center_y + current_radius,
                fill=color,
                outline="",
                tags="eye"
            )
    
    def draw_eyes(self, offset=0):
        """Draw both eyes with optional offset for pulsing effect"""
        self.canvas.delete("eye")
        
        eye_left_x = self.canvas_width * 0.3
        eye_left_y = self.canvas_height / 2.5
        eye_right_x = self.canvas_width * 0.7
        eye_right_y = self.canvas_height / 2.5
        
        radius = self.eye_radius + offset
        
        # Draw left eye
        self.draw_gradient_eye(
            eye_left_x,
            eye_left_y,
            radius,
            (30, 144, 255),  # Dodger blue
            (0, 0, 0),        # Black
            layers=50
        )
        
        # Draw right eye
        self.draw_gradient_eye(
            eye_right_x,
            eye_right_y,
            radius,
            (30, 144, 255),
            (0, 0, 0),
            layers=50
        )
    
    def animate_eyes(self):
        """Animation loop for pulsing eyes - called from main thread via after()"""
        try:
            offset = next(self.pulse)
            self.draw_eyes(offset=offset)
            # Schedule next animation frame
            self.root.after(100, self.animate_eyes)
        except tk.TclError:
            # Window was closed
            pass
        except Exception as e:
            print(f"Error in eye animation: {e}")
    
    def start(self):
        """Initialize and start the eye animation"""
        self.setup_window()
        self.draw_eyes()  # Draw initial eyes
        self.root.after(100, self.animate_eyes)  # Schedule animation
        print("Eye animation started in main thread")
    
    def update(self):
        """Update the Tkinter window"""
        try:
            self.root.update()
        except tk.TclError:
            pass
    
    def stop(self):
        """Stop the animation and close the window"""
        if self.root:
            try:
                self.root.quit()
            except:
                pass


def robot_movement_thread(eyes):
    """Run robot movement in a separate thread"""
    try:
        # Get current working directory and set up file path
        base_path = os.getcwd()
        file_path = os.path.join(base_path, "custom3.move")
        
        # Initialize robot if not already done
        if "poppy" not in globals():
            print("Initializing robot...")
            poppy = pe.creatures.PoppyTorso(camera="dummy", scene="keep-existing")
            print("Robot initialized")
        else:
            print("Robot already initialized")
        
        # Make all motors compliant
        for m in poppy.motors:
            m.compliant = True
        print("All motors set to compliant")
        
        # Wait 10 seconds before movement
        print("Waiting 10 seconds before movement...")
        time.sleep(10)
        
        # Play movement file
        print("Starting movement...")
        player = MovePlayer(poppy, move_filename=file_path, omit_motors=['head_y'])
        player.start()
        player.wait_to_stop()
        print("Movement completed")
        
        # Small delay
        time.sleep(1)
        
        # Make motors compliant at the end
        for m in poppy.motors:
            m.compliant = True
        print("All motors set to compliant")
        print("Hello World")
        
    except Exception as e:
        print(f"Error in robot movement: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main function - runs Tkinter in main thread with robot in background"""
    
    # Create eye animation
    eyes = EyeAnimation(canvas_width=800, canvas_height=600)
    eyes.start()
    
    # Start robot movement in background thread
    robot_thread = threading.Thread(target=robot_movement_thread, args=(eyes,), daemon=False)
    robot_thread.start()
    
    try:
        # Keep Tkinter running in main thread
        # This blocks until window is closed
        eyes.root.mainloop()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        eyes.stop()
        robot_thread.join(timeout=5)


if __name__ == "__main__":
    main()