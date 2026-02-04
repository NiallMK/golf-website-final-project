import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BookTeeTimeComponent } from './book-tee-time.component';

describe('BookTeeTimeComponent', () => {
  let component: BookTeeTimeComponent;
  let fixture: ComponentFixture<BookTeeTimeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BookTeeTimeComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BookTeeTimeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
