import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { UserComponent } from './user/user.component'
import { SensorComponent } from './sensor/sensor.component'
import { DetailedViewComponent } from './sensor/detailed-view/detailed-view.component'
import { HomeComponent } from './home/home.component';

const routes: Routes = [

  // Home redirection
  { path: '', redirectTo: '/home', pathMatch: 'full', data: { breadcrumb: 'Home' } },

  // Routes
  {
    path: 'home', data: { breadcrumb: 'Home' }, component: HomeComponent,
    children: [
      
      { // User
        path: 'user', component: UserComponent, data: { breadcrumb: 'Users' }, children: []
      },

      
      { // Sensor
        path: 'sensor', component: SensorComponent, data: { breadcrumb: 'Sensors' }, children: [
          { path: 'view', component: DetailedViewComponent, data: { breadcrumb: '' }, children: [] }
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
