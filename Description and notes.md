This project is meant to track 3D printer filament inventory and spools.

There will be three main components: Front end, back end, and database. Each of these will be built in python (except the database), and all will be separate containers running in a a portainer stack.

I also want to provide a website for showing the API documentation (probably swagger, this may require another container, I'm not sure).

Database will be postgres.

Rest api endpoints that backend provides (may need more):
Update filly (update quantity, adding more spools will use add filly)
Add filly
Remove filly?
Get filly
Get all fillys
    should ignore any fillys with 0g current quantity unless specifically asked for
Add filly type/subtype/brand/etc (maybe one endpoint, maybe more)
Add filly color
Delete filly type/subtype/brand/etc (maybe one endpoint, maybe more)
Delete filly color
search filly by any characteristic (type, color, brand, subtype, active/not active, opened/not opened, etc)
import/export to be added later
API will be fast api

Characteristics of filly (for python class):
Type (pla, petg, abs)
Color
Brand
Subtype (Basic, Matte, HF, silk, plus, metal, wood)
Original spool quantity (grams)
Opened/not opened flag
Current quantity (grams)
Is active roll (on printer)
Filament length and diameter are not necessary

DB tables:
Rolls of filly (this table should have a column for each characteristic above) - these will end up being updated by the front end (through backend rest api) - ie want a row for all filaments that match a specific type/color/brand/etc, and be able to add more extra spools to the bank, but also update the current quantity of all active spools
Filly types (color combo, type, subtype, etc)
  Maybe break the filly types into separate tables
Want to be able to use those as dropdowns, and make these tables updatable
Each table should have created_at column, and for filly rolls table an updated_at column
DB tables will be created through sqlalchemy models in the backend container
No migration strategy needed right now

Python classes?:
One for db definitions of each table
One for filly front end
One for filly type (full combo)

Authentication:
Authentication is not needed. This is meant to be run locally on a home network, and not exposed to the internet.

Number of Users: Meant to be 1-2 people, but should be able to support at least 5 concurrent users

Front End:
Will use react or angular
At some point there will be multiple pages, but to start it will be one, it should be a dashboard/table that shows all filly rolls, with ability to filter/search/sort
Each row should be a different filly combination (type/color/brand/etc), there may be multiple spools in 1 row
Each row should have a column for number of "opened" spools (ie you could have 2 black-pla-matte spools active)
Default order will be based on last updated_at (if that column is empty, use created_at for that item)
There should be a button (probably one of the upper corners) to add more filly spools - this should open a form allowing you to select each of the characteristics (type/color/brand/etc), original quantity, and number of spools to add
There should also be a way to "add another 1kg spool" to an existing row - this should update the original quantity (add 1000g), and increment the number of opened spools by 1
Current quantity of a spool cannot increment, only decrement

CICD Pipelines:
Each image will be hosted on a self hosted docker registry
There should be a batch script for each container to build the docker image, and push to this registry

Testing:
Adhoc right now

