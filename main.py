from subprocess import run, CalledProcessError
import pystray
import PIL.Image

# dictionary of local power plans with their GUIDs
power_plans: dict[str: str] = {
    "Chill": "01886991-ed76-4326-b2ad-3cd3c74446cd",
    "Performance": "e1abddeb-7848-4424-8b48-d4e9e17b3634"
}

# load tray icon
image = PIL.Image.open("tray_icon.png")

# set the specified power plan
def set_power_plan(plan):
    try:
        run(['powercfg', '/setactive', power_plans[plan]], check=True)
    except subprocess.CalledProcessError as e:
        with open("error.log", "a") as log_file:
            log_file.write(f"Error setting power plan {plan}: {e}\n")

# menu items handler
def on_click(tray, item):
    match item.text:
        case "Chill":
            set_power_plan("Chill")
        case "Performance":
            set_power_plan("Performance")
        case "Quit":
            tray.stop()
            exit(0)

# menu setup
menu = pystray.Menu(
    pystray.MenuItem("Performance", on_click),
    pystray.MenuItem("Chill", on_click),
    pystray.MenuItem("Quit", on_click)
)

# create and run the tray icon
tray_icon = pystray.Icon("PowerPlan", image, menu = menu)
tray_icon.run()