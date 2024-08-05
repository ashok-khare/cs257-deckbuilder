import psycopg2
import psqlconfig as config

class DataSource:
    '''
    DataSource executes all of the queries on the database.
    It also formats the data to send back to the frontend, typically in a list
    or some other collection or object.
    '''

    def __init__(self, deck, methods):
        '''
        Initializes data source from the psql database. Takes in a deck object as a list of integers and a methods object as a list of strings.
        Constructs the search results as a list of various objects, generally integers and floats.
        '''
        conn = self.connect()
        self.cur = conn.cursor()
        capitalizedDeck = []
        for card in deck:
            capitalizedDeck.append(card.title())
        self.orderedDeck = sorted(self.createDeck(capitalizedDeck))
        self.results = {}
        if len(self.orderedDeck) == 0: #check if the card names are valid
            self.results["Deck is Invalid"] = "card names were not entered correctly"
        elif self.containsRepeatCards(self.orderedDeck):
            self.results["Deck is invalid"] = "contains repeat cards"
        elif len(methods) == 0:
            self.results["Could not find statistics"] = "no statistics selected"
        elif self.deckNotInDataset() and "Elixir Cost" not in methods:
            self.results["No statistics could be found"] = "deck is not in dataset"
        elif self.deckNotInDataset() and len(methods) == 1:
            self.results["Elixir Cost"] = self.getElixirCost()
        elif self.deckNotInDataset():
            self.results["Elixir Cost"] = self.getElixirCost()
            self.results["No other statistics could be found"] = "deck is not in dataset"
        else:
            for method in methods:
                self.results[method] = self.callMethod(method)


    def connect(self):
        '''
        Establishes a connection to the database with the following credentials:
            user - shannoh, also the database name
            password - glass458eye
        
        Returns: a database connection.

        Note: exits if a connection cannot be established.
        '''
        try:
            connection = psycopg2.connect(database=config.database, user=config.user, password=config.password, host="localhost")
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection


    def createDeck(self, deck):
        '''
        Switches the deck object from names to card ids, or returns an empty deck if a card name is invalid

        PARAMETERS:
            a deck object contained in a list as cards

        RETURN:
            a deck object containing card ids instead of names, or an empty deck if a card is invalid
        '''
        try:
            newDeck = []
            for card in deck:
                cursor = self.cur
                cursor.execute("SELECT CardID FROM Cards WHERE CardName = %s", (card,))
                newDeck.append(cursor.fetchone()[0])
            return newDeck
        except Exception as e:
            newDeck = []
            return newDeck


    def containsRepeatCards(self, deck):
        '''
        Returns if the deck contains repeat cards

        PARAMETERS:
            list object containing a deck
        
        RETURN:
            a boolean value containing true if the deck contains repeat cards and false otherwise
        '''
        return deck != sorted(list(set(deck)))


    def deckNotInDataset(self):
        '''
        Returns if the specified deck is not in the dataset
        '''
        return self.getP1DeckCount() + self.getP2DeckCount() == 0


    def callMethod(self, method):
        '''
        Calls the method corresponding to the passed in method name

        PARAMETERS:
            a string method, indicating which method should be called.
        
        RETURN:
            the result of the proper method call, either an integer or a float
        '''
        if method == "Win Rate":
            return self.getWinRate()
        if method == "Elixir Cost":
            return self.getElixirCost()
        if method == "Average Trophy Count":
            return self.getAverageTrophies()
        if method == "Number of Wins":
            return self.getNumberOfWins()
        

    def getWinRate(self):
        '''
        Returns the win rate of the specified deck passed into the class.
        '''
        timesDeckUsed = self.getP1DeckCount() + self.getP2DeckCount()
        if timesDeckUsed > 0:
            return (self.getP1NumberOfWins()+self.getP2NumberOfWins())/timesDeckUsed
        else:
            return None
    
    def getP1NumberOfWins(self):
        '''
        Returns the number of wins for the specified deck when used by player 1
        '''
        try:
            query = "SELECT COUNT(*) FROM Matches WHERE Player1Card1 = %s AND Player1Card2 = %s AND Player1Card3 = %s AND Player1Card4 = %s AND Player1Card5 = %s AND Player1Card6 = %s AND Player1Card7 = %s AND Player1Card8 = %s AND Winner = 1"
            cursor = self.cur
            cursor.execute(query, (self.orderedDeck[0],self.orderedDeck[1],self.orderedDeck[2],self.orderedDeck[3],self.orderedDeck[4],self.orderedDeck[5],self.orderedDeck[6],self.orderedDeck[7],))
            return cursor.fetchone()[0]
        except Exception as e:
            return 0
    
    def getP2NumberOfWins(self):
        '''
        Returns the number of wins for the deck when used by player 2
        '''
        try:
            query = "SELECT COUNT(*) FROM Matches WHERE Player2Card1 = %s AND Player2Card2 = %s AND Player2Card3 = %s AND Player2Card4 = %s AND Player2Card5 = %s AND Player2Card6 = %s AND Player2Card7 = %s AND Player2Card8 = %s AND Winner = 0"
            cursor = self.cur
            cursor.execute(query, (self.orderedDeck[0],self.orderedDeck[1],self.orderedDeck[2],self.orderedDeck[3],self.orderedDeck[4],self.orderedDeck[5],self.orderedDeck[6],self.orderedDeck[7],))
            return cursor.fetchone()[0]
        except Exception as e:
            return 0

    def getP1DeckCount(self):
        '''
        Returns the number of times player 1 used the specified deck
        '''
        try:
            query = "SELECT COUNT(*) FROM Matches WHERE Player1Card1 = %s AND Player1Card2 = %s AND Player1Card3 = %s AND Player1Card4 = %s AND Player1Card5 = %s AND Player1Card6 = %s AND Player1Card7 = %s AND Player1Card8 = %s"
            cursor = self.cur
            cursor.execute(query, (self.orderedDeck[0],self.orderedDeck[1],self.orderedDeck[2],self.orderedDeck[3],self.orderedDeck[4],self.orderedDeck[5],self.orderedDeck[6],self.orderedDeck[7],))
            return cursor.fetchone()[0]
        except Exception as e:
            return 0

    def getP2DeckCount(self):
        '''
        Returns the number of times player 2 used the specified deck
        '''
        try:
            query = "SELECT COUNT(*) FROM Matches WHERE Player2Card1 = %s AND Player2Card2 = %s AND Player2Card3 = %s AND Player2Card4 = %s AND Player2Card5 = %s AND Player2Card6 = %s AND Player2Card7 = %s AND Player2Card8 = %s"
            cursor = self.cur
            cursor.execute(query, (self.orderedDeck[0],self.orderedDeck[1],self.orderedDeck[2],self.orderedDeck[3],self.orderedDeck[4],self.orderedDeck[5],self.orderedDeck[6],self.orderedDeck[7],))
            return cursor.fetchone()[0]
        except Exception as e:
            return 0
        

    def getElixirCost(self):
        '''
        Returns the average elixir cost of the specified deck
        '''
        try:
            avgElixirCost = 0
            containsMirror = False
            for card in self.orderedDeck:
                self.cur.execute("SELECT ElixirCost FROM Cards Where CardID = %s;", (card,))
                potentialElixir = self.cur.fetchone()[0]
                if potentialElixir == "?":
                    containsMirror = True
                else:
                    avgElixirCost += potentialElixir
            if containsMirror:
                return avgElixirCost/7
            else:
               return avgElixirCost/8
        except:
            return None

    
    def getAverageTrophies(self):
        '''
        Returns the average trophy count of players using the specified deck
        '''
        timesDeckUsed = self.getP1DeckCount() + self.getP2DeckCount()
        if timesDeckUsed > 0:
            return int((self.getP1TotalTrophies()+self.getP2TotalTrophies())/timesDeckUsed)
        else:
            return None

    def getP2TotalTrophies(self):
        '''
        Returns the sum of the trophy counts of all player 2s who used the specified deck
        '''
        try:
            query = "SELECT Player2Trophies FROM Matches WHERE Player2Card1 = %s AND Player2Card2 = %s AND Player2Card3 = %s AND Player2Card4 = %s AND Player2Card5 = %s AND Player2Card6 = %s AND Player2Card7 = %s AND Player2Card8 = %s"
            cursor = self.cur
            cursor.execute(query, (self.orderedDeck[0],self.orderedDeck[1],self.orderedDeck[2],self.orderedDeck[3],self.orderedDeck[4],self.orderedDeck[5],self.orderedDeck[6],self.orderedDeck[7],))
            total = 0
            for item in cursor.fetchall():
                total += item[0]
            return total
        except:
            return 0

    def getP1TotalTrophies(self):
        '''
        Returns the sum of the trophy counts of all player 1s who used the specified deck
        '''
        try:
            query = "SELECT Player1Trophies FROM Matches WHERE Player1Card1 = %s AND Player1Card2 = %s AND Player1Card3 = %s AND Player1Card4 = %s AND Player1Card5 = %s AND Player1Card6 = %s AND Player1Card7 = %s AND Player1Card8 = %s"
            cursor = self.cur
            cursor.execute(query, (self.orderedDeck[0],self.orderedDeck[1],self.orderedDeck[2],self.orderedDeck[3],self.orderedDeck[4],self.orderedDeck[5],self.orderedDeck[6],self.orderedDeck[7],))
            total = 0
            for item in cursor.fetchall():
                total += item[0]
            return total
        except:
            return 0
        
    
    def getNumberOfWins(self):
        '''
        Returns the total number of wins by players using the specified deck
        '''
        return self.getP2NumberOfWins() + self.getP1NumberOfWins()

    
    def getSearchResults(self):
        '''
        Returns a list of search results
        '''
        return self.results
        

if __name__ == '__main__':
    # test code below:
    pass
