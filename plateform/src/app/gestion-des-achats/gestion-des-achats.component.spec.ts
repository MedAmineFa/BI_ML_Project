import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestionDesAchatsComponent } from './gestion-des-achats.component';

describe('GestionDesAchatsComponent', () => {
  let component: GestionDesAchatsComponent;
  let fixture: ComponentFixture<GestionDesAchatsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GestionDesAchatsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GestionDesAchatsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
