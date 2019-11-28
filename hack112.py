# Imports
from tkinter import *
from cmu_112_graphics import *
from PIL import Image 
import math, copy, random
import time
from appJar import gui
from os.path import join as pjoin

from typing import Dict
from tkinter.constants import CURRENT
import requests
import json
import random



class Explorer(ModalApp):

    def appStarted(app):
        app.savedTripsMode = SavedTripsMode()
        app.mapMode = MapMode()
        app.makeTrip = MakeTripMode() 
        app.splashScreenMode = SplashScreenMode()
        app.setActiveMode(app.splashScreenMode)
        app.chosenCity = "0"

class MakeTripMode(Mode):
    def appStarted(mode):
        myCity = mode.app.chosenCity

        mode.term=None
        mode.location=myCity
        print(mode.location)
        mode.api_key=('1nweqqt7cW1WkFLU2aZvRm0FTCJknOkNHv5AkpV5zcbneTF6Olezxdw-pIIE0tP1'
            +'56lQE4MeqsTl52ao3dx6Ic9EiP01fjSd0SBuYqu0-tscRUii0hjkCvGNP_O-XXYx')
        headers = {'Authorization': 'Bearer %s' % mode.api_key}
        url='https://api.yelp.com/v3/businesses/search'
            # In the dictionary, term can take values like food, cafes or businesses like McDonalds
        params = {'term':mode.term,'location':mode.location}
            # Making a get request to the API
        mode.req=requests.get(url, params=params, headers=headers)
            # proceed only if the status code is 200
            #print('The status code is {}'.format(req.status_code))
            # printing the text from the response 
        mode.parsed=json.loads(mode.req.text)
            #print(json.dumps(parsed, indent=4))
        mode.businesses = mode.parsed["businesses"]

        mode.bfastName = mode.searchFood('breafast and brunch', mode.location)[0]
        mode.bfastType = mode.searchFood('breafast and brunch', mode.location)[1]
        mode.bfastRating = mode.searchFood('breafast and brunch', mode.location)[2]
        mode.bfastAddress = mode.searchFood('breafast and brunch', mode.location)[3]
        mode.bfastPhone = mode.searchFood('breafast and brunch', mode.location)[4]
        mode.bfastLink =mode.searchFood('breafast and brunch', mode.location)[5]

        mode.lunchName = mode.searchFood('Lunch', mode.location)[0]
        mode.lunchType = mode.searchFood('Lunch', mode.location)[1]
        mode.lunchRating = mode.searchFood('Lunch', mode.location)[2]
        mode.lunchAddress = mode.searchFood('Lunch', mode.location)[3]
        mode.lunchPhone = mode.searchFood('Lunch', mode.location)[4]
        mode.lunchLink =mode.searchFood('Lunch', mode.location)[5]

        mode.dinnerName = mode.searchFood('Dinner', mode.location)[0]
        mode.dinnerType = mode.searchFood('Dinner', mode.location)[1]
        mode.dinnerRating = mode.searchFood('Dinner', mode.location)[2]
        mode.dinnerAddress = mode.searchFood('Dinner', mode.location)[3]
        mode.dinnerPhone = mode.searchFood('Dinner', mode.location)[4]
        mode.dinnerLink =mode.searchFood('Dinner', mode.location)[5]

        mode.thingName = mode.searchThingsToDo(mode.location)[0]
        mode.thingType = mode.searchThingsToDo(mode.location)[1]
        mode.thingRating = mode.searchThingsToDo(mode.location)[2]
        mode.thingAddress = mode.searchThingsToDo(mode.location)[3]
        mode.thingPhone = mode.searchThingsToDo(mode.location)[4]
        mode.thingLink = mode.searchThingsToDo(mode.location)[5]

# To learn how to make the yelp apis we used the following site:
#https://python.gotrained.com/yelp-fusion-api-tutorial/#Generate_Yelp_API_Key

    def searchThingsToDo(mode, myLocation):
        mode.term = 'things to do'
        location=myLocation
        goodBusinesses=[]
        theBusiness=[]
        headers = {'Authorization': 'Bearer %s' % mode.api_key}

        params = {'term':mode.term,'location':location}
        url='https://api.yelp.com/v3/businesses/search'

        mode.req=requests.get(url, params=params, headers=headers)

        mode.parsed=json.loads(mode.req.text)
        mode.businesses = mode.parsed["businesses"]
        for business in mode.businesses:
            if business["rating"]>=4.5:
                goodBusinesses.append(business)
        business=random.choice(goodBusinesses)
        try:
            name = business["name"]
        except:
            name = "No name given"
        theBusiness.append(name)
        try:
            businessType = business["categories"][0]["alias"]
        except:
            businessType = "No food type given"
        theBusiness.append(businessType)
        try:
            rating = business["rating"]
        except:
            rating = "No rating given"
        theBusiness.append(rating)
        try:
            address = " ".join(business["location"]["display_address"])
        except:
            address = "No address given"
        theBusiness.append(address)
        try:
            phone = business["phone"]
        except:
            phone = "No phone given"
        theBusiness.append(phone)
        try:
            link = business["url"]
        except:
            link = "No link given"   
        theBusiness.append(link)
        return theBusiness

# To learn how to make the yelp apis we used the following site:
#https://python.gotrained.com/yelp-fusion-api-tutorial/#Generate_Yelp_API_Key

    def searchFood(mode,myTerm,myLocation):
        mode.term=myTerm
        mode.location=myLocation
        goodRestaurants=[]
        for business in mode.businesses:
            if business["rating"]>=4.5:
                goodRestaurants.append(business)
        business=random.choice(goodRestaurants)
        theRestaurant=[]
        try:
            name = business["name"]
        except:
            name = "No name given"
        theRestaurant.append(name)
        try:
            foodType = business["categories"][0]["title"]
        except:
            foodType = "No food type given"
        theRestaurant.append(foodType)
        try:
            rating = business["rating"]
        except:
            rating = "No rating given"
        theRestaurant.append(rating)
        try:
            address = " ".join(business["location"]["display_address"])
        except:
            address = "No address given"
        theRestaurant.append(address)
        try:
            phone = business["phone"]
        except:
            phone = "No phone given"
        theRestaurant.append(phone)
        try:
            link = business["url"]
        except:
            link = "No link given"  
        theRestaurant.append(link)
        return theRestaurant 

    def mousePressed(mode,event):
        clickX = event.x
        clickY = event.y

        xTrue = (clickX > 648) and (clickX < 719)
        yTrue = (clickY > 615) and (clickY < 646)

        homeX = (clickX > 19) and (clickX < 88)
        homeY = (clickY > 26) and (clickY < 49)

        breakfast = "pancake"
        lunch = "sandwich"
        dinner = "soup"


        if homeX and homeY:
            mode.app.setActiveMode(mode.app.splashScreenMode)

        if xTrue and yTrue:
            fileName = simpledialog.askstring("Input", "Enter a file name: ")



            cwd = os.getcwd()
            path_to_file = pjoin(cwd, "mySavedTrips", fileName)

            f = open(path_to_file, "w")
            f.write("Breakfast")
            f.write("\tName " + mode.bfastName)
            f.write("\n")
            f.write("\tType " + mode.bfastType)
            f.write("\n")
            f.write("\tRating " + str(mode.bfastRating))
            f.write("\n")
            f.write("\tAddress " + mode.bfastAddress)
            f.write("\n")
            f.write("\tPhone " + mode.bfastPhone)
            f.write("\n")
            f.write("\tLink " + mode.bfastLink)
            f.write("\n")
            f.write("\n")
            f.write("Lunch")
            f.write("\tName " + mode.lunchName)
            f.write("\n")
            f.write("\tType " + mode.lunchType)
            f.write("\n")
            f.write("\tRating " + str(mode.lunchRating))
            f.write("\n")
            f.write("\tAddress " + mode.lunchAddress)
            f.write("\n")
            f.write("\tPhone " + mode.lunchPhone)
            f.write("\n")
            f.write("\tLink " + mode.lunchLink)
            f.write("\n")
            f.write("\n")
            f.write("Dinner")
            f.write("\tName " + mode.dinnerName)
            f.write("\n")
            f.write("\tType " + mode.dinnerType)
            f.write("\n")
            f.write("\tRating " + str(mode.dinnerRating))
            f.write("\n")
            f.write("\tAddress " + mode.dinnerAddress)
            f.write("\n")
            f.write("\tPhone " + mode.dinnerPhone)
            f.write("\n")
            f.write("\tLink " + mode.dinnerLink)
            f.close()

    def redrawAll(mode, canvas):
        text = "Itinerary"
        canvas.create_text(mode.app.width//2, 60, text = text, font = "Arial 40 bold underline")
        canvas.create_text(40, 120, text = "Breakfast: ", font = "Arial 26 bold", anchor = W)
        canvas.create_text(40, 140, text = "\tName: " + mode.bfastName, font = "Arial 15", anchor = W)
        canvas.create_text(40, 155, text = "\tFood Type: " + mode.bfastType, font = "Arial 15", anchor = W)
        canvas.create_text(40, 170, text = "\tRating: " + str(mode.bfastRating), font = "Arial 15", anchor = W)
        canvas.create_text(40, 185, text = "\tAddress: " + mode.bfastAddress, font = "Arial 15", anchor = W)
        canvas.create_text(40, 200, text = "\tPhone: " + mode.bfastPhone, font = "Arial 15", anchor = W)
        canvas.create_text(40, 215, text = "\tLink: " + mode.bfastLink, font = "Arial 15", anchor = W)

        canvas.create_text(40, 240, text = "Lunch: ", font = "Arial 26 bold", anchor = W)
        canvas.create_text(40, 255, text = "\tName: " + mode.lunchName, font = "Arial 15", anchor = W)
        canvas.create_text(40, 270, text = "\tFood Type: " + mode.lunchType, font = "Arial 15", anchor = W)
        canvas.create_text(40, 285, text = "\tRating: " + str(mode.lunchRating), font = "Arial 15", anchor = W)
        canvas.create_text(40, 300, text = "\tAddress: " + mode.lunchAddress, font = "Arial 15", anchor = W)
        canvas.create_text(40, 315, text = "\tPhone: " + mode.lunchPhone, font = "Arial 15", anchor = W)
        canvas.create_text(40, 330, text = "\tLink: " + mode.lunchLink, font = "Arial 15", anchor = W)

        canvas.create_text(40, 360, text = "Dinner: ", font = "Arial 26 bold", anchor = W)
        canvas.create_text(40, 375, text = "\tName: " + mode.dinnerName, font = "Arial 15", anchor = W)
        canvas.create_text(40, 390, text = "\tFood Type: " + mode.dinnerType, font = "Arial 15", anchor = W)
        canvas.create_text(40, 405, text = "\tRating: " + str(mode.dinnerRating), font = "Arial 15", anchor = W)
        canvas.create_text(40, 420, text = "\tAddress: " + mode.dinnerAddress, font = "Arial 15", anchor = W)
        canvas.create_text(40, 435, text = "\tPhone: " + mode.dinnerPhone, font = "Arial 15", anchor = W)
        canvas.create_text(40, 450, text = "\tLink: " + mode.dinnerLink, font = "Arial 15", anchor = W)

        canvas.create_text(40, 480, text = "What to Explore: ", font = "Arial 26 bold", anchor = W)
        canvas.create_text(40,495, text="\tName: "+mode.thingName, font='Arial 15', anchor = W)
        canvas.create_text(40,510, text="\tType of business: "+mode.thingType, font='Arial 15', anchor = W)
        canvas.create_text(40,525, text="\tRating: "+ str(mode.thingRating), font='Arial 15', anchor = W)
        canvas.create_text(40,540, text="\tAddress: "+mode.thingAddress, font='Arial 15', anchor = W)
        canvas.create_text(40,555, text="\tPhone: "+mode.thingPhone, font='Arial 15', anchor = W)
        canvas.create_text(40,570, text="\tLink: "+mode.thingLink, font='Arial 15', anchor = W)


        #draw the save button
        canvas.create_rectangle(mode.app.width-150, mode.app.height-80,
                                mode.app.width-80, mode.app.height-50,
                                fill = "pink", outline = "black", width = 3)
        #draw the save button text
        canvas.create_text(mode.app.width-131,
                           mode.app.height-65, text = "Save",\
                           fill = "black", anchor = W, \
                           font = "Arial 14 bold")

        #draw the home button
        canvas.create_rectangle(20, 50, 90, 30, fill = "pink", outline = "black", width = 3)

        #draw the home button text
        canvas.create_text(36, 40, text = "Home", fill = "black", anchor = W, font = "Arial 14 bold")

class LimeDot(object):
    @staticmethod
    def rgbString(red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)
    def __init__(self,mode,x,y):
        self.mode = mode
        self.x = x
        self.y = y
        self.r = 3
        lime = LimeDot.rgbString(153,51,255)
        self.color = lime

    def draw(self,canvas):
        drawY = self.y - self.mode.scrollY
        canvas.create_oval(self.x - self.r , drawY - self.r,
                           self.x + self.r, drawY + self.r, \
                           fill = self.color)

class SplashScreenMode(Mode):
    def appStarted(mode):
        mode.green = LimeDot.rgbString(153,51,255)
        logoUrl = "https://i.imgur.com/Rn3hPSI.png"
        mode.logoRaw = mode.loadImage(logoUrl)
        mode.logo = mode.scaleImage(mode.logoRaw, 5/4)
        mode.scrollY = 0
        mode.screenDots = []
        for i in range(100):
            x = random.randint(0,mode.app.width)
            y = random.randint(0,mode.app.height*3)
            dot = LimeDot(mode,x,y)
            mode.screenDots.append(dot)
    
    def timerFired(mode):
        mode.scrollY += 5
    
    def redrawAll(mode,canvas):
        # to draw the background black
        canvas.create_rectangle(0,0,mode.app.width,mode.app.height,\
                                fill = "black")
        # to draw the two rectanglar menu
        canvas.create_text(mode.app.width/2, mode.height/2+30,
                           text = "Explore any city, with a purpose.",
                           fill = "blue", font = "Arial 20")
        canvas.create_rectangle(mode.app.width/2-100,mode.height/2+100,
                                mode.app.width/2+100,mode.height/2+150,
                                fill = mode.green)
        canvas.create_text(mode.app.width/2,mode.height/2+125, text = "New Trip",\
                        fill = "white")
        canvas.create_rectangle(mode.app.width/2-100,mode.height/2+200,\
                                mode.app.width/2+100,mode.height/2+250,\
                                    fill = mode.green)
        canvas.create_text(mode.app.width/2,mode.height/2+225,\
                           text = "Saved Trips", fill = "white")

        # to draw dots on the screen and i want it to be floating
        for dot in mode.screenDots:
            dot.draw(canvas)

        # to draw the logo
        canvas.create_image(mode.app.width//2, mode.app.height//3,\
                            image=ImageTk.PhotoImage(mode.logo))

    def mousePressed(mode, event):
        clickX = event.x
        clickY = event.y

        newTripX = (clickX > 301) and (clickX < 500)
        newTripY = (clickY > 452) and (clickY < 501)

        savedTripX = (clickX > 301) and (clickX < 500)
        savedTripY = (clickY > 544) and (clickY < 596)

        if newTripX and newTripY:
            mode.app.setActiveMode(mode.app.mapMode)

        elif savedTripX and savedTripY:
            mode.app.setActiveMode(mode.app.savedTripsMode)

class CityDots(object):
    def __init__(self, mode, cityX, cityY, cityName):
        self.mode = mode
        self.appWidth = self.mode.app.width
        self.appHeight = self.mode.app.height
        self.cityName = cityName
        self.cityX = cityX
        self.cityY = cityY
        self.color = "black"
        self.circleR = 4
        self.chosen = False
        self.hovering = False

    def selected(self):
        self.chosen = True

    def draw(self, canvas):
        if self.hovering:
            self.color = "blue"
        else:
            self.color = "black"
        canvas.create_text(self.cityX + 5, self.cityY, text = self.cityName, fill = self.color, anchor = W, font = "Arial 14 bold")
        canvas.create_oval(self.cityX - self.circleR, self.cityY - self.circleR, 
           self.cityX + self.circleR, self.cityY + self.circleR, fill = self.color)
           

class MapMode(Mode):

    def appStarted(mode):
        mapUrl = "https://i.imgur.com/FjsPpN5.png"
        imageRatio = 7/8
        unScaledMap = mode.loadImage(mapUrl)
        mode.map = mode.scaleImage(unScaledMap, imageRatio)
        mode.cities = []

        #draw LA
        lADot = CityDots(mode, 66, 387, "Los Angeles")
        mode.cities.append(lADot)

        #draw Orlando
        orlandoDot = CityDots(mode, 643, 534, "Orlando")
        mode.cities.append(orlandoDot)

        #draw Nashville
        nashvilleDot = CityDots(mode, 538, 395, "Nashville")
        mode.cities.append(nashvilleDot)

        #draw Phoenix
        phoenixDot = CityDots(mode, 169, 426, "Phoenix")
        mode.cities.append(phoenixDot)

        #draw San Francisco
        sanFranDot = CityDots(mode, 24, 313, "San Francisco")
        mode.cities.append(sanFranDot)

        #draw Las Vegas
        vegasDot = CityDots(mode, 118, 354, "Las Vegas")
        mode.cities.append(vegasDot)

        #draw Pittsburgh
        pittsburghDot = CityDots(mode, 631, 292, "Pittsburgh")
        mode.cities.append(pittsburghDot)

        #draw Philadelphia
        # philadelphiaDot = CityDots(mode, 169, 426, "Philadelphia")
        # mode.cities.append(philadelphiaDot)

        #draw Atlanta
        atlantaDot = CityDots(mode, 585, 429, "Atlanta")
        mode.cities.append(atlantaDot)

        #draw Chicago
        chicagoDot = CityDots(mode, 517, 280, "Chicago")
        mode.cities.append(chicagoDot)

        #draw Boston
        bostonDot = CityDots(mode, 745, 228, "Boston")
        mode.cities.append(bostonDot)

        #draw NY City
        nyCityDot = CityDots(mode, 718, 262, "NY City")
        mode.cities.append(nyCityDot)

        #draw Austin
        austinDot = CityDots(mode, 369, 507, "Austin")
        mode.cities.append(austinDot)

        #draw Seattle
        seattleDot = CityDots(mode, 71, 127, "Seattle")
        mode.cities.append(seattleDot)

        #draw Portland
        portlandDot = CityDots(mode, 55, 167, "Portland")
        mode.cities.append(portlandDot)

        #draw Charleston
        charlestonDot = CityDots(mode, 649, 429, "Charleston")
        mode.cities.append(charlestonDot)

        #draw Washington D.C
        dcDot = CityDots(mode, 679, 311, "Washington D.C")
        mode.cities.append(dcDot)
         
        #draw New Orleans
        orleansDot = CityDots(mode, 506, 502, "New Orleans")
        mode.cities.append(orleansDot)

        #draw St. Louis
        stlouisDot = CityDots(mode, 489, 338, "St. Louis")
        mode.cities.append(stlouisDot)

        #draw Salt Lake City
        saltLakeCityDot = CityDots(mode, 175, 289, "Salt Lake City")
        mode.cities.append(saltLakeCityDot)
        
        # Draw Denver
        denverDot = CityDots(mode, 282, 315, "Denver")
        mode.cities.append(denverDot)
         
        #draw Oklahoma City
        oklahomaCityDot = CityDots(mode, 385, 389, "Oklahoma City")
        mode.cities.append(oklahomaCityDot)

    def keyPressed(mode, event):
        
        #if the user presses h seitch to the instruction page
        if (event.key == 'h'):
            mode.app.setActiveMode(mode.app.savedTripsMode)
        
    def mousePressed(mode, event):
        clickX, clickY = event.x, event.y
        boundsY = 15
        boundsX = 45
        for city in mode.cities:
            checkX = (clickX > city.cityX) and (clickX  < city.cityX + boundsX)
            checkY = (clickY > city.cityY - boundsY) and (clickY  < city.cityY + boundsY)
            
            if checkX and checkY:
                city.selected()
                mode.app.chosenCity = city.cityName
                mode.location = mode.app.chosenCity
                print(mode.app.chosenCity)
                mode.app.setActiveMode(mode.app.makeTrip)

        homeX = (clickX > 19) and (clickX < 88)
        homeY = (clickY > 26) and (clickY < 49)

        if homeX and homeY:
            mode.app.setActiveMode(mode.app.splashScreenMode)

    def mouseMoved(mode, event):
        clickX, clickY = event.x, event.y
        boundsY = 15
        boundsX = 45
        for city in mode.cities:
            checkX = (clickX > city.cityX) and (clickX  < city.cityX + boundsX)
            checkY = (clickY > city.cityY - boundsY) and (clickY  < city.cityY + boundsY)
            
            if checkX and checkY:
                city.hovering = True
            else:
                city.hovering = False

    def redrawAll(mode, canvas):
        #draw the map
        canvas.create_image(mode.width//2, mode.height//2, image=ImageTk.PhotoImage(mode.map))

        #draw the home button
        canvas.create_rectangle(20, 50, 90, 30, fill = "pink", outline = "black", width = 3)

        #draw the home button text
        canvas.create_text(36, 40, text = "Home", fill = "black", anchor = W, font = "Arial 14 bold")

        #draw each city on the map
        for city in mode.cities:
            city.draw(canvas)

class SavedTripsMode(Mode):

    def redrawAll(mode, canvas):
        #draw the home button
        canvas.create_rectangle(20, 50, 90, 30, fill = "pink", outline = "black", width = 3)

        #draw the home button text
        canvas.create_text(36, 40, text = "Home", fill = "black", anchor = W, font = "Arial 14 bold")
        cwd = os.getcwd()
        path_to_file = pjoin(cwd, "mySavedTrips")
        numFiles =  len([name for name in os.listdir(path_to_file) if os.path.isfile(os.path.join(path_to_file, name))]) - 1


        canvas.create_text(mode.width//2, mode.height//2, text =  "You have made " + str(numFiles) + " trips!", font = "Arial 26 bold")
        canvas.create_text(mode.width//2, mode.height//2 + 80, text =  "(To access your trips go to your completedTrips folder)", font = "Arial 20")

    def mousePressed(mode, event):
        clickX, clickY = event.x, event.y

        homeX = (clickX > 19) and (clickX < 88)
        homeY = (clickY > 26) and (clickY < 49)

        if homeX and homeY:
            mode.app.setActiveMode(mode.app.splashScreenMode)

def runExplorer():
    Explorer(width=800, height=700)

runExplorer()