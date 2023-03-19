import Ticket
import User
import pygame
import pygame_gui

class MainMenu:

    def __init__(self):
        self.allUsers = []
        self.allTickets = []
        self.filteredTickets = []
        self.currentUser = None
        self.selectedTicket = None
        self.mode = "LOGIN"  #this variable will keep track of the current mode, and update the display accordingly.
        # starts off as "LOGIN", and can also hold values of "MAINMENU" or "ACCOUNT"
        self.errorMessage = None #when are error window is created, it will display this error message
        self.usersFile = open("users.txt", 'a+')  #opens users and tickets files
        self.ticketsFile = open("tickets.txt", "a+")

        self.readUsersFile()
        self.readTicketsFile()
        self.filteredTickets = self.allTickets

        self.create()

    def create(self):
        pygame.init()

        #GUI manager and text input fields
        manager = pygame_gui.UIManager((700,500))
        UI_REFRESH_RATE = pygame.time.Clock().tick(60)/5000  #sets the rate at which the GUI will refresh
        self.usernameInput = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((300, 125), (200, 35)), manager=manager, object_id = "#usernameInput")
        self.passwordInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((300, 200), (200, 35)), manager=manager, object_id="#passwordInput")
        self.creditCardInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((250, 150), (200, 35)), manager=manager, object_id="#creditCardInput")
        self.loadMoneyInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((250, 225), (200, 35)), manager=manager, object_id="#loadMoneyInput")

        self.creditCardInput.visible = False
        self.loadMoneyInput.visible = False

        size = (700, 500)
        screen = pygame.display.set_mode(size)

        running = True
        while running:
            self.updateDisplay(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()  #gets coordinates of click
                    self.buttonPressed(mx,my)  #calls function to check which button was pressed, and what needs to be done

                if self.mode == "LOGIN":
                    if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#usernameInput":  #check if enter is pressed when typing username/password, and if so tries to log in
                        self.login(self.usernameInput.get_text(),self.passwordInput.get_text())
                        self.usernameInput.clear()
                        self.passwordInput.clear()
                    elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#passwordInput":
                        self.login(self.usernameInput.get_text(), self.passwordInput.get_text())
                        self.usernameInput.clear()
                        self.passwordInput.clear()

                manager.process_events(event)

            manager.update(UI_REFRESH_RATE)
            manager.draw_ui(screen)  #updates gui components (text input field)

            pygame.display.flip()  #updates visuals

        pygame.quit()
        self.ticketsFile.close()
        self.usersFile.close()


    def updateDisplay(self, window):
        if self.mode == "LOGIN":
            self.drawLoginWindow(window)

        elif self.mode == "MAINMENU":
            self.drawMainMenu(window)

        elif self.mode == "ACCOUNT":
            self.drawAccountWindow(window)


    def drawMainMenu(self, window):    #main menu visuals go here
        self.usernameInput.visible = False
        self.passwordInput.visible = False
        self.creditCardInput.visible = False
        self.loadMoneyInput.visible = False

        pygame.draw.rect(window, (215, 215, 225), (0, 0, 700, 100))    #draws upper background
        pygame.draw.rect(window, (165, 215, 255), (0, 100, 700, 400))  #draws lower background

        pygame.draw.rect(window, (100, 150, 200), (100, 25, 75, 50), 250, 3)  #draws "add to cart" button
        pygame.draw.rect(window, (100, 150, 200), (200, 25, 75, 50), 250, 3)  #draws "sell ticket" button

        pygame.draw.rect(window, (100, 150, 200), (425, 25, 75, 50), 250, 3)  # draws "filter by price" button
        pygame.draw.rect(window, (100, 150, 200), (525, 25, 75, 50), 250, 3)  # draws "filter by artist" button

        pygame.draw.rect(window, (50, 150, 50), (312.5, 25, 75, 50), 250, 3)  # draws "Account" button

        font = pygame.font.Font('freesansbold.ttf', 10)
        slightlyBiggerFont = pygame.font.Font('freesansbold.ttf', 11)

        addToCartText = font.render("Add to Cart", True,(255, 255, 255))  # all the following code is for the text
        sellTicketText = font.render("Sell Ticket", True, (255, 255, 255))
        filterByPriceText = font.render("Filter by Price", True, (255, 255, 255))
        filterByArtistText = font.render("Filter by Artist", True, (255, 255, 255))
        accountText = font.render("Account", True, (255, 255, 255))

        addToCartTextRect = addToCartText.get_rect()
        sellTicketTextRect = sellTicketText.get_rect()
        filterByPriceTextRect = filterByPriceText.get_rect()
        filterByArtistTextRect = filterByArtistText.get_rect()
        accountTextRect = accountText.get_rect()

        addToCartTextRect.center = (137.5, 50)
        sellTicketTextRect.center = (237.5, 50)
        filterByPriceTextRect.center = (462.5, 50)
        filterByArtistTextRect.center = (562.5, 50)
        accountTextRect.center = (350, 50)

        window.blit(addToCartText, addToCartTextRect)
        window.blit(sellTicketText, sellTicketTextRect)
        window.blit(filterByPriceText, filterByPriceTextRect)
        window.blit(filterByArtistText, filterByArtistTextRect)
        window.blit(accountText, accountTextRect)


        if self.selectedTicket:   #if a ticket is selected, draws highlight around it. Note: must be done before drawing ticket rectangle to make it an outline
            y = (self.filteredTickets.index(self.selectedTicket) * 70) + 125
            pygame.draw.rect(window, (255,255,0), (95,y-5,510,45))

        x = 100
        y = 125
        for ticket in self.filteredTickets:   #draw box for each ticket
            pygame.draw.rect(window, (200, 0, 75), (x, y, 500, 35))

            ticketText = slightlyBiggerFont.render(str(ticket), True, (255, 255, 255))
            ticketTextRect = ticketText.get_rect()
            ticketTextRect.center = (x + 250, y + 17)
            window.blit(ticketText, ticketTextRect)

            y += 70

        if self.errorMessage != None:
            self.drawError(window)


    def drawLoginWindow(self, window):   #login window visuals go here
        self.usernameInput.visible = True  # sets text fields to visible
        self.passwordInput.visible = True

        pygame.draw.rect(window, (125, 225, 100), (0, 0, 700, 500))   #draws background

        pygame.draw.rect(window, (150, 50, 200), (150, 350, 130, 65), 250, 3)   #draws "Login" button
        pygame.draw.rect(window, (150, 50, 200), (425, 350, 130, 65), 250, 3)  # draws "Create Account" button

        font = pygame.font.Font('freesansbold.ttf', 15)

        loginText = font.render("Login", True, (255, 255, 255))  #all the following code in this function is for the text
        createAccountText = font.render("Create Account", True, (255, 255, 255))
        usernameText = font.render("Username", True,(100, 100, 100))
        passwordText = font.render("Password", True, (100, 100, 100))

        loginTextRect = loginText.get_rect()
        createAccountTextRect = createAccountText.get_rect()
        usernameTextRect = usernameText.get_rect()
        passwordTextRect = passwordText.get_rect()

        loginTextRect.center = (215, 382.5)
        createAccountTextRect.center = (490, 382.5)
        usernameTextRect.center = (250, 140)
        passwordTextRect.center = (250, 220)

        window.blit(loginText, loginTextRect)
        window.blit(createAccountText, createAccountTextRect)
        window.blit(usernameText, usernameTextRect)
        window.blit(passwordText, passwordTextRect)

        if self.errorMessage != None:
            self.usernameInput.visible = 0
            self.passwordInput.visible = 0
        else:
            self.usernameInput.visible = 1
            self.passwordInput.visible = 1

        if self.errorMessage != None:
            self.drawError(window)


    def drawAccountWindow(self, window):   #user account screen visuals

        self.usernameInput.visible = False # sets text fields to invisible
        self.passwordInput.visible = False
        self.creditCardInput.visible = True
        self.loadMoneyInput.visible = True

        pygame.draw.rect(window, (200, 200, 200), (0, 0, 700, 500))  #draws background

        pygame.draw.rect(window, (50, 150, 50), (300, 25, 100, 50), 250, 3)  #draws "main menu" button

        pygame.draw.rect(window, (50, 150, 50), (460, 152.5, 75, 30))  # draws "confirm credit card" button
        pygame.draw.rect(window, (50, 150, 50), (460, 227.5, 75, 30))  # draws "load money" button


        font = pygame.font.Font('freesansbold.ttf', 12)

        mainMenuText = font.render("Main Menu", True, (255, 255, 255))
        creditCardText = font.render("Credit Card:", True, (255, 255, 255))
        loadMoneyText = font.render("Load Money:", True, (255, 255, 255))
        cartText = font.render("Cart:", True, (255, 255, 255))
        creditCardButtonText = font.render("Confirm", True, (255, 255, 255))
        loadMoneyButtonText = font.render("Load Money", True, (255, 255, 255))
        balanceText = font.render("Balance:", True, (255, 255, 255))
        amountText = font.render(str(self.currentUser.balance), True, (255, 255, 255))

        mainMenuTexttRect = mainMenuText.get_rect()
        creditCardTextRect = creditCardText.get_rect()
        loadMoneyTextRect = loadMoneyText.get_rect()
        cartTextRect = cartText.get_rect()
        creditCardButtonTextRect = creditCardButtonText.get_rect()
        loadMoneyButtonTextRect = loadMoneyButtonText.get_rect()
        balanceTextRect = balanceText.get_rect()
        amountTextRect = amountText.get_rect()

        mainMenuTexttRect.center = (350, 50)
        creditCardTextRect.center = (205, 165)
        loadMoneyTextRect.center = (205, 240)
        cartTextRect.center = (205, 285)
        creditCardButtonTextRect.center = (497.5, 167.5)
        loadMoneyButtonTextRect.center = (497.5, 242.5)
        balanceTextRect.center = (325, 115)
        amountTextRect.center = (375, 115)

        window.blit(mainMenuText, mainMenuTexttRect)
        window.blit(creditCardText, creditCardTextRect)
        window.blit(loadMoneyText, loadMoneyTextRect)
        window.blit(cartText, cartTextRect)
        window.blit(creditCardButtonText, creditCardButtonTextRect)
        window.blit(loadMoneyButtonText, loadMoneyButtonTextRect)
        window.blit(balanceText, balanceTextRect)
        window.blit(amountText, amountTextRect)


        x = 100
        y = 300

        for ticket in self.currentUser.cart.items:  # draw box for each ticket
            pygame.draw.rect(window, (200, 0, 75), (x, y, 500, 35))

            ticketText = font.render(str(ticket), True, (255, 255, 255))
            ticketTextRect = ticketText.get_rect()
            ticketTextRect.center = (x + 250, y + 17)
            window.blit(ticketText, ticketTextRect)

            y += 60


        if self.errorMessage != None:
            self.drawError(window)



    def buttonPressed(self, x, y):
        if self.errorMessage == None:
            allGood = True
        else:
            allGood = False

        if self.mode == "LOGIN":
            if x > 150 and x < 280 and y > 350 and y < 415 and allGood:  #Login button was pressed
                self.login(self.usernameInput.get_text(),self.passwordInput.get_text())

            if x > 425 and x < 555 and y > 350 and y < 415 and allGood: #Create Account button pressed
                self.createAccount(self.usernameInput.get_text(),self.passwordInput.get_text())

            if (not allGood) and x > 275 and x < 425 and y > 280 and y < 330:
                self.errorMessage = None


        elif self.mode == "MAINMENU":
            if x > 100 and x < 175 and y > 25 and y < 75 and allGood: #Add to Cart button pressed
                self.addToCart()
            if x > 200 and x < 275 and y > 25 and y < 75 and allGood: #Sell Ticket button pressed
                self.sellTicket()
            if x > 425 and x < 500 and y > 25 and y < 75 and allGood: #Filter by Price button pressed
                self.filterByPrice()
            if x > 525 and x < 600 and y > 25 and y < 75 and allGood: #Filter by Artist button pressed
                self.filterByArtist()
            if x > 312.5 and x < 387.5 and y > 25 and y < 75 and allGood: #Account button pressed
                self.selectedTicket = None
                self.mode = "ACCOUNT"

            if (not allGood) and x > 275 and x < 425 and y > 280 and y < 330:
                self.errorMessage = None

            #check if a ticket is selected
            ticketx = 100
            tickety = 125
            for i in range(len(self.filteredTickets)):
                if x > ticketx and x < (ticketx + 500) and y > tickety and y < (tickety + 35):
                    if self.selectedTicket == None or self.selectedTicket != self.filteredTickets[i]:
                        self.selectedTicket = self.filteredTickets[i]   #sets the selected ticket to the chosen ticket
                    else:
                        self.selectedTicket = None #however, if a ticket is selected, unselects it
                tickety += 70


        elif self.mode == "ACCOUNT":
            if x > 300 and x < 400 and y > 25 and y < 75 and allGood: #Account button pressed
                self.mode = "MAINMENU"

            if x > 460 and x < 535 and y > 152.5 and y < 182.5 and allGood: #confirm credit card pressed
                self.confirmCreditCard()

            if x > 460 and x < 535 and y > 227.5 and y < 257.5 and allGood: #load money pressed
                self.loadMoney()

            if (not allGood) and x > 275 and x < 425 and y > 280 and y < 330:
                self.errorMessage = None



    def login(self, username, password):  #called when the login button is pressed
        #print("Login Attempt!")
        #print("Username: " + username)
        #print("Password: " + password)

        self.usernameInput.clear()
        self.passwordInput.clear()

        if username == "":
            self.errorMessage = "Enter a Username"
            return
        elif password == "":
            self.errorMessage = "Enter a Password"
            return

        for user in self.allUsers:
            if username == user.username and password == user.password:
                self.currentUser = user
                self.mode = "MAINMENU"
                return

        self.errorMessage = "Invalid Username/Password"
        return

        #if valid username + password, sets self.mode = "MAINMENU"  and sets self.currentUser to the username
        #else, set self.errerMessage = "some error message" and call self.error() function


    def createAccount(self, username, password):  #called when the create account button is pressed
        #print("Account Create Attempted!")  #this can use the same text fields as logging in, but will instead create a new account with that username + password
              #should then clear the username + login field, and allow the user to login
        #print("Username: " + username)
        #print("Password: " + password)

        self.usernameInput.clear()
        self.passwordInput.clear()

        if username == "":
            self.errorMessage = "Enter a Username"
            return
        elif password == "":
            self.errorMessage = "Enter a Password"
            return
        else:
            for user in self.allUsers:
                if username == user.username:
                    self.errorMessage = "Username Taken"
                    return

        self.usersFile.write("\n" + username + " , " + password + " , " + username + "@gmail.com" + " , " + "xxxx xxxx xxxx xxxx")
        self.usersFile.close()
        self.usersFile = open("users.txt", 'a+')

        self.readUsersFile()

    def addToCart(self):
        if self.selectedTicket == None:
            self.errorMessage = "Select a Ticket"
            return

        if self.currentUser.balance < self.selectedTicket.price:
            self.errorMessage = "Not Enough Funds"
            self.selectedTicket = None
            return

        self.currentUser.cart.addToCart(self.selectedTicket)
        self.currentUser.balance -= self.selectedTicket.price
        self.selectedTicket = None

    def sellTicket(self):
        print("Sell Ticket Button Pressed")

    def filterByPrice(self):
        print("Filter by Price Button Pressed")

        if self.filteredTickets != self.allTickets:
            self.filteredTickets = self.allTickets #if button is pressed again, resets the tickets

    def filterByArtist(self):
        print("Filter by Artist Button Pressed")

        if self.filteredTickets != self.allTickets:
            self.filteredTickets = self.allTickets #if button is pressed again, resets the tickets

    def confirmCreditCard(self):
        if (not self.creditCardInput.get_text().isnumeric()) or len(self.creditCardInput.get_text()) != 16:
            self.errorMessage = "Enter a Valid Card"
            self.creditCardInput.clear()
            return

        self.currentUser.cardInfo = self.creditCardInput.get_text()
        self.updateUsersFile()
        self.creditCardInput.clear()

    def loadMoney(self):
        if not self.loadMoneyInput.get_text().isnumeric():
            self.errorMessage = "Enter a Number"
            self.loadMoneyInput.clear()
            return

        if self.currentUser.cardInfo == "xxxx xxxx xxxx xxxx":
            self.errorMessage = "No Payment Method"
            self.loadMoneyInput.clear()
            return

        self.currentUser.balance += int(self.loadMoneyInput.get_text())
        self.loadMoneyInput.clear()


    def readUsersFile(self):  #reads users file for checking login, balance, and other important information
        self.allUsers.clear()
        self.usersFile.seek(0)
        for user in self.usersFile:
            userString = user.split(',')

            username = userString[0].strip()
            password = userString[1].strip()
            emailAddress = userString[2].strip()
            cardInfo = userString[3].strip()
            self.allUsers.append(User.User(username, password, emailAddress, cardInfo))


    def readTicketsFile(self):  #reads ticket file and files self.allTickets
        self.ticketsFile.seek(0)  # resets the file reading position to the start, before reading it
        for ticket in self.ticketsFile:
            ticketString = ticket.split(',')

            seller = ticketString[0].strip()
            artist = ticketString[1].strip()
            date = ticketString[2].strip()
            time = ticketString[3].strip()
            location = ticketString[4].strip()
            price = int(ticketString[5].strip())
            self.allTickets.append(Ticket.Ticket(seller, artist, date, time, location, price))


    def updateUsersFile(self):

        self.usersFile.truncate(0)
        for user in self.allUsers:
            if self.allUsers.index(user) == 0:
                self.usersFile.write(user.fileFormat())
            else:
                self.usersFile.write("\n" + user.fileFormat())

        self.usersFile.close()
        self.usersFile = open("users.txt", 'a+')

    def drawError(self, window):   #call this whenever an error occurs to create an error pop up with with self.errorMessage
        self.creditCardInput.visible = False
        self.loadMoneyInput.visible = False


        pygame.draw.rect(window, (255,0,0), (200,110,300,290))   #draws error window background

        pygame.draw.rect(window, (0, 0, 255), (275, 280, 150, 50))   #draws exit button

        font = pygame.font.Font('freesansbold.ttf', 20)

        errorText = font.render(self.errorMessage, True, (255, 255, 255))
        exitText = font.render("Exit", True, (255, 255, 255))

        errorTextRect = errorText.get_rect()
        exitTextRect = exitText.get_rect()

        errorTextRect.center = (350, 225)
        exitTextRect.center = (350, 305)

        window.blit(errorText, errorTextRect)
        window.blit(exitText, exitTextRect)