import asyncio
import aiohttp

from custom_components.myedenred.api.myedenred import MY_EDENRED

async def main():
    async with aiohttp.ClientSession() as session:
        api = MY_EDENRED(session)

        username = input("Enter your username/email..: ")
        password = input("Enter your password........: ")

        token = await api.login(username, password)
        if (token):
            cards = await api.getCards(token)
            print ("Cards............:", cards)
            for card in cards:
                print ("  Card Id........:", card.id)
                print ("  Card Number....:", card.number)
                print ("  Card Owner.....:", card.ownerName)
                print ("  Card Status....:", card.status)
                print ("  Card Account....")

                account = await api.getAccountDetails(card.id, token)
                print ("    IBAN.........:", account.iban)
                print ("    Card Number..:", account.cardNumber)
                print ("    First Name...:", account.cardHolderFirstName)
                print ("    Last Name....:", account.cardHolderLastName)
                print ("    Balance......:", account.availableBalance)

                printTransaction = input("Print transaction list? (y/N) ")
                if (printTransaction == "Y" or printTransaction == "y"):                    
                    [print ("  -", t.date, t.name, t.amount) 
                        for t in account.movementList]

asyncio.get_event_loop().run_until_complete(main())