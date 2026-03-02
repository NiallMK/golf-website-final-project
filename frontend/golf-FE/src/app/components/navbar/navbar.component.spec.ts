import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NavbarComponent } from './navbar.component';
import { AuthService } from '../../services/auth.service';
import { RouterTestingModule } from '@angular/router/testing';

describe('NavbarComponent', () => {

  let component: NavbarComponent;
  let fixture: ComponentFixture<NavbarComponent>;

  // Loosely typed mock for flexibility
  const mockAuthService: any = {
    currentUser: null,
    logout: jasmine.createSpy('logout')
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        NavbarComponent,      // standalone component
        RouterTestingModule   // prevents router errors
      ],
      providers: [
        { provide: AuthService, useValue: mockAuthService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(NavbarComponent);
    component = fixture.componentInstance;
  });

  it('should create navbar component', () => {
    expect(component).toBeTruthy();
  });

  it('should show Login and Register when user is not logged in', () => {
    mockAuthService.currentUser = null;
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;

    expect(compiled.textContent).toContain('Login');
    expect(compiled.textContent).toContain('Register');
  });

  it('should show Logout and Handicap when user is logged in', () => {
    mockAuthService.currentUser = {
      name: 'Niall',
      current_handicap: 2.6
    };

    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;

    expect(compiled.textContent).toContain('Logout');
    expect(compiled.textContent).toContain('Handicap');
    expect(compiled.textContent).toContain('2.6');
  });

});