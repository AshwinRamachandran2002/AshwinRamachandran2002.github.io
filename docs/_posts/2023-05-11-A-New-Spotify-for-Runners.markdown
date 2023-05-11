---
layout: post
title:  "Spotify Playlist Seggregation for Runners"
date:   2023-05-11 08:24:51 +0200
categories: jekyll update
---

# Introduction

The idea is to seggregate your spotify playlist into different playlists, according to the pace you are running at the moment.

# Primary Features

1. Pace splits to consider: 
    a. Slow
    b. Medium
    c. Fast

2. Sort will be based upon the BPM (Spotify Metadata) of the song.

3. Beta: Toggle feature to renew your playlist with new Songs


# App Frontend (Version 1.0)

1.  A Login page (no independent SignUp) using Spotify Credentials

2.  A Home page 
    a. Display a dropdown menu, to choose form among the playlists present in the spotify app, (can choose multiple)
    b. Horizontal Scroll View to change pace setting, each view will have a display of all songs in the setting, the playing song highlighted, the user can also change the song to be played, songs will be played one after the other (Shuffle capability should be added)
    d. No controls will be displayed (Spotify displays its own controls over the App) - Play, Pause, Skip Forward, Description
    e. When playing from a specific playlist, if a song in the playlist has exceeded 3 plays, then we remove the song from the playlist 
        and add a new song according the Spotify Recommendation API
    
# No backend required