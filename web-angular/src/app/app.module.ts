import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { SensorComponent } from './sensor/sensor.component';
import { UserComponent } from './user/user.component';
import { DetailedViewComponent } from './sensor/detailed-view/detailed-view.component';

@NgModule({
  declarations: [
    AppComponent,
    SensorComponent,
    UserComponent,
    DetailedViewComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
