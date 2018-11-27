# ksp-sync
A small (and buggy!) KSP save data merging tool using python
NOTE: this program uses pickle to send data, so it is unsecure! REALLY do not use this without modifying!

This program was a test to see if KSP semi-asyncronous multiplayer is feasible.
The server must be run, and when the clients want to merge their save files, they run asyncClient.py in their save file.

The program works by parsing save data for ships and sending it to the server, who then determines if the master save file should have the ship added / updated.

There is some issue with time advancing etc, and how that is merged.
