import sense
from random import randrange
import time
import battery

# Authentication
def authentication():
    # sense.api_key = '4a5f9881e53ba0a3cf237fa1c20737a0dbfe5e99'
    # You can get your key using the API.
    sense.api_key = sense.User.api_key(username='kellydiote', password='master2isc')
    return sense

# Get the first cookie of your account
def getCookies():
    user = sense.User.retrieve(expand=['devices'])
    return [d for d in user.devices if d.resource.slug == 'cookie']

def subscribe(cookie):
        # Create a subscription in order to receive new temperature events.
        # You will be notified of a new event on a URL of your choice,
        sub = sense.Subscription.create(
            label='%s motion feed subscription' % cookie.label,
            gatewayUrl='https://server2000.eu/events/',
            subscribes= ['/nodes/%s/feeds/temperature/' % cookie.uid]
        )
        assert sub.uid is not None

def getCookieTemperature(cookie):
        # Once you know UIDs you can instantiate objects without querying the API.
        feed = sense.Node(cookie.uid).feeds(type='temperature')

        # Get the last 5 events of the motion feed
        ev = feed.events.list(limit=1)
        #print(ev.objects[0].data.centidegreeCelsius)
        return (ev.objects[0].data.centidegreeCelsius /100)

def getChargingTime(cookieTemperature):
        cold = randrange(-10,10)
        #la tension
        dV=abs( (cookieTemperature-cold)*2.1)
        #l'intensite
        I= (dV/100)
        #temps de chargement = 1,2 * capacite de la batterie (en mA) / courant du chargeur (en mA)
        return (1.2 * 10) /(I*1000)
