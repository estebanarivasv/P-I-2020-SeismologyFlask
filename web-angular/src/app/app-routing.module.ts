import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { UserComponent } from './user/user.component'
import { SensorComponent } from './sensor/sensor.component'
import { DetailedViewComponent } from './sensor/detailed-view/detailed-view.component'

const routes: Routes = [

  // Home redirection
  {
    path: '',
    redirectTo: '/',
    pathMatch: 'full',
    data: {
      breadcrumb: 'Home'
    }
  },

  // Routes
  {
    path: '',
    data: {
      breadcrumb: 'Home'
    },
    children: [
      // User
      {
        path: 'user',
        component: UserComponent,
        data: {
          breadcrumb: 'User'
        },
        children: []
      },

      // Sensor
      {
        path: 'sensor',
        component: SensorComponent,
        data: {
          breadcrumb: 'Sensor'
        },
        children: [
          {
            path: 'view',
            component: DetailedViewComponent,
            data: {
              breadcrumb: ''
            },
            children: []
          }
        ]
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
