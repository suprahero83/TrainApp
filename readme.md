### Active Profile create db ###
con.execute("create table activeprofile (id INTEGER PRIMARY KEY AUTOINCREMENT, tracknum INT NOT NULL, trainID INT NOT NULL)")

### TrainPower - The service that connects to the GPIO to control the train ###
### Check Status ###
sudo systemctl status trainpower.service
### Start Train Power ###
sudo systemctl start trainpower.service
### Stop Train Power ###
sudo systemctl stop trainpower.service
### Restart Train Power ###
sudo systemctl restart trainpower.service

### TrainApp - The service that run the web interface ###
### Check Status ###
sudo systemctl status trainapp.service
### Start Train App ###
sudo systemctl start trainapp.service
### Stop Train App ###
sudo systemctl stop trainapp.service
### Restart Train App ###
sudo systemctl restart trainapp.service

