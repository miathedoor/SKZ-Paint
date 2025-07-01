"""
SKZ Paint
Mia Isidore
2024.11.06
ICS3U
-------------------
The Stray Kids-themed paint program that we didn't know we need is now here!

Run the program to find a help button that will help with navigating the program's functionalities.

SKZ Paint features:
- Paint brush tool
- Spray paint tool
- Eyedropper tool
- 8 stamps

- Highlighting of tool buttons when hovered and selected
- Help button
- Undo/redo

- Trash/clear screen button
- Fill screen button
- Mouse-canvas coordinates

"""

# Setup------------------------

from pygame import *
from random import *
from math import*
    
screen = display.set_mode((1000,600))
screen.fill(0)

display.set_caption("SKZ Paint")

RED = (197, 36, 58)
WHITE = (255, 255, 255)
GREY = (51, 51, 51)

# Canvas------------------------

draw.rect(screen, GREY, (0, 0, 1000, 97)) # header bar where stamps and logo are located

canvas_rect = Rect(144, 117, 782, 455) # canvas dimensions
draw.rect(screen, WHITE, canvas_rect) # drawing the canvas

# Tools-------------------------

# these are tools found on the left side of the program.

# I decided to use lists like this to perform repetitive tasks more efficiently.
# This also allows me to make changes to my layout extremely easily.
tools = ["upload", "download",
         "pencil", "eraser",
         "brush", "line",
         "spray", "eyedrop",
         "square", "circle",
         "square_fill", "circle_fill"]


tool = "pencil" # default tool
tool_images = [] # stores tool images

for t in tools:
    # I named my image files methodically so that the only difference between each
    # is handled by an f-string that changes based on the "t" in tools
    tool_images.append(image.load(f"images/buttons/button_{t}.png"))

    
tool_start = [0, 107] # starting coords [x, y] of the first tool's coordinates
tool_size = [52, 46] # uniform size [width, height] of all tools

tool_rects = [] # list that stores each tool's dimensions

for t in range(len(tools)):
    tool_rects.append(Rect(tool_start[0], tool_start[1], tool_size[0], tool_size[1]))
    
    if t%2 == 0:
        # notice how there are two columns of tools on the left side.
        # if the tool we're currently on is even, then we increase the x coord by the tool's width
        tool_start[0] += tool_size[0]
    else:
        # if the tool is odd, then we subtract the tool width from x so we're back to the edge of screen
        tool_start[0] -= tool_size[0]
        # we also change the y coord by the tool's height to move down.
        tool_start[1] += tool_size[1]


#Side Tools

# these tools appear on the right side of the screen.

side_tools = ["help", "trash", "bucket", "undo", "redo", "increase", "blank", "decrease"]
side_tool_images = []

for t in side_tools:
    side_tool_images.append(image.load(f"images/buttons/button_{t}.png"))

help_screen = image.load(f"images/help.png") # this is the screen that blits when the help button is clicked.

side_tool_start = [948, 107]
side_tool_size = [52, 46]

side_tool_rects = []

for t in range(len(side_tools)):
    side_tool_rects.append(Rect(side_tool_start[0], side_tool_start[1], side_tool_size[0], side_tool_size[1]))
    side_tool_start[1] += side_tool_size[1]
    if t != side_tools.index("undo") and t != side_tools.index("trash"): # I wanted undo and redo, and trash and bucket to be closer to each other since they are related functions.
        # but all other tools should have a little margin below to separate them.
        side_tool_start[1] += 10
    

#Blit all tool images
for t in range(len(tools)):
        screen.blit(tool_images[t], (tool_rects[t]))

for t in range(len(side_tools)):
        screen.blit(side_tool_images[t], (side_tool_rects[t]))
        

# Stamps-------------------------
# stamps are similar to how tools and side tools were set up.

stamps = ["Bang Chan", "Lee Know",
         "Changbin", "Hyunjin",
         "HAN", "Felix",
         "Seungmin", "I.N"]

stamp_images = []

logo_image = image.load(f"images/stamps/stamp_logo.png") # the "SKZ Paint" logo

for t in stamps:
    stamp_images.append(image.load(f"images/stamps/stamp_{t}.png"))
    

stamp_start = [0, 5]
stamp_size = [73, 95]

stamp_rects = []

logo_coord = []
logo_size = [261, 98]

for t in range(len(stamps)):
    stamp_rects.append(Rect(stamp_start[0], stamp_start[1], stamp_size[0], stamp_size[1]))
    
    if t == 3: # this is the fourth stamp. There needs to be space after the fourth stamp for the logo.
        logo_coord.append(logo_size[0] + 100) # only the x coordinate gets appended to the logo coord since
        #its y coord is equal to the stamps' y coord.
        # the logo's x coord is the width of the logo plus "padding" that separates it from the left-side stamps by 100.

        stamp_start[0] += logo_coord[0] + 100 # the fifth stamp starts after the logo and after separating itself from the logo by another 100.

    else:
        stamp_start[0] += stamp_size[0] # for all other stamps, it should only increase the x coord of the stamp by the stamp's uniform width.

for t in range(len(stamps)):
    screen.blit(stamp_images[t], (stamp_rects[t]))

# Logo
logo_rect = Rect(logo_coord[0], stamp_start[1], logo_size[0], logo_size[1]) # logo's y coord is same as other stamps
screen.blit(logo_image, (logo_rect)) # blitting logo image

# Colour---------------------

# following is for the colour spectrum and colour preview box under the tools on the left side.

eraser_colour = (WHITE) 

current_colour = (RED) # default colour
colour_rect = Rect(0, tool_start[1], tool_size[0]*2, 59) # rectangle that shows preview of current colour

spectrum = image.load(f"images/buttons/spectrum.png")
spectrum_rect = Rect(0, tool_start[1]+colour_rect[3], tool_size[0]*2, 158) # spectrum dimensions

screen.blit(spectrum, (spectrum_rect))
draw.rect(screen, 0, (spectrum_rect), 2) # a border around the spectrum to separate it from the colour preview rect.

# Text-----------------
font.init() 
size_font = font.SysFont("Comic Sans", 36) # text format for disaplying the brush size
coord_font = font.SysFont("Comic Sans", 12) # text format for the mouse-canvas coordinates.

# Download/upload---------------

from tkinter import *
from pygame import *
from tkinter import filedialog

root = Tk()             # this initializes the Tk engine
root.withdraw()         # by default the Tk root will show a little window. This just hides that window

#Undo/redo----------------------

past_activity = [] # this stores activity that has already happened
future_activity = [] # this stores activity that has been undone, but the user may want to retrieve by redoing.

past_activity.append(screen.subsurface(canvas_rect).copy()) # appends the inital white canvas screen to the undo list.
# this can't ever be undone since it's the default screen.

#Help------------------------------

helping = False # when helping is true, the help screen will be displayed. Else it will be hidden by "done", defined below.

done = screen.subsurface(canvas_rect).copy() # saves the image that user was working on before they pressed the help button.
# so when they are done with viewing help, they don't lose their progress.

# Misc variables---------------------

size = 4 # size of tools such as pencil, eraser, brush, etc.

omx, omy = None, None # omx and omy keeps track of where the starting point of drawings like a line or rect is.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
           if e.button == 1:
               omx, omy = e.pos # retrieve the starting point when the user initially clicks.
               
               back = screen.subsurface(canvas_rect).copy()
               # 'back" keeps track of what the canvas looks like until the user releases the mouse and draws a line or rectangle etc.

               for t in range(len(side_tools)):
                   # the side tools are different from normal tools because side tools are "one click" tools
                   # you only need to click once to activate them.
                   # normal tools stay activated until another normal tool is chosen since they have to
                   # be continuously activated to draw on the canvas.

                   # that's why side tools are under MOUSEBUTTONDOWN
                   #and normal tools are further below in a continous loop
                   
                   if side_tool_rects[t].collidepoint(mx, my) and helping == False:
                       if side_tools[t] == "trash": 
                           draw.rect(screen, WHITE, canvas_rect) # clear the screen
                       elif side_tools[t] == "bucket":
                           draw.rect(screen, current_colour, canvas_rect)
                           eraser_colour = current_colour # changes the eraser colour so that the back ground doesn't get erased no matter its colour.
                           
                       elif side_tools[t] == "increase":
                           size += 1 # increase brush size
                           
                       elif side_tools[t] == "decrease":
                           size -= 1
                           if size <= 0:
                               size = 1 # the user unfortunately can't have a negative brush size.
                               
                       elif side_tools[t] == "undo" and len(past_activity) > 1: # past_activity has to be greater than 1 so that we don't undo the original white canvas.
                           
                               activity = past_activity.pop() # the past_activity list gets user user drawings appended to under MOUSEBUTTONUP, found below.
                               # whenever the user releases the mouse on the canvas, that latest modification by the user gets appended to past_activity.
                               future_activity.append(activity)  # that activity gets appended to the future list in case the user wants to redo it.

                               # The below code effectively "undoes" the latest action by displaying
                               #the state of the canvas before the user's most recent modification.
                               
                               screen.blit(past_activity[-1], (canvas_rect)) # blits the latest acitivty in past_activity.
                               # [-1] is blitted back instead of the activity we just popped because that activity is not what we want to blit, but the one before.
                               # Example, the user just finished drawing, but made a mistake they want to undo. We pop off what the user just drew as a mistake,
                               #then we blit back whatever was before that, which is what the user wants.
                               
                       elif side_tools[t] == "redo" and len(future_activity) > 0:
                           activity = future_activity.pop() # removes the latest item from future_activity, which was previously undone
                           past_activity.append(activity) # adds that activity back into past_activity, essentialy restoring it as the latest modification the user made.
                           screen.blit(past_activity[-1], (canvas_rect)) # redos the last undone action and restores the canvas state to how it looked before the undo.

            # the help tool is the only exception to the "one click" concept among side tools since the help screen needs to be kept open until the user decides they are finished.
            # that's why the following code for help is outside the loop of the other side tools.
           if side_tool_rects[side_tools.index("help")].collidepoint(mx, my):
                       helping = not helping # if helping is true, then helping is switched to false.
                       # if helping was flase, then it is switched to true.

                       if helping:
                            done = screen.subsurface(canvas_rect).copy() # we need to keep track of what their canvas looked like before they opened help.
                            screen.blit(help_screen, (canvas_rect)) # then we blit the help screen.
                       elif helping == False: 
                            screen.blit(done, (canvas_rect)) # once the user is finished with help, blit back what the canvas looked like before
                            
           for s in range(len(stamps)): 
                if stamp_rects[s].collidepoint(mx, my):
                    current_stamp = stamp_images[s] # the current stamp becomes the stamp corresponding to the clicked rect.
                    tool = "stamp"
 
           if e.button == 4: # UP
               size += 1 # change the brush size by scrolling the mouse wheel
           if e.button == 5: # DOWN
                size -= 1
           if size <= 0:
                size = 1
                
        if e.type == MOUSEBUTTONUP:
            if e.button == 1:
                omx, omy = None, None # once the mouse is released, there is no old mx/my present.

                for t in range(len(tools)):
                    if tool_rects[t].collidepoint(mx,my) and tool_rects[tools.index("upload")].collidepoint(mx, my) == False and tool_rects[tools.index("download")].collidepoint(mx, my) == False: 
                        tool = tools[t] # changes tool based on corresponding tool rect clicked.

                        # the above if statement excludes upload/download because they are "one click" tools.
                        
                    elif spectrum_rect.collidepoint(mx, my):
                        current_colour = screen.get_at((mx,my)) # change the colour based on where the mouse clicks the colour spectrum

                if canvas_rect.collidepoint(mx, my) or side_tool_rects[side_tools.index("bucket")].collidepoint(mx, my) or side_tool_rects[side_tools.index("trash")].collidepoint(mx, my):
                    # I check if the trash or bucket tool is used because it is a modification that needs to be appended to the past activity list below:
                    # every event after the user releases the mouse is appended to the past activity list for the undo functionality.
                    past_activity.append(screen.subsurface(canvas_rect).copy())
                    
                    future_activity = [] # future activity is cleared every time something new is drawn to prevent storing every event.
                    # because then when redo is clicked the list would be filled with things that were undone from a while ago.

                elif tool_rects[tools.index("upload")].collidepoint(mx, my): # this line is checking if the user clicked the upload button.
                    # because if I instead had "if tool == upload"; the following code would keep asking the user to open a file over and over.
                    
                    file_name = filedialog.askopenfilename(filetypes = [("Picture files", "*.png;*.jpg")])
                    if file_name: # only if the user actually selected a file:
                        screen.set_clip(canvas_rect) # clip prevents the image from jutting out of the canvas
                        file_image = image.load(file_name)
                        screen.blit(file_image, (canvas_rect))
                        screen.set_clip(None)
                        
                elif tool_rects[tools.index("download")].collidepoint(mx, my):
                    file_name = filedialog.asksaveasfilename()
                    if file_name:
                        current_drawing = screen.subsurface(canvas_rect)
                        image.save(current_drawing, file_name)

    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()

    #Draw layout------------------

    blank = side_tools.index("blank") # in the side tool list, there's a spot for a "blank" space that's just a black box.
    # the size text is displayed on top of this blank box.
    
    # so I only have to redraw the blank box instead of the whole program layout when the size changes:
    screen.blit(side_tool_images[blank], side_tool_rects[blank]) # redraw blank box
    size_image = size_font.render(f"{size:02}", True, (WHITE))
    screen.blit(size_image,(side_tool_rects[blank]))

    # displaying mouse-canvas coordinates
    if canvas_rect.collidepoint(mx, my): 
        coords_coords = side_tool_start[0], side_tool_start[1] # the coordinates for where the mouse-canvas coordinates should be displayed, which is right under the side tools.
        screen.blit(side_tool_images[blank], (coords_coords))

        coordinates = coord_font.render(f"{mx-canvas_rect[0]},{ my-canvas_rect[1]}", True, (WHITE))
        screen.blit(coordinates, (coords_coords)) 
        
    for t in range(len(tools)):
        draw.rect(screen, 0, tool_rects[t], 2) # draws a black border around each tool.
        # makes layout look more aesthetic
        # and more importantly, it covers up the red highlight when the user switches tools.

        if tool_rects[t].collidepoint(mx, my): # if the user simply hovers over tools, white border.
            draw.rect(screen, WHITE, tool_rects[t], 2) 

        if tool == tools[t]:
            # this draws a red highlight that stays only around the current selected tool.
            draw.rect(screen, RED, tool_rects[t], 2)
                
 
        elif mb[0] and canvas_rect.collidepoint(mx, my) and helping == False: # if helping was true, the user would draw over the help screen.
            screen.set_clip(canvas_rect) # prevents from user drawing outside canvas

            if tool == "stamp":
                   current_stamp = transform.scale(current_stamp, (stamp_size[0]*2, stamp_size[1]*2))
                   # transforms the stamp to be twice its original size when stamping it on the canvas.
                   
                   screen.blit(back, canvas_rect)

                   cx = mx-current_stamp.get_width()//2 # cx and cy centers the stamp around the mouse
                   cy = my-current_stamp.get_height()//2 # it looks nicer than dragging it by the corner.
                   
                   screen.blit(current_stamp, (cx, cy))

            elif tool == "pencil":
                if size > 5: # automatically changes the pencil to brush because over size 5, the pencil doesn't draw nicely.
                    tool = "brush"
                if omx:
                    draw.line(screen, current_colour, (omx, omy), (mx, my), size)
                omx, omy = mx, my

                """
                The pencil line is drawn from the last recorded mouse position (omx, omy) to the current mouse position (mx, my).
                omx and omy  are set to mx and my at the end of each iteration of the main drawing loop to make it "follow" the mouse smoothly.
                """
 
            elif tool == "eraser" or tool == "brush": # eraser is a white brush
                if omx:
                    dx = mx - omx
                    dy = my - omy
                    distance = int(hypot(dx, dy) ) # distance between the old mousepoint and the current mousepoint

                    # below loop iterates for each unit of distance. Each i represents a step between (omx, omy) and (mx, my).
                    for i in range(distance):
                        progress = i / distance
                        """
                         i / distance produces a "progress" value between 0 and 1:
                        When i is 0, progress is 0, giving us (omx, omy) (the starting point).
                        As i increases, progress is close to 1, giving us a point closer to (mx, my) (the endpoint).
                        """
                        x = int(omx + dx * progress)
                        y = int(omy + dy * progress)
                        """
                        omx + dx * (i / distance) takes the initial x-position omx
                        and adds a fraction of dx (since dx was multiplied by the "progress" value), moving gradually from omx to mx
                        """

                        if tool == "eraser":
                            draw.circle(screen, eraser_colour, (x, y), size) # the eraser colour changes when the background is changed by the bucket tool.
                        elif tool == "brush":
                            draw.circle(screen, current_colour, (x, y), size)
                omx, omy = mx, my
                
            elif tool == "line":
                screen.blit(back, canvas_rect)
                draw.line(screen, current_colour, (omx, omy),(mx,my), size)
                    
            elif tool == "spray":
                off_x = randint(-size, size) # horizontal off set
                off_y = randint(-size, size) # vertical off set

                #randint(-size, size) generates random integers within the range [-size, size],
                #meaning the spray dots can appear up to size pixels away from the current mouse position in any direction.

                x = mx - (mx+off_x)
                y = my - (my+off_y)
                distance = hypot(x, y)
                #calculating distance helps determine if the randomly generated offset is within the spray radius (size).

                if distance < size: # only if the offset is within the spray radius:
                    draw.circle(screen, current_colour, (mx + off_x, my + off_y), 1)
                    
            elif tool == "eyedrop":
                current_colour = screen.get_at((mx,my)) 
                
            elif tool == "square" or tool == "square_fill" or tool == "circle" or tool == "circle_fill":
                # rects and ellipses have same code except the fact they are either rect or ellipse; or filled or unfilled.
                screen.blit(back, canvas_rect)

                w = mx - omx # the width of the shape is the distance from mx and omx
                h = my - omy
            
                current_rect = Rect(omx, omy, w,h)
                current_rect.normalize() # ensures that the shape can be drawn in any direction
                
                if tool == "square":
                    draw.rect(screen, current_colour, current_rect, size)
                elif tool == "square_fill":
                    draw.rect(screen, current_colour, current_rect)
                elif tool == "circle":
                    draw.ellipse(screen, current_colour, current_rect, size)
                elif tool == "circle_fill":
                    draw.ellipse(screen, current_colour, current_rect)
                
            screen.set_clip(None)
             
    draw.rect(screen, current_colour, (colour_rect)) # the current colour preview rect
    draw.rect(screen, 0, (colour_rect), 2) # a border around the rect

    for t in range(len(side_tools)):
        draw.rect(screen, 0, side_tool_rects[t], 2) # draws a black border around side tools.

        if side_tool_rects[t].collidepoint(mx, my) and t != side_tools.index("blank"):
            draw.rect(screen, WHITE, side_tool_rects[t], 2) # white border when user is hovering.
            # doesn't get drawn around the blank box that displays the size because it's not an actual tool.
            
    display.flip()
quit()
