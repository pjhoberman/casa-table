# What is this?
This is a simple app to check for availability of a reservation at Casa Bonita, once you get the email to make a reservation.

I built this for my own purposes of finding a Casa Bonita table for 6 people, dinner service, with waterfall seating.

I tried to make this extensible for others to use, but it's definitely pretty bare bones and not feature rich.

For example, it will keep texting you if a table remains available. 

But, it works and we got our booking! Feel free to modify or do what you want with this.

**Note: This may or may not be against the Terms of Service of Casa Bonita. Use at your own risk, do your own research, etc**

# How to use
## local
1. Clone this repo
2. Install the requirements with `pip install -r requirements.txt`
3. Rename `example.env` to `.env` and fill in the values
4. Run the script with `python main.py`

## docker
There is a Dockerfile. You can build and run the container. I set it up specifically to deploy it to fly.io

## fly.io
fly.io is my new heroku. Check it out. There's a `fly.toml` file in this repo. 
You can deploy this app to fly.io, just read some basic docs over there and set the secrets properly.

## etc
In main.py, there are a bunch of variables to set for your specific circumastance.

There is no .exe, sorry.

# What else
I'm not going to maintain this, but feel free to open an issue if you have any questions. 
Enjoy!
