from tkinter import Tk, Label, Button, filedialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Function to handle the button click event
def start_sending():
    # Config
    login_time = 30  # Time for login (in seconds)
    new_msg_time = 5  # Time for a new message (in seconds)
    send_msg_time = 5  # Time for sending a message (in seconds)
    country_code = 91  # Set your country code

    # Open browser with default link
    link = "https://web.whatsapp.com"
    driver.get(link)
    time.sleep(login_time)

    # Check if Notepad file is selected
    if notepad_path_label["text"] == "No Notepad file selected":
        print("Please select a Notepad file.")
        return

    # Check if Message file is selected
    if message_path_label["text"] == "No message file selected":
        print("Please select a message file.")
        return

    # Read the contents of the Notepad file
    with open(notepad_path_label["text"], "r") as file:
        numbers = file.readlines()

    # Read the contents of the Message file
    with open(message_path_label["text"], "r", encoding="utf-8") as file:
        msg = file.read()

    # Loop through the phone numbers
    for number in numbers:
        num = number.strip()  # Remove leading/trailing whitespace or newline characters

        # Construct the WhatsApp link
        link = f"https://web.whatsapp.com/send/?phone={country_code}{num}"
        driver.get(link)
        time.sleep(new_msg_time)

        # Attach image
        time.sleep(2)
        attach_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "._1OT67"))
        )
        attach_button.click()
        time.sleep(2)
        image_input = driver.find_element(By.CSS_SELECTOR, "._1CGek input")
        image_input.send_keys(
            image_path_label["text"]
        )  # Use the selected image path from the label
        time.sleep(2)

        # Enter message
        actions = ActionChains(driver)
        for line in msg.split("\n"):
            actions.send_keys(line)
            actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(send_msg_time)

    # Quit the driver
    driver.quit()


# Function to handle the image selection button click event
def select_image():
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.JPEG")])
    # Update the image path label with the selected image path
    image_path_label.config(text=image_path)


# Function to handle the Notepad selection button click event
def select_notepad():
    notepad_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    # Update the Notepad file path label with the selected file path
    notepad_path_label.config(text=notepad_path)


# Function to handle the Message selection button click event
def select_message():
    message_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    # Update the Message file path label with the selected file path
    message_path_label.config(text=message_path)


# Create the main window
window = Tk()
window.title("WhatsApp Bulk Messenger")
window.geometry("400x200")

# Create labels and buttons
image_path_label = Label(window, text="No image selected")
image_path_label.pack()

select_image_button = Button(window, text="Select Image", command=select_image)
select_image_button.pack()

notepad_path_label = Label(window, text="No Number file selected")
notepad_path_label.pack()

select_notepad_button = Button(
    window, text="Select Number File", command=select_notepad
)
select_notepad_button.pack()

message_path_label = Label(window, text="No message file selected")
message_path_label.pack()

select_message_button = Button(
    window, text="Select Message File", command=select_message
)
select_message_button.pack()

start_button = Button(window, text="Start Sending", command=start_sending)
start_button.pack()

# Create the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Start the main event loop
window.mainloop()
