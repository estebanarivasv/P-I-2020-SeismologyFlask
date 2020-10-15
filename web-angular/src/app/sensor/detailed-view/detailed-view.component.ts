import { Component, OnInit, Input } from '@angular/core';
import { SensorModel } from 'src/app/models/sensor.model'

@Component({
  selector: 'app-sensor-view',
  templateUrl: './detailed-view.component.html',
  styleUrls: ['./detailed-view.component.scss']
})
export class DetailedViewComponent implements OnInit {

  //Property Binding
  //Carga el valor del profesor seleccionado en la variable professor
  @Input() sensor: SensorModel;


  constructor() { }

  ngOnInit(): void {
  }

}
