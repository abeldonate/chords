# Chords

An app that displays and transports any custom song with chords.

## Motivation
There are plenty of online websites and apps for guitar/piano/ukulele tabs for the most celebrated songs. However, as a guitar apprentice, I want something straightforward, which can tackle the main problems I notice in these programs:
- Some less-known songs are not there (or are distributed in different ones)
- Transportation is not allowed in the majority of them (or is premium)
- Some of them need registration
- Plenty of ads

For these reasons I decided to code this simple app.


## Working principle
The folder specified as `MD_PATH` in the config file must contain `.md` files with the desired songs. The format of the file must be like this:

    Name: Stick Season
    Artist: Noah Kahan
    Tune: 0
    
    ---
           <A>
    As you promised me that I was more than all the miles combined
                  <E>
    You must have had yourself a change of heart like halfway through the drive
                     <F#m>
    'Cause your voice trailed off exactly as you passed my exit sign
    <D>
    Kept on driving straight and left our future to the right 

The fields `Name` and `Artist` are important for displaying the list of all the songs in the main page. The format of the chords must be enclosed with `<>`.

## Installation
Clone the repository

    $ git clone https://github.com/abeldonate/chords.git

Setup the environment

    $ make setup

Write a couple of tabs files in the folder specified in the variable `MD_PATH` in the config file. 

Run the program with

    $ make