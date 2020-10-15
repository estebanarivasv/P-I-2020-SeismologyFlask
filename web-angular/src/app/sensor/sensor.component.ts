import { Component, OnInit } from '@angular/core';
import { SensorModel } from '../models/sensor.model';

@Component({
  selector: 'app-sensor',
  templateUrl: './sensor.component.html',
  styleUrls: ['./sensor.component.scss']
})
export class SensorComponent implements OnInit {

  selectedSensor: SensorModel;    // Empty at startup
  
  sensors: SensorModel[] = [
    {
      "active": true,
      "id_num": 1,
      "ip": "127.0.0.1",
      "name": "LetS4",
      "port": 5000,
      "status": false,
      "user": {
        "admin": false,
        "email": "esteban.rivas@seismologyinstitute.com",
        "id_num": 5
      }
    },
    {
      "active": true,
      "id_num": 2,
      "ip": "127.0.0.1",
      "name": "C3A58D",
      "port": 5001,
      "status": false,
      "user": {
        "admin": false,
        "email": "diana.thatcher@seismologyinstitute.com",
        "id_num": 10
      }
    },
    {
      "active": true,
      "id_num": 3,
      "ip": "127.0.0.1",
      "name": "AB364S",
      "port": 5002,
      "status": false,
      "user": {
        "admin": false,
        "email": "esteban.rivas@seismologyinstitute.com",
        "id_num": 5
      }
    },
    {
      "active": true,
      "id_num": 4,
      "ip": "127.0.0.1",
      "name": "OOP158",
      "port": 5003,
      "status": false,
      "user": {
        "admin": false,
        "email": "stella.brown@seismologyinstitute.com",
        "id_num": 9
      }
    },
    {
      "active": true,
      "id_num": 6,
      "ip": "127.0.0.1",
      "name": "8XZKE0",
      "port": 5004,
      "status": false,
      "user": {
        "admin": false,
        "email": "diana.thatcher@seismologyinstitute.com",
        "id_num": 10
      }
    },
    {
      "active": true,
      "id_num": 7,
      "ip": "127.0.0.1",
      "name": "Q8WDS5",
      "port": 5005,
      "status": false,
      "user": {
        "admin": false,
        "email": "esteban.rivas@seismologyinstitute.com",
        "id_num": 5
      }
    },
    {
      "active": true,
      "id_num": 8,
      "ip": "127.0.0.1",
      "name": "87ASZ5",
      "port": 5006,
      "status": false,
      "user": {
        "admin": false,
        "email": "esteban.rivas@seismologyinstitute.com",
        "id_num": 5
      }
    },
    {
      "active": true,
      "id_num": 9,
      "ip": "127.0.0.1",
      "name": "A/S4W",
      "port": 5007,
      "status": false,
      "user": {
        "admin": false,
        "email": "stella.brown@seismologyinstitute.com",
        "id_num": 9
      }
    }
  ];

  constructor() { }

  ngOnInit(): void {
  }

  // We difine a method that returns a UserModel type. Then we define the implementation
  onSelect(sensor: SensorModel): void {
    this.selectedSensor = sensor;
    // When we click on the table, it loads the selected user to the selectedUser variable
  }

  deleteSensor(sensor: SensorModel): void {
    
  }
}
