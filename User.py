import ShoppingCart
class User:


    def __init__(self, username, password, emailAddress, cardInfo):
        self.username = username
        self.password = password
        self.emailAddress = emailAddress
        self.cardInfo = cardInfo
        self.balance = 0
        self.favourites = []
        self.cart = ShoppingCart.ShoppingCart()

    def displayCart(self):
        print(self.cart.items)

    def loadMoney(self, amount):
        self.balance += amount

    def __repr__(self):  # this allows tickets to be printed easier for testing
        return self.__str__()

    def __str__(self):
        return (
                    '{' + self.username + ', ' + self.password + ', ' + self.emailAddress + ', ' + self.cardInfo + '}')


