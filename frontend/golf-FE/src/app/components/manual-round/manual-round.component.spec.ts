import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManualRoundComponent } from './manual-round.component';

describe('ManualRoundComponent', () => {
  let component: ManualRoundComponent;
  let fixture: ComponentFixture<ManualRoundComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ManualRoundComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManualRoundComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
