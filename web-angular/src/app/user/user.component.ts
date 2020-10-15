import { Component, OnInit } from '@angular/core';

import { UserModel } from 'src/app/models/user.model'

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss']
})
  
export class UserComponent implements OnInit {

  selectedUser: UserModel;    // Empty at startup
  
  users: UserModel[] =
    [
      {
        "admin": false,
        "email": "esteban.rivas@seismologyinstitute.com",
        "id_num": 5
      },
      {
        "admin": true,
        "email": "estebanarivasv@gmail.com",
        "id_num": 8
      },
      {
        "admin": false,
        "email": "stella.brown@seismologyinstitute.com",
        "id_num": 9
      },
      {
        "admin": false,
        "email": "diana.thatcher@seismologyinstitute.com",
        "id_num": 10
      },
      {
        "admin": false,
        "email": "blaine.larsen@seismologyinstitute.com",
        "id_num": 11
      },
      {
        "admin": false,
        "email": "pete.bosch@seismologyinstitute.com",
        "id_num": 12
      }
    ];

  constructor() { }

  ngOnInit(): void {
  }

  // We difine a method that returns a UserModel type. Then we define the implementation
  onSelect(user: UserModel): void {
    this.selectedUser = user;
    // When we click on the table, it loads the selected user to the selectedUser variable
  }

  deleteUser(user: UserModel): void {
    
  }

}
