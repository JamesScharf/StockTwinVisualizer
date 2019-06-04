import cherrypy
import dashboard

class StockServer(object):
    @cherrypy.expose
    def index(self, stockSYM=""):

        LandingPageFile = open("LandingPage.html", "r")
        
        '''
        if we don't have an inputted stock, then we want the default page
        which tells the user what to do
        '''

        if stockSYM == "":
            return LandingPageFile.read()

        splitGET = stockSYM.split()
        if len(splitGET) < 2:
            return "ERROR: PLEASE ENTER IN THE CORRECT FORMAT"
        inputtedStock = splitGET[0]
        inputtedSample = splitGET[1]

        '''
        We do have an inputted stock symbol, so now we need to
        generate the dashboards, which we will then serve.
        '''
        DashboardHomeFile = open("DashboardHome.html", "r")

        DashboardHome = DashboardHomeFile.read()

        try:
            polarityScript, polarityHtml, biasScript, biasHtml, relScript, relHtml = dashboard.makeDashboards(inputtedStock, int(inputtedSample))
        except:
            return "ERROR: PLEASE ENTER A STOCK SYMBOL THAT EXISTS."

        DashboardHome = DashboardHome.replace("{{polarityScript}}", polarityScript)
        DashboardHome = DashboardHome.replace("{{polarityHtml}}", polarityHtml)
        DashboardHome = DashboardHome.replace("{{biasScript}}", biasScript)
        DashboardHome = DashboardHome.replace("{{biasHtml}}", biasHtml)
        DashboardHome = DashboardHome.replace("{{relScript}}", relScript)
        DashboardHome = DashboardHome.replace("{{relHtml}}", relHtml)

        return DashboardHome

cherrypy.quickstart(StockServer())