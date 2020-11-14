import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VerifiedSeismComponent } from './verified-seism.component';

describe('VerifiedSeismComponent', () => {
  let component: VerifiedSeismComponent;
  let fixture: ComponentFixture<VerifiedSeismComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VerifiedSeismComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(VerifiedSeismComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
