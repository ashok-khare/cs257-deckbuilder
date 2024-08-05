import psycopg2

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
        self.orderedDeck = sorted(deck)
        self.conn = self.connect()
        self.cur = self.conn.cursor()
        self.results = []
        for method in methods:
            self.results.append(self.callMethod(method))


    def connect(self):
        '''
        Establishes a connection to the database with the following credentials:
            user - shannoh, also the database name
            password - glass458eye
        
        Returns: a database connection.

        Note: exists if a connection cannot be established.
        '''
        try:
            connection = psycopg2.connect(database="shannoh", user="shannoh", password="glass458eye", host="localhost")
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection

    
    def callMethod(self, method):
        '''
        Checks which method should be called, and then calls it and returns its result.

        PARAMETERS:
            a string method, indicating which method should be called.
        
        RETURN:
            the result of the proper method call, either an integer or a float
        '''
        if method == "Win Rate":
            return self.getWinrate()
        if method == "Elixir Cost":
            return self.getElixirCost()
        if method == "Average Trophy Count":
            return self.getAverageTrophies()
        if method == "Number of Wins":
            return self.getNumberOfWins()
        

    def getWinrate(self):
        '''
        Returns the win rate of the deck passed into the class.

        PARAMETERS:
            none, just uses the initialized deck

        RETURN:
            a float containing the win rate of the deck initialized in the class
        '''
        timesDeckUsed = self.getP1DeckCount() + self.getP2DeckCount()
        if timesDeckUsed > 0:
            return (self.getP1NumberOfWins()+self.getP2NumberOfWins())/timesDeckUsed
        else:
            return None
    
    def getP1NumberOfWins(self):
        try:
            query = "SELECT COUNT(*) FROM Matches WHERE Player1Card1 = %s AND Player1Card2 = %s AND Player1Card3 = %s AND Player1Card4 = %s AND Player1Card5 = %s AND Player1Card6 = %s AND Player1Card7 = %s AND Player1Card8 = %s AND Winner = 1"
            cursor = self.cur
            cursor.execute(query, (self.orderedDeck[0],self.orderedDeck[1],self.orderedDeck[2],self.orderedDeck[3],self.orderedDeck[4],self.orderedDeck[5],self.orderedDeck[6],self.orderedDeck[7],))
            return cursor.fetchone()[0]
        except Exception as e:
            return 0
    
    def getP2NumberOfWins(self):
        try:
            query = "SELECT COUNT(*) FROM Matches WHERE Player2Card1 = %s AND Player2Card2 = %s AND Player2Card3 = %s AND Player2Card4 = %s AND Player2Card5 = %s AND Player2Card6 = %s AND Player2Card7 = %s AND Player2Card8 = %s AND Winner = 0"
            cursor = self.cur
            cursor.execute(query, (self.orderedDeck[0],self.orderedDeck[1],self.orderedDeck[2],self.orderedDeck[3],self.orderedDeck[4],self.orderedDeck[5],self.orderedDeck[6],self.orderedDeck[7],))
            return cursor.fetchone()[0]
        except Exception as e:
            return 0

    def getP1DeckCount(self):
        try:
            query = "SELECT COUNT(*) FROM Matches WHERE Player1Card1 = %s AND Player1Card2 = %s AND Player1Card3 = %s AND Player1Card4 = %s AND Player1Card5 = %s AND Player1Card6 = %s AND Player1Card7 = %s AND Player1Card8 = %s"
            cursor = self.cur
            cursor.execute(query, (self.orderedDeck[0],self.orderedDeck[1],self.orderedDeck[2],self.orderedDeck[3],self.orderedDeck[4],self.orderedDeck[5],self.orderedDeck[6],self.orderedDeck[7],))
            return cursor.fetchone()[0]
        except Exception as e:
            return 0

    def getP2DeckCount(self):
        try:
            query = "SELECT COUNT(*) FROM Matches WHERE Player2Card1 = %s AND Player2Card2 = %s AND Player2Card3 = %s AND Player2Card4 = %s AND Player2Card5 = %s AND Player2Card6 = %s AND Player2Card7 = %s AND Player2Card8 = %s"
            cursor = self.cur
            cursor.execute(query, (self.orderedDeck[0],self.orderedDeck[1],self.orderedDeck[2],self.orderedDeck[3],self.orderedDeck[4],self.orderedDeck[5],self.orderedDeck[6],self.orderedDeck[7],))
            return cursor.fetchone()[0]
        except Exception as e:
            return 0
        

    def getElixirCost(self):
        '''
        Returns the average elixir cost of the deck initialized to the class.

        PARAMETERS:
            self
        
        RETURN:
            a float value containing the average elixir cost of the deck initialized to the class.
        '''
        try:
            avgElixirCost = 0
            containsMirror = False
            for card in self.orderedDeck:
                self.cur.execute("SELECT ElixirCost FROM Cards Where CardID = %s;", (card))
                potentialElixir = self.cur.fetchone()
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
        Returns the average trophies of players using the deck initialized to the class
        '''
        timesDeckUsed = self.getP1DeckCount() + self.getP2DeckCount()
        if timesDeckUsed > 0:
            return (self.getP1TotalTrophies()+self.getP2TotalTrophies())/timesDeckUsed
        else:
            return None

    def getP2TotalTrophies(self):
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
        Returns an integer containing the total number of wins by players using the deck initialized to the class
        '''
        return self.getP2NumberOfWins() + self.getP1NumberOfWins()

    
    def getSearchResults(self):
        '''
        Returns the results of the search in the form of a list of all of the results.
        '''
        return self.results
        

if __name__ == '__main__':
    # test code below:
    testData = DataSource([8,34,37,52,69,88,92,97],["Win Rate","Elixir Cost"])
    print(testData.getSearchResults())
