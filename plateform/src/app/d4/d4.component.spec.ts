import { ComponentFixture, TestBed } from '@angular/core/testing';

import { D4Component } from './d4.component';

describe('D4Component', () => {
  let component: D4Component;
  let fixture: ComponentFixture<D4Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ D4Component ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(D4Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
