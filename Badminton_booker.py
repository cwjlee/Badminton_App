# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 15:51:22 2021

@author: cwjle
"""


#Importing relevant modules
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import PySimpleGUI as sg

#Function to open user GUI and run up to the authentication
def pre_authentication():
    window = sg.Window(title="CWL Login", layout = [ 
        [sg.Text('Please enter your CWL username, password, and time')], 
        [sg.Text('username', size =(15, 1)), sg.InputText()], 
        [sg.Text('password', size =(15, 1)), sg.InputText()], 
        [sg.Text('time (hour in 24 hour format)', size =(15, 1)), sg.InputText()], 
        [sg.Text('time (minute)', size =(15, 1)), sg.InputText()], 
        [sg.Submit(), sg.Cancel()]])
    event, values = window.read()
    window.close()
    # Using Chrome to access web
    print("window closed")
    driver = webdriver.Chrome("C:/Users/cwjle/Desktop/PersonalWork/Python Practice/downloads_python/chromedriver.exe")
    # Open the website
    driver.get('https://ubc.perfectmind.com/24063/Clients/BookMe4BookingPages/Classes?calendarId=f14c6c16-b80d-48dd-be79-aa664d2346b4&widgetId=15f6af07-39c5-473e-b053-96653f77a406&embed=False')
    login = driver.find_element_by_class_name('pm-button')
    login.click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/sso/index.php"]'))).click()
    username = driver.find_element_by_id("username")
    username.send_keys(values[0])
    password = driver.find_element_by_id("password")
    password.send_keys(values[1])
    driver.find_element_by_class_name("ui-button").click()
    print("logged in")
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    time.sleep(2)
    push = driver.find_element_by_class_name("auth-button")
    push.click()
    print(push)
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@aria-label,'waitlist')]"))) #Waiting for page to load
    driver.refresh()
    output = [driver,values]
    return output

#Function to run after the authentication
def post_authentication(driver):
    print("second half called well")
    driver.refresh()
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@aria-label,'Register Now Badminton')]")))#Waiting for page to load
    buttons = driver.find_elements_by_xpath("//input[contains(@aria-label,'Register Now Badminton')]")
    i = len(buttons) - 1
    buttons[i].click()
    time.sleep(2)
    driver.find_element_by_class_name('bm-book-button').click() #click register
    driver.find_elements_by_class_name("bm-button")[1].click() #confirm attendees
    driver.find_elements_by_class_name("bm-button")[1].click() #confirm waiver
    time.sleep(2)
    driver.find_elements_by_class_name("holiday-radio-btn")[1].click()
    driver.find_element_by_xpath("//a[contains(@onclick,'Registration')]").click() #fees and extras
    driver.find_element_by_id("checkoutButton").click()
    time.sleep(2)
    #Troubleshoot looking for the final button
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    print("switched to Iframe")
    element = driver.find_element_by_xpath("//button[contains(text(), 'Place My Order')]")
    element.click()
    print("booking is done!",element)
    
#Timing the post_authentication function to run at the desired booking time for the same day
def timing_post_auth():
    hour_t = int(output[1][2])
    minute_t = int(output[1][3])
    x=datetime.today()
    y=x.replace(day=x.day, hour=hour_t, minute=minute_t, second=0, microsecond=0)
    delta_t=y-x
    secs=delta_t.seconds+1
    print("you have to wait : ",secs, " seconds.")
    time.sleep(secs)
    post_authentication(output[0])   
    
#Running code from above.
output = pre_authentication()

timing_post_auth() 










