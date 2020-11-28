# Todo

Create a class called Correlation. It should accept a list of events to track. On every update, a check should be run that

Maybe use a set? To tracked events unique, and then some sort of a TTL to get rid of old events being tracked. Every incoming event should run a check to see if it's criteria have been met.  If they have, the "action" method should be run for that particular instance of the class.

Creating a new instance of the class should add the "event to be tracked" to a master event tracker, so that each instance of that event gets added to it's list of caught events. Each new event that is not to be tracked is simply discarded.  Each new event to be tracked does three things.

1. Delete all old events that don't match the TTL criteria
1. Delete all instances of the currently tracked event
1. Add the event
1. Check to see if all criteria are met
   1. If so, execute the action trigger
   1. If not, wait for next matched event
