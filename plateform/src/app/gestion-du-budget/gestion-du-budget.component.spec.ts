import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestionDuBudgetComponent } from './gestion-du-budget.component';

describe('GestionDuBudgetComponent', () => {
  let component: GestionDuBudgetComponent;
  let fixture: ComponentFixture<GestionDuBudgetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GestionDuBudgetComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GestionDuBudgetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
