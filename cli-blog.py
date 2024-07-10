import curses
from curses import wrapper

# Function to wrap text to fit within the given width
def wrap_text(text, width):
    words = text.split()
    wrapped_lines = []
    line = ""

    for word in words:
        if len(line) + len(word) + 1 > width:
            wrapped_lines.append(line)
            line = word
        else:
            if line:
                line += " "
            line += word

    if line:
        wrapped_lines.append(line)

    return wrapped_lines

# Function to print a blog post
def render_post(win, title, content):
    win.clear()

    # Print the title
    win.addstr(0, 2, title, curses.A_BOLD)
    win.hline(1, 1, curses.ACS_HLINE, win.getmaxyx()[1] - 2)

    # Get the width of the window for text wrapping
    width = win.getmaxyx()[1] - 4  # Adjust for padding inside the box

    # Wrap the content text to fit within the window width
    wrapped_content = wrap_text(content, width)

    # Print the wrapped content
    y = 3
    for line in wrapped_content:
        win.addstr(y, 2, line)
        y += 1

    # Draw a thin solid line at the bottom
    bottom_y = win.getmaxyx()[0] - 6
    win.hline(bottom_y, 1, curses.ACS_HLINE, win.getmaxyx()[1] - 2)

    # Define the shortcuts string and calculate its starting x position to center it
    shortcuts = "j/k: ↓/↑   bksp: back"
    start_x = (win.getmaxyx()[1] - len(shortcuts)) // 2

    # Print the shortcuts below the line, centered
    win.addstr(bottom_y + 1, start_x, shortcuts)

    win.refresh()

    while True:
        c = win.getch()
        if c == 127: # Backspace key
            break

# Function to print the menu
def print_menu(win, highlight, choices):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, -1)

    win.clear()
    arrow = "→"

    x = 2
    y = 0
    for i, choice in enumerate(choices):
        if highlight == i + 1:
            win.addstr(y, x, f"{arrow} ", curses.color_pair(1) | curses.A_BOLD)
            win.addstr(y, x + 2, f"{choice}", curses.color_pair(1) | curses.A_BOLD)
        else:
            win.addstr(y, x + 2, f"{choice}")
        y += 1

    # Draw a thin solid line at the bottom
    bottom_y = win.getmaxyx()[0] - 6
    win.hline(bottom_y, 1, curses.ACS_HLINE, win.getmaxyx()[1] - 2)

    # Define the shortcuts string and calculate its starting x position to center it
    shortcuts = "j/k: ↓/↑   enter: select   q: quit"
    start_x = (win.getmaxyx()[1] - len(shortcuts)) // 2

    # Print the shortcuts below the line, centered
    win.addstr(bottom_y + 1, start_x, shortcuts)

    win.refresh()

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    stdscr.refresh()
    stdscr.keypad(True)  # Enable arrow keys

    # Initialize colors if the terminal supports it
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()

    # Get the size of the terminal window
    term_height, term_width = stdscr.getmaxyx()

    # Set the fixed width for the content
    content_width = 70  # Example fixed width
    content_start_x = (term_width - content_width) // 2

    # Create a window for the menu with fixed width and centered
    win = curses.newwin(term_height - 2, content_width, 3, content_start_x)

    # Menu items
    choices = [
        "Welcome to Peter's Blog",
        "How to git",
        "Hi, Mom!"
    ]

    # Blog contents
    contents = [
        "Welcome to my blog! Here you'll find various posts about different topics I'm passionate about.",
        "Post 1 content goes here. This is where you can write the full details of the post.",
        "Post 2 content goes here. This is where you can write the full details of the post."
    ]

    nav_highlight = 1
    highlight = 1
    choice = 0

    while True:
        print_menu(win, highlight, choices)
        c = win.getch()
        if c == curses.KEY_UP or c == ord('k'):
            if highlight == 1:
                highlight = len(choices)
            else:
                highlight -= 1
        elif c == curses.KEY_DOWN or c == ord('j'):
            if highlight == len(choices):
                highlight = 1
            else:
                highlight += 1
        elif c == 10:  # Enter key
            choice = highlight
            render_post(win, choices[choice - 1], contents[choice - 1])
            # stdscr.refresh()
            # stdscr.getch()
            win.clear()
        elif c == ord('q'):
            break

if __name__ == "__main__":
    wrapper(main)
