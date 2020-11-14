import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { SensorComponent } from './sensor/sensor.component';
import { UserComponent } from './user/user.component';
import { DetailedViewComponent } from './sensor/detailed-view/detailed-view.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { VerifiedSeismComponent } from './verified-seism/verified-seism.component';

@NgModule({
  declarations: [
    AppComponent,
    SensorComponent,
    UserComponent,
    DetailedViewComponent,
    HeaderComponent,
    FooterComponent,
    VerifiedSeismComponent
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
