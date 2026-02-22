# NaviTrack-Prototype

NaviTrack prototype built on Python 3 for quicker testing and deployment on prototyping environments.
This is the first subproject of the Navia project, which will also include two other subprojects.

## What is NaviTrack?
NaviTrack is a simple CLI tool for navigating directories.
It was born as an alternative to [zoxide](https://github.com/ajeetdsouza/zoxide) with a focus on speed and simplicity.
NaviTrack is not meant to integrate with any other tool out-of-the-box, but rather be used as a standalone tool with optional plugins for compatibility with other tools.

This first version of NaviTrack is a prototype and will be integrated into the official Navia release for production use in two different flavors; one for servers and one for desktop environments.

The prototype is being built for a Unix-like, desktop environment.

## How does NaviTrack work?
NaviTrack uses a simple algorithm to remember directories based on the user's history of directory visits.
It also allows the user to add custom aliases to directories or files, which can be used to navigate to them more easily.

The term for aliases is "tracks."

All tracks are stored in an SQLite database, which is located in the user's home directory.

## Who is NaviTrack for?
NaviTrack is meant for people who want to navigate directories quickly and easily.
It's meant for both the user that wants a simple CLI tool and the developer that wants to integrate NaviTrack into their own tools.

Yet this prototype is not meant for production use, as it will be integrated into the official and more reliable Navia release for production use.

[Do you want NaviTrack on a server? Take a look at the official Navia release and its different Use Cases (**NaviTrack server edition will be available soon**)]()

Tracks can be numbered so that they can be accessed by their number.
Tracks can also be named so that they can be accessed by their name.
These can be managed using the built-in CLI tool.

## How to use NaviTrack?
NaviTrack is a simple CLI tool that can be used to navigate directories.

### Basic Usage
To save the current working directory as track number 0:
```sh
track # Saves the pwd in track number 0
```

To cd to the directory stored in track number 0:
```sh
navi # Changes to the directory stored in track number 0
```

### Tracking with numbers
To save the current working directory as track number 1:
```sh
track 1 # Saves the pwd in track number 1
```

To cd to the directory stored in track number 1:
```sh
navi 1 # Changes to the directory stored in track number 1
```

Tracks can also be stored even if they are not the pwd:
```bash
track 2 /home/foo
# Saves the specified directory as track number 2
```

### Tracking with names
To save the current working directory as track "foo":
```sh
track foo # Saves the pwd in track "foo"
```

To cd to the directory stored in track "home":
```sh
navi foo # Changes to the directory stored in track "foo"
```

Tracks can also be stored even if they are not the pwd:
```bash
track foo /home/bar
# Saves the specified directory as track "foo"
```

**More tutorials will be available soon.**

## NaviTrack APIs
NaviTrack has a simple API that can be used to integrate NaviTrack into other tools and languages.

**APIs and libraries will be available soon.**

## Extra thingies
NaviTrack also has an optional built-in web server that can be used to manage the tracks and NaviTrack configurations with a user-friendly interface (**coming soon**).

It's also possible to use export and import tracks to and from JSON and CSV files.

## The best part?
It's fast! It's reliable! It's straightforward!

It's also free and open-source, so any developer can contribute to the project, and any user can use it for free.

Feedback on the project is more than welcome! I'm still a junior developer, so any help is appreciated.

## Checklist
Desktop environment:
- [x] Project structure and required functionality
  - [x] Read and parse config.toml
  - [x] Check if tracks.db (navitrack.db for now) exists and create it if it doesn't
  - [ ] Read and parse tracks.db
  - [ ] Save and load tracks by number
  - [ ] Save and load tracks by name
  - [ ] Create a wrapper for changing the directory
- [ ] Basic CLI tool functionality (bash)
  - [ ] Create all the commands and be able to parse arguments
  - [ ] Tracks with numbers
  - [ ] Tracks with names
  - [ ] Navigation
- [ ] Advanced functionality
  - [ ] Export and import tracks to and from JSON and CSV files
  - [ ] Web server
    - [ ] Create web server
    - [ ] Create a web interface
  - [ ] API
- [ ] Being able to set logging from the TOML file (with different levels, debugging...)
- [ ] Write a man page and usage documentation for using arguments. Show these usage messages when arguments aren't used properly 
- [ ] Rust time baby!

## Plans, changes, and improvements
- [ ] Add support for other shells
- [ ] Add support for other operating systems
- [ ] Add support for other languages
- [ ] Add support for other configuration formats (JSON and YAML)
  (Which requires →)
  - [ ] Renovating the configuration class with _layers_ as objects
    - [ ] Parsing a JSON / YAML into an object containing a dictionary which can have nested dictionaries 
    - [ ] Be able to get the depth of that dictionary (max count of nested dictionaries)
- [ ] Add support for server environments (bare metal)
  - [ ] Add support for systemd
  - [ ] Add support for other databases
- [ ] Add support for Docker
  - [ ] Add support for other databases
  - [ ] Publish the image on Docker Hub
