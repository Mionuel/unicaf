# Introduction
Unicaf is a local tool used to simulate a university cafeteria in your browser. 

It comes with many configurable settings that can represent all kinds of cafeterias: different sizes / popularity / delays.

A simulated person can perform 2 actions:
1. **occupy a seat** - which means that they will have to wait in the queue if no seats are available
2. **reserve a seat** - a person selects a random currently occupied seat for reservation, only 1 person at a time can reserve a specific seat

Another feature are the **bonus snacks** - a person that has frequented the cafeteria before accumulates a configurable amount of bonus point.

After reaching a threshold they will get a bonus snack, that increase the amount of time that they occupy the seat for.

# UI

The UI is hosted on http://localhost:5173/.

The first things you will notice when opening the frontend are the 3 different tabs:
1. **Simulation** - the main tab of the application 
2. **Settings** - where you can configure the simulation to your liking
3. **Grafana** - that comes with many graphs by default that will help you monitor the simulation's progress in time

Just below the tabs you can see the **Average Waiting Time** that Gets updated every second.

After that you will see 2 sections:
1. **Queue** - as the name suggests represents the people waiting for a free seat
2. **Tables** - each table comes with 4 seats 

All the cells will initially be **empty** - they will be colored whenever a person enters the queue / takes a seat.

Whenever a cell is **clicked** a pop-up is opened that display some information about the person in the cell as well as some actions that can be performed on them.

Two **buttons** are available in the first tab:
1. **Start** - the triggers the simulation start
2. **Stop** - that clears the current queue and pauses the simulation

# Observability

The tool was built with **observability** in mind - many different internal actions produce logs which can be viewed both from Grafana UI and internally
by running
```bash
docker compose logs -f backend
```  

Go to the Grafana tab, in which you have 2 **dashboards**

## Totals
Here different stats are displayed as well as all the logs in a readable format. 

In particular you can find here:
1. the amount of reservations done, 
2. the amount of people that tried to enter the queue without sufficient credits  
3. how many total bonus snacks were assigned

## Graphs 

All kinds of time-dynamic data is displayed here.

For example:
1. **Insufficient credits rates** board displays how often are there people without enough credits
2. **Average Wait Time** displays how the waiting time changed over time 
3.  **Average Occupancy** time shows for how long does an average person occupy a seat for

# Settings

## Simulation settings

| Setting               | Description                                                                                                         |
| --------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **People Per Second** | Number of people arriving at the cafeteria per second.                                                              |
| **Tick Interval**     | Number of seconds between simulation ticks.                                                                         |
| **Update Delay**      | Number of seconds to delay the simulation so that UI changes are more visible.                                      |
| **Max Queue Size**    | Maximum number of people that can wait in the queue.                                                                |
| **Occupy Time**       | Baseline amount of time each person occupies a seat.                                                                |
| **Time Variance**     | Maximum additional occupancy time. For example, `20` means that between `0` and `20` extra seconds can be assigned. |
| **Bonus Time**        | Additional occupancy time granted by a bonus snack.                                                                 |
| **Order Cost**        | Number of credits subtracted from a person when entering the queue.                                                 |
| **Bonus Threshold**   | Number of bonus points required to receive a bonus snack.                                                           |

After changing the settings, press the **Apply** button to make the changes take effect.

## Seeding Settings

The Seeding Settings control the initial database data.

| Setting          | Description                                          |
| ---------------- | ---------------------------------------------------- |
| **Total People** | Number of randomly generated people in the database. |
| **Total Tables** | Total number of tables in the cafeteria.             |

Press **Seed DB** to reset the database and populate it using the specified values.
# Architecture

## Backend
The backend follows the **Model View Controller** design patter
* **Model** - containt the Pydantic representation of data - be it a DB entry or an endpoint response
* **View** - contains the different sql queries as query strings
* **Controller** - where the business logic itself is located 

The entrypoint of the app is the `app.py` file, that exposes simualtion related endpoints that start the main loops.

In the **config** directory you will find the following files:
1. `app_config.py` - the source of all app variables controlled in the Settings tab
2. `db_config.py` - set ups the DB for internal usage
3. `logging_config.py` - set ups the logger with desired configs

In the **db** directory you will find:
1. The main DB schema
2. The names and surnames text files from based on which the generated people will be named
3. seed.py script that populates the DB with data

## Frontend

The frontend follows the **features** project structure - each feature has a set of directories realted to it (components, services, helpers, costants, etc.)

The entrypoint is the `main.jsx` file and the `router.jsx` set-ups all the routes.

The main directory in the src/features are:
* **Grafana** - that uses an iframe to embed the grafana instance inside the frontend
* **Settings** - that defines the settings tab
* **Shared** - that contains some shared components / hooks
* **Simulation** - the main tab of the app, here you will find the queue and tables display

# Set-up

In order to use this tool, clone this repo to your computer.

## Start-up

Then build the Docker images:

```bash
docker compose build --no-cache
```

Start the application:

```bash
docker compose up -d
```


## Stopping

To stop the running containers:

```bash
docker compose down
```
