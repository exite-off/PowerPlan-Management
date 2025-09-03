import subprocess
import pystray
import PIL.Image
from sys import exit as sys_exit
import re

# get available power plans from system
def get_power_plans() -> dict[str: str]:
    pattern = r'GUID:\s*([a-fA-F0-9-]+)\s*\(([^)]+)\)' # regex pattern to match GUID and plan name
    plans: dict[str: str] = {}
    result = subprocess.run(['powercfg', '-list'], capture_output=True, text=True)
    matches = re.findall(pattern, result.stdout)
    for match in matches:
        plans[match[1]] = match[0]
    return plans

# dictionary of local power plans with their GUIDs
power_plans: dict[str: str] = get_power_plans()

# load tray icon
image = PIL.Image.open("tray_icon.png")

# set the specified power plan
def set_power_plan(plan_name: str) -> None:
    try:
        subprocess.run(['powercfg', '/setactive', power_plans[plan_name]], check=True)
    except subprocess.CalledProcessError as e:
        with open("error.log", "a") as log_file:
            log_file.write(f"Error setting power plan {plan}: {e}\n")

# menu items handler
def on_click(tray, item):
    if item.text == "Quit":
        tray.stop()
    set_power_plan(item.text)

# generate menu items
menu_items = []

for plan, guid in power_plans.items():
    menu_items.append(pystray.MenuItem(plan, on_click))

menu_items.append(pystray.MenuItem("Quit", on_click))

# menu setup
menu = pystray.Menu(*menu_items)

# create and run the tray icon
tray_icon = pystray.Icon("PowerPlan", image, menu = menu)
tray_icon.run()