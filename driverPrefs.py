from selenium import webdriver

def getPrefs():
    return ch_options

ch_options = webdriver.chrome.options.Options()

prefs = {
    'profile.default_content_setting_values.automatic_downloads': 1,
    "download.default_directory" : "/home/godys/Pictures/Unsplash"
    }

ch_options.add_experimental_option("prefs", prefs)