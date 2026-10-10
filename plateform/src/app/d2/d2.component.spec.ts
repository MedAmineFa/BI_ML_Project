import { ComponentFixture, TestBed } from '@angular/core/testing';

import { D2Component } from './d2.component';

describe('D2Component', () => {
  let component: D2Component;
  let fixture: ComponentFixture<D2Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ D2Component ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(D2Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
