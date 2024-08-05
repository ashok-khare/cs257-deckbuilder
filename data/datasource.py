import psycopg2

class DataSource:
    '''
    DataSource executes all of the queries on the database.
    It also formats the data to send back to the frontend, typically in a list
    or some other collection or object.
    '''

    def __init__(self):
        '''
        Make sure you provide an implementation for your constructor! This is where you should initialize any of your instance variables and do any other necessary setup actions, like opening a database connection.
        '''
        pass

    def getMagnitudesInRange(self, start, end=10.0):
        '''
        Returns a list of all of the magnitudes from the specified starting magnitude until the specified ending magnitude.

        PARAMETERS:
            start - the low end of the magnitude range
            end - the high end of the magnitude range (default: 10.0)

        RETURN:
            a list of all of the earthquake events with magnitudes in the specified range
        '''
        return []
        

    def getQuakesOnContinent(self, continent):
        '''
        Returns a list of all of the earthquakes that occurred on the specified continent.

        PARAMETERS:
            continent 
        
        RETURN:
            a list of all of the earthquake events that occurred on this continent
        '''
        return []
        
    def getQuakesInCountry(self, country):
        '''
        Returns a list of all of the earthquakes that occurred in the specified country.
        '''
        return []
        
    def getQuakesInTimeRange(self, start, end):
        '''
        Returns a list of all of the earthquakes that occurred within the specified time range.
        
        Note: Assumes that times are expressed in standard time format 
        '''
        return []

    def getQuakesInDateRange(self, start, end):
        '''
        Returns a list of all of the earthquakes that occurred within the range of specified dates.

        PARAMETERS:
            start - the starting date of the range
            end - the ending date of the range

        RETURN:
            a list of all of the earthquake events that occurred within this date range.
        '''
        return []
        
    def getQuakesByType(self, quakeType):
        '''
        Returns a list of all of the earthquakes of the specified type (e.g. ice quake, quarry, explosion, etc.)
        '''
        return []
        

if __name__ == '__main__':
    # your code to test your function implementations goes here.
    pass
