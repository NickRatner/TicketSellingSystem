class ShoppingCart:
    def __init__(self):
        self.items = []
        self.tickets = 0
        self.total = 0

    def addToCart(self, ticket):
        self.items.append(ticket)
        self.tickets += 1
        self.total += ticket.price
        #print(f"{ticket.name} added to cart.")

    def removeFromCart(self, ticket):
        if ticket in self.items:
            self.items.remove(ticket)
            self.tickets -= 1
            self.total -= ticket.price
            #print(f"{ticket.name} removed from cart.")
        else:
            print("Ticket not found in cart.")

    def emptyCart(self):
        self.items = []
        self.tickets = 0
        self.total = 0
        print("Cart emptied.")

    def confirmTicketAdded(self):
        if self.tickets > 0:
            print(f"{self.tickets} ticket(s) added to cart. Total price: {self.total}.")
        else:
            print("Cart is empty.")

    def confirmTicketRemoved(self):
        if self.tickets > 0:
            print(f"{self.tickets} ticket(s) removed from cart. Total price: {self.total}.")
        else:
            print("Cart is empty.")
