class Ticket:
   def __init__(self, seller, artist, date, time, location, price):
       self.seller = seller
       self.artist = artist
       self.date = date
       self.time = time
       self.location = location
       self.price = price

   def details(self):
       print("Ticket Details:",
       "\nArtist: ", self.artist,
       "\nLocation: ", self.location,
       "\nDate: ", self.date,
       "\nTime: ", self.time,
       "\nPrice: ", self.price)

   def __repr__(self):   #this allows tickets to be printed easier for testing
       return self.__str__()

   def __str__(self):
       return ('{' + self.seller + ', ' + self.artist + ', ' + self.date + ', ' + self.time + ', ' + self.location + ', ' + str(self.price) + '}')